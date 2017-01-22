from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import datetime


# Create your models here.
class UserProfile(models.Model):
    class Meta:
        db_table = 'profile'

    user = models.OneToOneField(User)
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


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/pictures//user_<id>/<filename>
    return 'pictures/user_{0}/{1}'.format(instance.user.id, filename)


class UserImage(models.Model):
    class Meta:
        db_table = 'user_image'

    user = models.ForeignKey(User)
    image_height = models.PositiveIntegerField(default=200)
    image_width = models.PositiveIntegerField(default=200)
    image = models.ImageField(upload_to=user_directory_path, height_field='image_height', width_field='image_width')
    creation_date = models.DateTimeField(default=datetime.now())
    public = models.BooleanField(default=True)

    def __str__(self):
        return ' %s - %s - %s' % (self.user.username, self.image.name, self.creation_date)
