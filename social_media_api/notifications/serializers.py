# notifications/serializers.py
from rest_framework import serializers
from .models import Notification
from django.contrib.contenttypes.models import ContentType

class NotificationSerializer(serializers.ModelSerializer):
    actor = serializers.StringRelatedField()
    target = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = ['id', 'actor', 'verb', 'target', 'unread', 'timestamp']

    def get_target(self, obj):
        if obj.target is None:
            return None
        # Simple representation: model name and id
        return {
            'type': obj.target_content_type.model,
            'id': obj.target_object_id,
            'repr': str(obj.target)
        }
