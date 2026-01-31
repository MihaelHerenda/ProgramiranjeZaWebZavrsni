from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name="Naslov")
    content = models.TextField(verbose_name="Sadržaj")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def total_likes(self):
        return self.likes.count()

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    # Ovdje je ključ: on_delete=models.SET_NULL čuva komentar čak i ako se autor obriše
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    content = models.TextField(verbose_name="Komentar")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at'] # Najnoviji komentari prvi

    def __str__(self):
        return f"Komentar na {self.post.title}"

    # Ovo koristiš u HTML-u kao {{ comment.display_author }}
    @property
    def display_author(self):
        if self.author:
            return self.author.username
        return "Obrisani korisnik"

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Ovo sprječava da isti korisnik lajka isti post više puta
        unique_together = ('user', 'post')

    def __str__(self):
        return f"{self.user.username} likes {self.post.title}"