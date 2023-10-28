
import os

from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter
from channels.routing import URLRouter

from manage_user.routing import ws_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'deploy_django.settings')

application = ProtocolTypeRouter(
	{
		'http': get_asgi_application(),
		'websocket': AuthMiddlewareStack(URLRouter(ws_urlpatterns))
    }
)
