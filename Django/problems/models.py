from django.db import models

from users.models import Profile


class Tag(models.Model):
    name = models.CharField(max_length=30, blank=False, null=False, unique=True)

    def __str__(self):
        return self.name


class Mistake(models.Model):
    name = models.CharField(max_length=150, blank=False, null=False)


class Problem(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)

    title = models.CharField(max_length=100, blank=False, null=False)
    description = models.TextField(blank=False, null=False)
    photo = models.TextField(blank=True, null=True)
    tag = models.ForeignKey(Tag, blank=False, null=True, on_delete=models.SET_NULL)

    latitude = models.FloatField(blank=False, null=False)
    longitude = models.FloatField(blank=False, null=False)
    address = models.CharField(max_length=200, blank=True)

    rating = models.IntegerField(blank=False, null=False, default=0)
    voted_by = models.ManyToManyField(Profile, related_name='voted', blank=True)
    mistake = models.IntegerField(blank=False, null=False, default=0)

    solved = models.BooleanField(null=False, default=False)

    def solve(self):
        self.status = True

    def json(self):
        return dict(title=self.title, img=self.photo, coords=[self.latitude, self.longitude], address=self.address,
                    description=self.description, rating=self.rating, status=self.solved, id=self.pk)

    def __str__(self):
        return self.title
