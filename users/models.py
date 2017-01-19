from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class UserProfile(models.Model):
    class Meta:
        db_table = 'profile'

    user = models.OneToOneField(User)  # null=True
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birthday = models.DateField(null=True)
    url_height = models.PositiveIntegerField(default=200)
    url_width = models.PositiveIntegerField(default=200)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True,
                               height_field='url_height', width_field='url_width')
    about_user = models.TextField(max_length=300)

    def __str__(self):
        if self.first_name and self.last_name:
            return 'User "%s" -(%s %s)' % (self.user.username, self.first_name, self.last_name)
        else:
            return 'User "%s" - (None first && last name)' % self.user.username
