from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Tag(models.Model):
    name = models.CharField(max_length=100)
    image = models.FileField(upload_to="tags")

    def __str__(self):
        # Return a string that represents the instance
        return self.name


class Wine(models.Model):
    short_name = models.CharField(max_length=100)
    full_name = models.CharField(max_length=100)
    image = models.FileField(upload_to="wines")
    order = models.IntegerField()  # ex: 3rd wine of the session
    variety = models.CharField(max_length=100)  # cepage
    region = models.CharField(max_length=100)  # country, specific region
    alcohol_content = models.FloatField()  # in %
    sweetness = models.FloatField()  # in g/L
    tags = models.ManyToManyField(Tag)  # natural, organic etc.

    def __str__(self):
        # Return a string that represents the instance
        return self.short_name


class Session(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()
    wines = models.ManyToManyField(Wine)

    def __str__(self):
        # Return a string that represents the instance
        return f"{self.name} - {self.date}"


class UserScore(models.Model):  # All scores for a user
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        # Return a string that represents the instance
        return f"{self.name}'s scores"


class WineScore(models.Model):
    user_score = models.ForeignKey(UserScore, on_delete=models.CASCADE)
    wine = models.ForeignKey(Wine, on_delete=models.CASCADE)
    score = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(10.0)])
