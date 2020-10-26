from django.db import models

from FoodBase import settings


class News(models.Model):
    title = models.CharField(max_length=128)
    photo = models.ImageField(upload_to='news', default=settings.NEWS_DEFAULT_IMAGE)
    description = models.TextField(max_length=2000)
    creation_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'News'
        ordering = ['-creation_date']
