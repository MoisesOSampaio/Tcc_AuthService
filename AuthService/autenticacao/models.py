from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True)
    cargo = models.CharField(max_length=100, null=False)
    lideranca = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'users' 

    def __str__(self):
        return self.username
