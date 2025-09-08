from backend.ioc_container import ApplicationContainer

from .app_factory import create_app

application = ApplicationContainer()
application.init_resources()
application.wire(packages=["api"])

app = create_app(application)
