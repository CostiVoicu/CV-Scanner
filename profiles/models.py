from django.db import models

# Create your models here.
class Profile(models.Model):
    name = models.CharField( max_length=50)

    def __str__(self):
        return self.name
    
class KeyWord(models.Model):
    profile = models.ForeignKey(Profile, related_name='keywords', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    value = models.IntegerField()

    def __str__(self):
        return f"{self.name} ({self.value})"