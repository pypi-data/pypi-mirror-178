from django.conf import settings

User = settings.AUTH_USER_MODEL

PERMISSION_PATH = settings.BASE_DIR
PERMISSION_RELATIVE_PATH = 'permission_files'

PERMISSION_START_WHITE_LIST = getattr(settings, "PERMISSION_START_WHITE_LIST", [])
PERMISSION_END_WHITE_LIST = getattr(settings, "PERMISSION_END_WHITE_LIST", [])
SUPER_ROLE_LIST = getattr(settings, "SUPER_ROLE_LIST", [])
