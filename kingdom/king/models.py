from django.db import models

# Create your models here.
class Kingdom(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name + " kingdom."

class King(models.Model):
    name = models.CharField(max_length=50)
    kingdom = models.OneToOneField(Kingdom, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name + ", king of " + self.kingdom.name + "."

class Servant(models.Model):
    name = models.CharField(max_length=50)
    kingdom = models.ForeignKey(Kingdom, on_delete=models.CASCADE, default=None, null=True, blank=True)
    age = models.IntegerField()
    mail = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name + " from " + f"{'?' if self.kingdom is None else self.kingdom.name}" + "."

class TestCase(models.Model):
    kingdom = models.ForeignKey(Kingdom, on_delete=models.CASCADE)
    question = models.CharField(max_length=300)
    answer = models.BooleanField()

    def __str__(self) -> str:
        return "Tests of " + self.kingdom.name + " kingdom."