from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Book(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='books')
    name = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    description = models.TextField()
    cover = models.ImageField(upload_to='covers/', null=True, blank=True)

    def __str__(self):
        return self.name
    
    @property
    def avg_rate(self):
        rates = self.reviews.all().values_list('rate', flat=True)
        if rates:
            return round(sum(rates) / len(rates), 2)
        return '-'
    

class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    review_content = models.CharField(max_length=2000)
    rate = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.book.name} - {self.author.username} ({self.rate}/5)"