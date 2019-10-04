from django.db import models
from datetime import datetime


class AbstracModel(models.Model):
    publication_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Author(AbstracModel):
    name = models.CharField(max_length=200, blank=False)
    birth = models.IntegerField(null=True)
    death = models.IntegerField(blank=True, null= True)

    def __str__(self):
        return "{} ({} - {})".format(self.name , self.birth , self.death)


class Genre(AbstracModel):
    title = models.CharField(max_length=200, blank=False)

    def __str__(self):
        return self.title


class Book(AbstracModel):
    title = models.CharField(max_length=200, blank=False)
    year = models.IntegerField(null=True)
    price = models.IntegerField(blank=False, null=False)
    author = models.ForeignKey(Author, on_delete=models.PROTECT)
    genre = models.ManyToManyField(Genre)
    cover = models.ImageField(upload_to='book_covers/', null=True, blank=True)
    pdf = models.ImageField(upload_to='pdf/', null=True, blank=True)

    def __str__(self):
        return "{} ({} - {})".format(self.title, self.year, self.author.name)




