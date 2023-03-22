from django.db import models


# Create your models here.
class Usermanagement(models.Model):
    idusermanagement = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=200)
    userrole = models.CharField(max_length=30)
    password = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "usermanagement"


# Counter
class Counter(models.Model):
    key = models.CharField(max_length=200, unique=True)
    value = models.IntegerField()

    class Meta:
        db_table = "counter"
