from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Post, Comment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = '__all__'

    def get_comments(self, obj):
        comments = obj.comments.all()
        return CommentSerializer(comments, many=True).data


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'content', 'created_at', 'updated_at']
        read_only_fields = ['author', 'created_at', 'updated_at']

    def create(self, validated_data):
        request = self.context.get('request')
        if request:
            validated_data['author'] = request.user
        return super().create(validated_data)
        
        