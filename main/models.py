from django.db import models
from django.contrib.auth.models import User


class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.title)

class PersonalInfo(models.Model):
    resume = models.OneToOneField(Resume, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    address = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    website = models.CharField(max_length=200, blank= True, null= True)
    github_link = models.CharField(max_length=200, blank=True, null=True)
    linked_in_link = models.CharField(max_length=200, blank= True, null= True)
    position_title = models.CharField(max_length=200, blank=True, null=True)
    summary = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.full_name)

class Projects(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    time = models.CharField(max_length=100, blank=True, null=True)
    link = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return str(self.name)


class Education(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    institute = models.CharField(max_length=200)
    field_of_study = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    gpa = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    currently_studying = models.BooleanField(default=False)

    def __str__(self):
        return str(self.field_of_study) +' in ' + str(self.institute)


class Experience(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    company = models.CharField(max_length=200)
    company_address = models.CharField(max_length=200, blank=True, null=True)
    position = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField()
    currently_working = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.position} in {self.company}"


class SkillCategory(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        skills = ", ".join(skill.name for skill in self.skills.all())
        return f"{self.name.upper()} : {skills} "

class Skill(models.Model):
    category = models.ForeignKey(SkillCategory, on_delete= models.CASCADE, related_name='skills')
    name = models.CharField(max_length=100)

    def __str__(self):
        return str(self.name)

class AchievementsCertifications(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)

    def __str__(self):
        return str(self.title)

