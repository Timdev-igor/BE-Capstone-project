from rest_framework import serializers
from .models import Task
from datetime import datetime

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ('user', 'created_at', 'updated_at')

     # Custom validation to ensure the due date isin the future.
    def validate_due_date(self, value):
        if value is not None and value <= datetime.now():
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
    
    def update(self, instance, validated_data):
        if instance.status  == 'Complete': # Task is marked complete
            raise serializers.ValidationError("Cannot update a completed task.")
        return super().update(instance, validated_data)