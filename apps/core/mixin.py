from django.core.handlers.wsgi import WSGIRequest
from django.template import (
    loader,
    backends,
)
from django.http import HttpResponse


class HttpResponseMixin:
    """Mixin for http response rendering"""

    content_type: str = 'text/html'

    def get_http_response(
        self,
        request: WSGIRequest,
        template_name: str,
        context: dict = {},
    ):
        """Get http response"""
        template: backends.django.Template =\
            loader.get_template(
                template_name
            )
        return HttpResponse(
            template.render(
                context,
                request
            ),
            content_type=self.content_type
        )
