from django.contrib.auth.models import User

def from_dict(self, user_dict):
    if user_dict.get('first_name'):
        self.first_name = user_dict.get('first_name')

    if user_dict.get('last_name'):
        self.first_name = user_dict.get('last_name')

    if user_dict.get('username'):
        self.first_name = user_dict.get('username')

    if user_dict.get('email'):
        self.first_name = user_dict.get('email')

User.add_to_class("from_dict", from_dict)