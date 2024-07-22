from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError


superuser_data = dict(
    username="akb-anapa",
    email="roma2910@list.ru",
    is_staff=True,
    is_superuser=True,
)


class Command(
    BaseCommand
):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **kwargs):
        self.create_default_superuser()

    @staticmethod
    def create_default_superuser():
        User = get_user_model()
        if not (user := User.objects.filter(username=superuser_data["username"]).first()):
            print("Creating superuser.")
            user = User(**superuser_data)
            user.set_password("Akb24@$Anapa")
            user.save()
        return user
