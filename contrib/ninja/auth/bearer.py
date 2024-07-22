from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from rest_framework.authtoken.models import Token
from ninja.security import HttpBearer
from ninja.errors import HttpError

from contrib.common.cached import acached
from ..schemas import UserInfo


@acached
async def authenticate(token):
    if token_obj := await Token.objects.filter(key=token).select_related("user").afirst():
        user = token_obj.user
        return UserInfo.from_orm(user).model_dump()


class AuthBearer(HttpBearer):
    is_async = True
    is_superuser = False

    def __init__(self, *args, is_superuser=False, **kwargs):
        self.is_superuser = is_superuser
        super().__init__(*args, **kwargs)

    async def authenticate(self, request, token):
        if (user := await authenticate(token)):
            User = get_user_model()
            user = User(**user)
            self.check_superuser(user)
            request.user = user
            return token

    def check_superuser(self, user):
        try:
            assert user.is_superuser if self.is_superuser else True
        except Exception as e:
            raise HttpError(403, str(_("Admin only")))
