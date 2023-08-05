import re
from rest_framework import permissions
from .models import UserRoleMembership, UserToPermission
from django.db import connection
from .settings import PERMISSION_START_WHITE_LIST, PERMISSION_END_WHITE_LIST, SUPER_ROLE_LIST


ROLE_AUTH_SQL = "SELECT papi.id FROM drf_rbac_permission_role par " \
      "INNER JOIN drf_rbac_permission_api pap ON pap.permission_id = par.permission_id " \
      "INNER JOIN drf_rbac_apimethodmembership pa ON pap.apimethodmembership_id = pa.id " \
      "INNER JOIN drf_rbac_api papi ON papi.id = pa.api_id " \
      "INNER JOIN drf_rbac_httpmethod pt ON pt.id = pa.method_id " \
      "WHERE par.role_id IN ({}) AND pt.name = '{}' AND (papi.url = '{}' or papi.url = '{}')"

OBJ_AUTH_SQL = "SELECT papi.id FROM drf_rbac_usertopermission_permission pua " \
       "INNER JOIN drf_rbac_usertopermission pu ON pua.usertopermission_id = pu.id " \
       "INNER JOIN drf_rbac_permission_api pap ON pap.permission_id = pua.permission_id " \
       "INNER JOIN drf_rbac_apimethodmembership pa ON pap.apimethodmembership_id = pa.id " \
       "INNER JOIN drf_rbac_api papi ON papi.id = pa.api_id " \
       "INNER JOIN drf_rbac_httpmethod pt ON pt.id = pa.method_id " \
       "WHERE pu.user_id = {} AND pt.name = '{}' AND (papi.url = '{}' or papi.url = '{}')"


class UserRolePermission(permissions.BasePermission):
    """
    Global permission check for User.
    """

    def has_permission(self, request, view):
        try:
            if request.u:
                new_path = request.path
                user_role_qs = UserRoleMembership.objects.filter(user=request.user)

                # SUPER ROLE
                if user_role_qs.filter(role__name__in=SUPER_ROLE_LIST):
                    return True

                # No role
                role_id_list = [str(user_role.role.id) for user_role in user_role_qs]
                if not role_id_list:
                    return False

                # start white
                for white_list_api in PERMISSION_START_WHITE_LIST:
                    if re.match(r"{}{}".format(white_list_api, r".*"), new_path):
                        return True

                # end white
                for white_list_api in PERMISSION_END_WHITE_LIST:
                    if re.match(r"{}{}$".format(r".*", white_list_api), new_path):
                        return True

                # delete and detail
                # DELETE,GET,PUT,PATCH match /api/paas/cluster/234/ --> /api/paas/cluster/
                if re.match(r'(.*)/\d+/$',  new_path):
                    new_path = re.sub(r'/\d+', '', new_path)

                # /api/paas/cluster/2/turn/ --> /api/paas/cluster/{}/turn/
                if re.match(r'(.*)/\d+/\w+/$',  new_path):
                    new_path = re.sub(r'/\d+/', '/{}/', new_path)

                # role perm and user perm
                role_id_format = ",".join(list(set(role_id_list)))
                new_path_format_end = new_path.rsplit("/", 1)[0]

                cursor = connection.cursor()
                cursor.execute(ROLE_AUTH_SQL.format(role_id_format, request.method.lower(),
                                                    new_path, new_path_format_end))
                result = cursor.fetchall()

                def obj_perm(cr):
                    if UserToPermission.objects.filter(user=request.u).exists():
                        cr.execute(OBJ_AUTH_SQL.format(request.u.id, request.method.lower(),
                                                       new_path, new_path_format_end))
                        return cr.fetchall()

                if result or obj_perm(cursor):
                    return True
        except Exception as e:
            raise ValueError(e)
