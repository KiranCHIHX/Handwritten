#####################################################################
# Copyright(C), 2022 IHX Private Limited. All Rights Reserved
# Unauthorized copying of this file, via any medium is
# strictly prohibited
#
# Proprietary and confidential
# email: care@ihx.in
#####################################################################
from fastapi import FastAPI
from fastapi.routing import APIRoute
from fastapi.staticfiles import StaticFiles

from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import FileResponse

from app.api import api_router
from app.core.config import cfg
from app.core import logger

def create_app():
    """Creates the FASTAPI app."""
    app = FastAPI(
        title=cfg.APPLICATION,
        openapi_url=f"{cfg.API_PATH}/openapi.json",
        docs_url="/docs/",
        description=cfg.DESCRIPTION,
        redoc_url="/redoc/",
        version= cfg.VERSION,
        terms_of_service="https://www.ihx.in/terms.html",
        contact={
            "name": "IHX",
            "url": "https://www.ihx.in/contact-us.html",
            "email": "care@ihx.in",
        },
        license_info={
            "name": "Copyright(C), 2022 IHX Private Limited. All Rights Reserved. Unauthorized access to this system is forbidden and will be prosecuted by law. By accessing this system, you agree that your actions may be monitored if unauthorized usage is suspected.",
            "url": "https://www.ihx.in/privacy.html",
        },
    )
    logger.info("App setup completed.")
    return app

def setup_routers(app: FastAPI) -> None:
    app.include_router(api_router, prefix=cfg.API_PATH)
    # The following operation needs to be at the end of this function
    use_route_names_as_operation_ids(app)
    logger.info("App routes setup completed.")
    return app

def setup_cors_middleware(app):
    if cfg.BACKEND_CORS_ORIGINS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[str(origin) for origin in cfg.BACKEND_CORS_ORIGINS],
            allow_credentials=True,
            allow_methods=["*"],
            expose_headers=["Content-Range", "Range"],
            allow_headers=["Authorization", "Range", "Content-Range"],
        )
    logger.info("App CORS setup completed.")
    return app


def use_route_names_as_operation_ids(app: FastAPI) -> None:
    """
    Simplify operation IDs so that generated API clients have simpler function
    names.

    Should be called only after all routes have been added.
    """
    route_names = set()
    for route in app.routes:
        if isinstance(route, APIRoute):
            if route.name in route_names:
                raise Exception("Route function names should be unique")
            route.operation_id = route.name
            route_names.add(route.name)
    logger.info("App route options setup completed.")