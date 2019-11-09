import random
from hashlib import sha256
from time import time

from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    tg_token = models.CharField(max_length=64, blank=False, null=True)
    tg_activated = models.BooleanField(blank=False, null=False, default=False)

    vk_token = models.CharField(max_length=64, blank=False, null=True)
    vk_activated = models.BooleanField(blank=False, null=False, default=False)

    alice_token = models.CharField(max_length=64, blank=False, null=True)
    alice_activated = models.BooleanField(blank=False, null=False, default=False)

    def __str__(self):
        return str(self.user)

    def generate_tokens(self):
        self.tg_token = sha256(str(time() + random.random()).encode()).hexdigest()
        self.vk_token = sha256(str(time() + random.random()).encode()).hexdigest()
        self.alice_token = sha256(str(time() + random.random()).encode()).hexdigest()[:12]
