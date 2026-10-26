from django.db import models


class User(models.Model):
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    age = models.IntegerField()


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_photo = models.ImageField(upload_to='profile_pics', blank=True, null=True)
    location = models.CharField(max_length=100)
    experience_level = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)


class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    category = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)


class UserSkill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    skill_type = models.CharField(max_length=10, choices=[
        ('TEACHING', 'Teaching'),
        ('LEARNING', 'Learning'),
    ])
    proficiency_level = models.IntegerField()
    years_of_experience = models.IntegerField(default=0)
    is_verified = models.BooleanField(default=False)


class MentorshipRequest(models.Model):
    requester = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='sent_mentorship_requests'
    )
    recipient = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='received_mentorship_requests'
    )
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    message = models.TextField()
    status = models.CharField(max_length=10, choices=[
        ('PENDING', 'Pending'),
        ('ACCEPTED', 'Accepted'),
        ('REJECTED', 'Rejected'),
        ('CANCELLED', 'Cancelled'),
    ], default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)


class Mentorship(models.Model):
    mentor = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='mentorships_as_mentor'
    )
    learner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='mentorships_as_learner'
    )
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    request = models.OneToOneField(
        MentorshipRequest, on_delete=models.CASCADE, related_name='mentorship'
    )
    status = models.CharField(max_length=10, choices=[
        ('ACTIVE', 'Active'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ], default='ACTIVE')
    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(blank=True, null=True)


class Availability(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    day_of_week = models.IntegerField(choices=[
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    ])
    start_time = models.TimeField()
    end_time = models.TimeField()
    time_zone = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)


class Session(models.Model):
    mentorship = models.ForeignKey(Mentorship, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    meeting_link = models.URLField(blank=True)
    status = models.CharField(max_length=10, choices=[
        ('SCHEDULED', 'Scheduled'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
        ('NO_SHOW', 'No show'),
    ], default='SCHEDULED')
    created_at = models.DateTimeField(auto_now_add=True)


class LearningGoal(models.Model):
    learner = models.ForeignKey(User, on_delete=models.CASCADE)
    mentorship = models.ForeignKey(Mentorship, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateTimeField()
    target_date = models.DateTimeField()
    status = models.CharField(max_length=15, choices=[
        ('NOT_STARTED', 'Not started'),
        ('IN_PROGRESS', 'In progress'),
        ('COMPLETED', 'Completed'),
        ('PAUSED', 'Paused'),
        ('CANCELLED', 'Cancelled'),
    ], default='NOT_STARTED')


class GoalMilestone(models.Model):
    learning_goal = models.ForeignKey(LearningGoal, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    order = models.IntegerField()
    due_date = models.DateTimeField()
    status = models.BooleanField(default=False)
    completed_at = models.DateTimeField(blank=True, null=True)


class Conversation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)


class ConversationParticipant(models.Model):
    conversation = models.ForeignKey(
        Conversation, on_delete=models.CASCADE, related_name='participants'
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='conversation_participations'
    )
    joined_at = models.DateTimeField(auto_now_add=True)
    last_read_at = models.DateTimeField(blank=True, null=True)


class Message(models.Model):
    conversation = models.ForeignKey(
        Conversation, on_delete=models.CASCADE, related_name='messages'
    )
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='sent_messages'
    )
    content = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)


class SessionFeedback(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    reviewer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='session_feedbacks'
    )
    rating = models.IntegerField(choices=[
        (1, '1 star'),
        (2, '2 stars'),
        (3, '3 stars'),
        (4, '4 stars'),
        (5, '5 stars'),
    ])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Report(models.Model):
    reporter = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='submitted_reports'
    )
    reported_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reports_received'
    )
    reason = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=15, choices=[
        ('PENDING', 'Pending'),
        ('UNDER_REVIEW', 'Under review'),
        ('RESOLVED', 'Resolved'),
        ('DISMISSED', 'Dismissed'),
    ], default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(blank=True, null=True)


class Achievement(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    icon = models.ImageField(upload_to='achievements', blank=True, null=True)
    criteria = models.TextField()
    is_active = models.BooleanField(default=True)


class UserAchievement(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_achievements'
    )
    achievement = models.ForeignKey(
        Achievement, on_delete=models.CASCADE, related_name='earned_by'
    )
    earned_at = models.DateTimeField(auto_now_add=True)
