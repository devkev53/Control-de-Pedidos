from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.


def custom_upload_to(instance, filename):
    old_instance = Profile.objects.get(pk=instance.pk)
    old_instance.avatar.delete()
    return 'profile/' + filename


class Profile(models.Model):
    user = models.OneToOneField(
        User, verbose_name='Usuario', on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to=custom_upload_to, null=True, blank=True)
    bio = models.TextField('Biografia', null=True, blank=True)
    link = models.URLField('Link', max_length=200, null=True, blank=True)

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"

    def __str__(self):
        return '%s' % (self.user)

    @receiver(post_save, sender=User)
    def ensure_profile_exits(sender, instance, **kwargs):
        if kwargs.get('created', False):
            Profile.objects.get_or_create(user=instance)
            print('se acaba de crear un usuario y su perfil enlazado')
