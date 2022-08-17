from aiohttp import web
from app.views.views import routes, on_startup, on_shutdown

from app.middlewares.middlewares import auth_middleware


if __name__ == '__main__':
    app = web.Application(middlewares=[auth_middleware])
    # Add Routes
    app.add_routes(routes)
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)
    # Run app on port 8000
    web.run_app(app, host='127.0.0.1', port=8000)
