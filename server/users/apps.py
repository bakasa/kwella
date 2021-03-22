from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'users'

    # import users.signals
    def ready(self):
        import users.signals
        return super().ready()
