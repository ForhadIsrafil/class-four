import logging
from functools import wraps
from rest_framework.exceptions import PermissionDenied
from account.models import Account

logger = logging.getLogger(__file__)


def require_permissions(model=Account):
    def outer_wrapper(func):
        @wraps(func)
        def wrapped(self, *args, **kwargs):
            id = self.kwargs.get('id')
            request = self.request
            account = self.get_object_or_404(model, id)
            allow_request = self.check_account_object_permissions(request, account)
            if allow_request is False:
                raise PermissionDenied("You are not Authorized to access this information.")
            response = func(self, *args, **kwargs)
            return response
        return wrapped
    return outer_wrapper
