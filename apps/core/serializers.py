from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    whatsapp_link = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'owner', 'title', 'text', 'phone', 'whatsapp_link',
                  'category', 'date_created', 'images', 'price']
        read_only_fields = ['id', 'owner', 'date_created']

    def get_whatsapp_link(self, obj):
        return f"https://wa.me/{obj.phone}"