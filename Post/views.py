from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer

# Create your views here.
class PostListCreateAPIView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class PostRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class CommentListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_id = self.kwargs['post_pk']
        return Comment.objects.filter(post_id=post_id)

    def perform_create(self, serializer):
        post_id = self.kwargs['post_pk']
        post = Post.objects.get(pk=post_id)
        serializer.save(author=self.request.user, post=post)

class CommentRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

@api_view(['GET'])
def get_post_comments(request, post_pk):
    
    try:
        post = Post.objects.get(pk=post_pk)
        comments = Comment.objects.filter(post=post)
        serializer = CommentSerializer(comments, many=True, context={'request': request})
        return Response(serializer.data)
    except Post.DoesNotExist:
        return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def create_comment(request, post_pk):

    try:
        post = Post.objects.get(pk=post_pk)
        data = request.data.copy()
        data['post'] = post_pk

        serializer = CommentSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save(author=request.user, post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Post.DoesNotExist:
        return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

