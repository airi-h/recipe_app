from django.urls import path
from . import views  # viewsを直接インポート
from .views import RecipeCreateView

app_name = 'recipes'

urlpatterns = [
    path('', views.recipe_list, name='recipe_list'), # レシピ一覧
    path('create/', views.recipe_create, name='recipe_create'),  # レシピ作成
    path('<int:pk>/edit/', views.recipe_edit, name='recipe_edit'),
    path('<int:pk>/delete/', views.recipe_delete, name='recipe_delete'),
    path('search/', views.recipe_search, name='recipe_search'),
    path('favorites/', views.favorite_list, name='favorite_list'),
    path('<int:pk>/favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('<int:pk>/', views.recipe_detail, name='recipe_detail'), # レシピ詳細
    path('history/', views.history_list, name='history_list'),
    path('<int:pk>/review/add/', views.add_review, name='add_review'),
    path('recipes/<int:recipe_id>/review/<int:review_id>/delete/', views.review_delete, name='review_delete'),

]
