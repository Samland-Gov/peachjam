from django.contrib.auth import get_user_model
from django.db import models


class Article(models.Model):
    date = models.DateField(null=False, blank=False)
    title = models.CharField(max_length=1024, null=False, blank=False)
    body = models.TextField()
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    image = models.ImageField(upload_to="articles/")
    summary = models.TextField()
    slug = models.SlugField(max_length=1024, unique=True)

    def __str__(self):
        return self.title


class UserProfile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    photo = models.ImageField(upload_to="user_profiles/")
    profile_description = models.TextField()

    # @property
    # def slug(self):
    #     return self.user.first_name + self.user.
