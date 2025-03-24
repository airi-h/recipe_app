from django.db import models
from django.conf import settings
from users.models import CustomUser
from django.contrib.auth.models import User

class Recipe(models.Model):
    recipe_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, verbose_name='タイトル')
    image = models.ImageField(upload_to='recipe_images/', blank=True, null=True)
    instructions = models.TextField(verbose_name='作り方', blank=True, null=True)
    ingredients = models.TextField(verbose_name='材料', null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Review(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    comment = models.TextField(verbose_name='コメント')
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.PositiveIntegerField(verbose_name='評価', default=3, choices=[(i, i) for i in range(1, 6)])

    def __str__(self):
        return f'{self.user.user_name}のレビュー: {self.recipe.title}'


class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
            unique_together =('user', 'recipe')
        

    def __str__(self):
        return f'{self.user.username}お気に入り{self.recipe.title}'
    
class History(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}が{self.recipe.title}を閲覧({self.viewed_at})'
    

