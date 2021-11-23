from django.db import models

class Genre(models.Model):

    name = models.CharField(max_length=1024)
    
class Movie(models.Model):

    movie_title = models.CharField(max_length=1024)
    original_title = models.CharField(max_length=1024,null=True)
    released = models.DateField()
    runtime = models.IntegerField(default=90,help_text="in minutes")
    genre = models.ManyToManyField(Genre)

    def __str__(self):
        return self.movie_title

class Person(models.Model):

    GENDER_CHOICES = (
        ('m','male'),
        ('f','female'),
        ('x','diverse'),
    )

    credited_name = models.CharField(max_length=1024)
    year_of_birth = models.IntegerField(db_index=True)
    year_of_death = models.IntegerField(null=True,blank=True)
    participates_in = models.ManyToManyField(Movie,through="Role")
    gender = models.CharField(max_length=1,choices=GENDER_CHOICES)

    def __str__(self):
        return self.credited_name

class RoleType(models.Model):

    name = models.CharField(max_length=1024,unique=True)

class Role(models.Model):

    person = models.ForeignKey(Person,on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie,on_delete=models.CASCADE)
    role = models.ForeignKey(RoleType,on_delete=models.CASCADE)

    class Meta:
        unique_together = ('person','movie','role')

class TVShow(models.Model):

    name = models.CharField(max_length=1024)
    original_title = models.CharField(max_length=1024,null=True)
    released_year = models.IntegerField()
    created_by = models.ForeignKey(Person,on_delete=models.PROTECT,null=True)

class Season(models.Model):

    season_no = models.IntegerField()
    tv_show = models.ForeignKey(TVShow, on_delete=models.PROTECT)
    cast = models.ManyToManyField(Person)

    class Meta:
        unique_together = ("season_no","tv_show")


class Episode(models.Model):

    name = models.CharField(max_length=1024)
    season = models.ForeignKey(Season,on_delete=models.PROTECT)
