from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    skills_offered = models.TextField(help_text="Skills you can teach (comma-separated)", blank=True)
    skills_wanted = models.TextField(help_text="Skills you want to learn (comma-separated)", blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

class Skill(models.Model):
    CATEGORY_CHOICES = [
        ('technology', 'Technology'),
        ('languages', 'Languages'),
        ('arts', 'Arts & Crafts'),
        ('music', 'Music'),
        ('sports', 'Sports'),
        ('cooking', 'Cooking'),
        ('business', 'Business'),
        ('other', 'Other'),
    ]
    
    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class SkillExchange(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requested_exchanges')
    provider = models.ForeignKey(User, on_delete=models.CASCADE, related_name='provided_exchanges')
    skill_offered = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='offered_in_exchanges')
    skill_wanted = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='wanted_in_exchanges')
    description = models.TextField(help_text="Describe what you want to learn/teach")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    scheduled_date = models.DateTimeField(null=True, blank=True)
    location = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.requester.username} wants {self.skill_wanted.name} from {self.provider.username}"

class Message(models.Model):
    exchange = models.ForeignKey(SkillExchange, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"Message from {self.sender.username} at {self.timestamp}"

class Review(models.Model):
    exchange = models.ForeignKey(SkillExchange, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_given')
    reviewed_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_received')
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # 1-5 stars
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['exchange', 'reviewer']

    def __str__(self):
        return f"Review by {self.reviewer.username} for {self.reviewed_user.username}"