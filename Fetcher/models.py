from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

# Create your models here.


class Company(models.Model):
    name = models.TextField()

    def __str__(self):
        return self.name


class Source(models.Model):
    site = models.TextField()

    def __str__(self):
        return self.site


class Work(models.Model):
    title = models.TextField()
    desc = models.TextField()
    skills = models.TextField()
    url = models.CharField(max_length=200, default=None)
    source = models.ForeignKey(Source, related_name='sources')
    company = models.ForeignKey(Company, related_name='works')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return '%s %s %s' % (self.title, self.desc, self.url)