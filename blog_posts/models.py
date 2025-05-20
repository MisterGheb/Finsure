from django.db import models

class BlogPost (models.Model):

    class Categories(models.TextChoices):
        TECHNOLOGY = 'Technology', 'Technology'
        BUSINESS_FINANCE = 'Business & Finance', 'Business & Finance'
        HEALTH_WELLNESS = 'Health & Wellness', 'Health & Wellness'
        ENTERTAINMENT = 'Entertainment', 'Entertainment'
        LIFESTYLE = 'Lifestyle', 'Lifestyle'
        EDUCATION = 'Education', 'Education'
        SPORTS = 'Sports', 'Sports'
        POLITICS_CURRENT_AFFAIRS = 'Politics & Current Affairs', 'Politics & Current Affairs'
        SCIENCE = 'Science', 'Science'
        FOOD_COOKING = 'Food & Cooking', 'Food & Cooking'
        OTHER = 'Other', 'Other'

    title = models.CharField(max_length=200)
    content = models.TextField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.CharField(max_length=100,blank=True)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    category = models.CharField(max_length=100, choices=Categories.choices, default=Categories.OTHER)

    def __str__(self):
        return self.title
    

class Comment(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.CharField(max_length=100)

    def __str__(self):
        return f"Comment by {self.author} on {self.post.title}"
    
    