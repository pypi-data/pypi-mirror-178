django-front-door
===================


Simple, easy to use, middleware to lock access to any django app based on request attributes.

Quick Start
===========

Add `FrontDoorMiddleware` to your `settings.MIDDLEWARE` as first as possible.

    MIDDLEWARE = (
         'front_door.middleware.FrontDoorMiddleware',
         'django.contrib.sessions.middleware.SessionMiddleware',
         'django.middleware.common.CommonMiddleware',
         'django.middleware.csrf.CsrfViewMiddleware',
         'django.contrib.auth.middleware.AuthenticationMiddleware',
         'django.contrib.messages.middleware.MessageMiddleware',
    )
    FRONT_DOOR_ALLOWED_IPS=[],  # allowed ips
    FRONT_DOOR_ALLOWED_PATHS=[],  # url paths regex list always allowed
    FRONT_DOOR_COOKIE_NAME=None,
    FRONT_DOOR_COOKIE_PATTERN=None,
    FRONT_DOOR_DEFAULT_POLICY=FORBID,
    FRONT_DOOR_ENABLED=False,  # FrontDoor enable/disable
    FRONT_DOOR_ERROR_CODE=404,  # status code if access denied
    FRONT_DOOR_FORBIDDEN_PATHS=[],  # url paths regex list always denied
    FRONT_DOOR_HEADER=None,  # special header name without HTTP- prefix
    FRONT_DOOR_REDIR_URL="",  # HttpResponseRedirect(REDIR_URL) if access denied
    FRONT_DOOR_ROUTER="front_door.router.DefaultRouter",
    FRONT_DOOR_RULES=[
            "front_door.rules.internal_ip",  # grant access to settings.INTERNAL_IPS
            "front_door.rules.forbidden_path",  # DENY access to FORBIDDEN_PATHS
            "front_door.rules.allowed_ip",  # grant access to FORBIDDEN_PATHS
            "front_door.rules.allowed_path",  # grant access to ALLOWED_PATHS
            "front_door.rules.special_header",  # grant access if request has Header[HEADER] == TOKEN
            "front_door.rules.has_header",  # grant access if request has HEADER
            "front_door.rules.cookie_value",  # grant access if request.COOKIES[COOKIE_NAME]
            "front_door.rules.cookie_exists",  # grant access ir COOKIE_NAME in request.COOKIES
        ],
    FRONT_DOOR_TOKEN=None,  # custom header value
