"""
Setting config of Flask
"""

from datetime import timedelta


def set_app_config(app):
    """Setting config for Flask APP"""
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "School Management System REST API"
    app.config["API_VERSION"] = "v1"
    app.config["APPLICATION_ROOT"] = "/"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/api-docs"
    app.config["OPENAPI_SWAGGER_UI_URL"] = (
        "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    )
    app.config["JWT_SECRET_KEY"] = "dbeywbsakxwj903jdsnxkcjdbdsmxxdionsalxlsakcufvdcd"

    ACCESS_EXPIRES = timedelta(hours=1)
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = ACCESS_EXPIRES
    return app
