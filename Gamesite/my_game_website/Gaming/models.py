from django.db import models
from PIL import Image
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify
import urllib.parse

# Create your models here.
def game_directory_path(instance, filename):
    safe_title = urllib.parse.quote(instance.title.replace(" ", "_").lower())
    return f'web/{safe_title}/{filename}'

class Game(models.Model):
    title = models.CharField("Game Title", max_length=40)
    slug = models.SlugField(null=False, unique=True, default='')
    file = models.FileField("APK File", upload_to=game_directory_path)
    index_file = models.FileField(upload_to=game_directory_path, null=True)
    thumbnail = models.ImageField(default="profile_pics/default_game.png", upload_to='thumbnails')
    template_name = models.CharField(max_length=100, blank=True, null=True)
    uploader = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        self.template_name = f"{self.slug}.html"
        super(Game, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

class Comment(models.Model):
    game = models.ForeignKey('Game', on_delete=models.SET_NULL, null=True, blank=True)
    commenter = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    content = models.TextField('Comment', max_length=2000)

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        ordering = ['-date_created']

class Profilis(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nuotrauka = models.ImageField(default="profile_pics/default.jpg", upload_to="profile_pics")

    def __str__(self):
        return f"{self.user.username} profilis"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.nuotrauka.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.nuotrauka.path)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profilis.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profilis.save()