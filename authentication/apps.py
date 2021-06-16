from django.apps import AppConfig


class AuthenticationConfig(AppConfig):
    name = 'authentication'
    def ready(self):
        from django.contrib.auth.models import User
        
        def from_dict(self, user_dict):
            if user_dict.get('first_name'):
                self.first_name = user_dict.get('first_name')

            if user_dict.get('last_name'):
                self.last_name = user_dict.get('last_name')

            if user_dict.get('username'):
                self.username = user_dict.get('username')

            if user_dict.get('email'):
                self.email = user_dict.get('email')

        User.add_to_class("from_dict", from_dict)