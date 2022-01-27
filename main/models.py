from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.text import slugify
from accounts.models import Account

class Department(models.Model):
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField()
    slug = models.SlugField(null=False, unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
    

class Course(models.Model):
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField()
    department = models.ForeignKey(
                    Department,
                    on_delete=models.CASCADE,
                    related_name='courses'
                    )
    slug = models.SlugField(null=False, unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

class Group(models.Model):
    name = models.CharField(max_length=100)
    course = models.ForeignKey(
                Course,
                on_delete=models.CASCADE,
                related_name='groups'
                )
    students = models.ManyToManyField(Account, related_name='groups')

    def __str__(self):
        return f'ID: {self.id} | {self.name}'

class Module(models.Model):
    name = models.CharField(max_length=100)
    tutors = models.ManyToManyField(Account, related_name='tutors')
    course = models.ForeignKey(
                Course,
                on_delete=models.CASCADE,
                related_name='modules'
                )

    def __str__(self):
        return f'ID: {self.id} | {self.name}'

class Exam(models.Model):
    name = models.CharField(max_length=100)
    module = models.ForeignKey(
                Module,
                on_delete=models.CASCADE,
                related_name='exams'
                )
    tutor = models.ForeignKey(Account, on_delete=models.CASCADE)
    group = models.ForeignKey(Group,on_delete=models.CASCADE)
    date = models.DateField()

    def __str__(self):
        return f'ID: {self.id} | {self.name}'

class Grade(models.Model):
    value = models.PositiveSmallIntegerField(
                validators=[MaxValueValidator(100),MinValueValidator(0)]
            )
    student = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='grades')
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='grades')
