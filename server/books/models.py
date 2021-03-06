from django.db import models


class Book(models.Model):
    author = models.CharField(max_length=50)
    country = models.CharField(max_length=35)
    language = models.CharField(max_length=20)
    link = models.URLField()
    pages = models.PositiveIntegerField()
    title = models.CharField(max_length=100)
    year = models.IntegerField()

    def __str__(self) -> str:
        return f'{self.title}'
