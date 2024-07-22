from django.contrib.auth import get_user_model

from ninja import ModelSchema


class UserInfo(ModelSchema):
    class Meta:
        model = get_user_model()
        exclude = ["password", "groups", "user_permissions"]
