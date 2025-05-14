from django.db import models
from django.contrib.auth.models import User

class InstructorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()
    skills = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    profile_picture = models.ImageField(upload_to='instructors/', null=True, blank=True)
    is_verified = models.BooleanField(default=False)

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    skill_coins = models.PositiveIntegerField(default=0)

class SkillClass(models.Model):
    instructor = models.ForeignKey(InstructorProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    max_participants = models.PositiveIntegerField()
    location = models.CharField(max_length=255, null=True, blank=True)
    is_online = models.BooleanField(default=True)
    scheduled_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    thumbnail = models.ImageField(upload_to='classes/', null=True, blank=True)

class Booking(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    skill_class = models.ForeignKey(SkillClass, on_delete=models.CASCADE)
    booked_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)

class SkillCoinTransaction(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    amount = models.IntegerField()
    reason = models.CharField(max_length=256)
    timestamp = models.DateTimeField(auto_now_add=True)