import datetime
import time
import os

from django.contrib.auth.models import User
from django.core import validators
from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    parent = models.ForeignKey("Category", on_delete=models.RESTRICT, default=None, blank=True, null=True,
                               verbose_name="Otasi")
    name = models.CharField(max_length=45, default=None, null=True, blank=True, verbose_name="Nomi")

    path = models.CharField(max_length=50, default='-', db_index=True)

    @staticmethod
    def fix_path(pid, path):
        for row in Category.objects.filter(parent_id=pid).order_by('id').all():
            row.path = '-' + '-'.join(path + [str(row.id)]) + '-'
            row.save(fix=False)
            Category.fix_path(row.id, path + [str(row.id)])

    def save(
            self, force_insert=False, force_update=False, using=None, update_fields=None, fix=True
    ):
        if fix:
            Category.fix_path(None, [])

        ret = super().save(force_insert, force_update, using, update_fields)
        return ret

    def __str__(self):
        return self.name

    @property
    def slug(self):
        return slugify(self.name)

    class Meta:
        verbose_name = "Kategoriya"
        verbose_name_plural = "Kategoriyalar"


def file_rename(instance, filename):
    ext = filename.split('.')[-1]
    new_filename = f"{int(time.time())}_{filename.split('.')[0]}.{ext}"

    return os.path.join('files', new_filename)


def image_rename(instance, filename):
    ext = filename.split('.')[-1]
    new_filename = f"{int(time.time())}_{filename.split('.')[0]}.{ext}"

    return os.path.join('blocks', new_filename)


class Post(models.Model):
    category = models.ForeignKey(Category, on_delete=models.RESTRICT, verbose_name="Kategoriyasi")
    owner = models.ForeignKey(User, on_delete=models.RESTRICT)

    title = models.CharField(max_length=500, verbose_name="Sarlavha")

    content = models.TextField()

    photo = models.ImageField(upload_to=image_rename, default=None, blank=True, null=True, verbose_name="Rasm")
    file = models.FileField(upload_to=file_rename, default=None, blank=True, null=True, verbose_name="Fayl")

    is_date = models.BooleanField(default=False, verbose_name="Muhim sana")
    is_audio = models.BooleanField(default=False, verbose_name="Audio")
    is_video = models.BooleanField(default=False, verbose_name="Video")

    like = models.IntegerField(default=0, validators=[validators.MinValueValidator(0)])
    dislike = models.IntegerField(default=0, validators=[validators.MinValueValidator(0)])
    read = models.IntegerField(default=0, verbose_name="o'qildi", validators=[validators.MinValueValidator(0)])
    date = models.DateTimeField(default=datetime.datetime.now, blank=True, verbose_name="Sana")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        index_together = (
            ("title", "date"),
            ("read", "like", "dislike")
        )

    @property
    def short_info(self):
        return self.content[:100]

    @property
    def slug(self):
        return slugify(self.title, allow_unicode=True)

    def __str__(self):
        return f"{self.title} ({self.id})"
