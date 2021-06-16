from django.conf import settings

def print_output(msg):
    if settings.DEBUG:
        print(msg)

    # TODO: To handle Later
    print(msg)