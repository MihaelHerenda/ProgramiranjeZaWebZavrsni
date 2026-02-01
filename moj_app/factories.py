import factory
from django.contrib.auth.models import User
from .models import Post, Comment, Like
from factory.django import DjangoModelFactory


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
    
    username = factory.Faker('user_name')
    email = factory.Faker('email')
    password = factory.PostGenerationMethodCall('set_password', 'pass123')


class PostFactory(DjangoModelFactory):
    class Meta:
        model = Post
    
    title = factory.Faker('sentence', nb_words=4)
    content = factory.Faker('paragraph', nb_sentences=5)
    author = factory.SubFactory(UserFactory)


class CommentFactory(DjangoModelFactory):
    class Meta:
        model = Comment
    
    post = factory.SubFactory(PostFactory)
    author = factory.SubFactory(UserFactory)
    content = factory.Faker('sentence', nb_words=10)


class LikeFactory(DjangoModelFactory):
    class Meta:
        model = Like
        django_get_or_create = ('user', 'post')

    post = factory.SubFactory(PostFactory)
    user = factory.SubFactory(UserFactory)