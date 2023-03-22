from django.apps import AppConfig
from django.contrib.auth.hashers import make_password
import os


class SdntoolConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sdntool'

    def ready(self):
        if os.environ.get('RUN_MAIN'):
            try:
                from sdntool.models import Usermanagement
                # Create the default user
                if Usermanagement.objects.all().count() > 0:
                    print("User already exists")
                else:
                    Usermanagement.objects.create(
                        username="cdcju",
                        userrole="admin",
                        password=make_password("cdcju@112358")
                    )
                    print("User created")
            except Exception as e:
                pass