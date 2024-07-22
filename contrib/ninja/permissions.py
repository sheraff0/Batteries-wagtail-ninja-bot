from functools import wraps

from django.utils.translation import gettext_lazy as _

from ninja.errors import HttpError


def permissions(
    is_superuser: bool = False,
):
    def __(coro):
        @wraps(coro)
        async def _(request, *args, **kwargs):
            try:
                assert request.user.is_superuser if is_superuser else True
            except:
                raise HttpError(403, str(_("Admin only")))
            return await coro(request, *args, **kwargs)
        return _
    return __
