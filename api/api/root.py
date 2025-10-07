from api.api.auth import router as auth_router
from backend.ioc_container import ApplicationContainer

from .app_factory import create_app

application = ApplicationContainer()
application.init_resources()
application.wire(packages=["api", "backend", auth_router])

app = create_app(application)
