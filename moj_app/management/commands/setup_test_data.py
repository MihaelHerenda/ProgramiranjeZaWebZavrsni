import random
from django.db import transaction
from django.core.management.base import BaseCommand
from moj_app.models import Post, Comment, Like, User
from moj_app.factories import UserFactory, PostFactory, CommentFactory, LikeFactory

class Command(BaseCommand):
    help = "Generira testne podatke koristeći Factory Boy"

    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write("Brisanje starih podataka...")
        Like.objects.all().delete()
        Comment.objects.all().delete()
        Post.objects.all().delete()
        User.objects.exclude(is_superuser=True).delete() # Čuvamo admina

        self.stdout.write("Kreiranje novih podataka...")

        
        users = UserFactory.create_batch(10)

        
        for _ in range(30):
            author = random.choice(users)
            post = PostFactory(author=author)

            
            for _ in range(random.randint(0, 5)):
                comment_author = random.choice(users)
                CommentFactory(post=post, author=comment_author)

            
            likers = random.sample(users, random.randint(0, 8))
            for liker in likers:
                LikeFactory(post=post, user=liker)

        self.stdout.write(self.style.SUCCESS("Uspješno generirano: 10 korisnika, 30 postova + komentari i lajkovi!"))