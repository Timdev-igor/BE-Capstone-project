from rest_framework import serializers
from django.utils import timezone
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ('user', 'created_at', 'updated_at')

     # Custom validation to ensure the due date isin the future.
    def validate_due_date(self, value):
        if value <= timezone.now():
            raise serializers.ValidationError("Due date should be in the future")
        return value
    
    def validate_priority(self, value):
        if value not in dict(Task.PRIORITY_CHOICES):
            raise serializers.ValidationError("Invalid priority choice")
        return value
    
    def validate_status(self, value):
        if value not in dict(Task.STATUS_CHOICES):
            raise serializers.ValidationError("Status must be either 'Complete' or 'incomplete'")
        return value