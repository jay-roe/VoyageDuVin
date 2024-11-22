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
    image = models.BinaryField()
    variety = models.CharField(max_length=100)  # cepage
    region = models.CharField(max_length=100)  # country, specific region
    alcohol_content = models.FloatField()  # in %
    sweetness = models.FloatField()  # in g/L
    color = models.CharField(max_length=100) 
    tags = models.ManyToManyField(Tag, blank=True)  # natural, organic etc.
    emoji_sucre = models.BooleanField(default=False) # special boolean to show emoji in modal
    price = models.FloatField()

    def __str__(self):
        # Return a string that represents the instance
        return self.short_name


class Session(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()

    def __str__(self):
        # Return a string that represents the instance
        return f"{self.name} - {self.date}"

class SessionWine(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    wine = models.ForeignKey(Wine, on_delete=models.CASCADE)
    order = models.IntegerField()  # ex: 3rd wine of the session

    class Meta:
        unique_together = ('session', 'wine')
        ordering = ['order']

    def __str__(self):
        return f"{self.session} - {self.wine} - {self.order}"


class UserScore(models.Model):  # All scores for a user
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        # Return a string that represents the instance
        return f"{self.name}'s scores"


class WineScore(models.Model):
    user_score = models.ForeignKey(UserScore, on_delete=models.CASCADE)
    session_wine = models.ForeignKey(SessionWine, on_delete=models.CASCADE)
    score = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(10.0)])

    class Meta:
        unique_together = ('user_score', 'session_wine')

    def __str__(self):
        return f"{self.user_score} - {self.session_wine} - {self.score}"
