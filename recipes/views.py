from django.shortcuts import render, redirect, get_object_or_404
from .models import Recipe, Review, Favorite, History
from .forms import RecipeForm,ReviewForm
from .forms import CustomLoguinForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import login
from django.forms import inlineformset_factory



def custom_login_view(request):
   if request.method=="POST":
      form = CustomLoguinForm(data=request.POST)
      if form.is_valid():
         user = form.get_user()
         login(request, user)
         return redirect('home') # ホームページにリダイレクト
   else:
      form = CustomLoguinForm()
      
   return render(request, 'users/login.html', {'form':form})
         


# レシピ一覧
def recipe_list(request):
    recipes = Recipe.objects.all()  # 余計な prefetch_related を削除
    return render(request, 'recipes/recipe_list.html', {'recipes': recipes})

# レシピ投稿
@login_required
def recipe_create(request):
    if request.method == "POST":
        recipe_form = RecipeForm(request.POST, request.FILES)

        if recipe_form.is_valid():
            recipe = recipe_form.save(commit=False)
            recipe.user = request.user

            # `ingredients` フィールドを保存（カンマ区切り）
            ingredients_text = request.POST.get('ingredients', '').strip()
            recipe.ingredients = ingredients_text
            recipe.save()

            messages.success(request, "レシピが投稿されました！")
            return redirect('recipes:recipe_detail', pk=recipe.pk)
        else:
            messages.error(request, "入力に誤りがあります。修正してください。")
    else:
        recipe_form = RecipeForm()

    return render(request, 'recipes/recipe_form.html', {'recipe_form': recipe_form})

       
# レシピ削除
def recipe_delete(request, pk):
   recipe = get_object_or_404(Recipe, pk=pk)
   if request.method == 'POST':
      recipe.delete()
      return redirect('recipes:recipe_list') # 削除後のリダイレクト先
   return render(request, 'recipes/recipe_confirm_delete.html',{'recipe':recipe})

# 検索ビューを追加
def recipe_search(request):
    query = request.GET.get('q')
    results = []

    if query:
        results = Recipe.objects.filter(
            Q(title__icontains=query) |  
            Q(instructions__icontains=query) |  
            Q(ingredients__icontains=query)  
        ).distinct()

    return render(request, 'recipes/recipe_search.html', {'results': results, 'query': query})

@login_required
def toggle_favorite(request, pk):
   recipe = get_object_or_404(Recipe, pk=pk)
   favorite, created = Favorite.objects.get_or_create(user=request.user, recipe=recipe)
   
   if not created:
      favorite.delete()
   return redirect('recipes:recipe_detail', pk=recipe.pk)

@login_required
def favorite_list(request):
   favorites = Favorite.objects.filter(user=request.user).select_related('recipe')
   return render(request, 'recipes/favorite_list.html', {'favorites':favorites})


@login_required   

def history_list(request):
   histories = History.objects.filter(user=request.user).order_by('-viewed_at')
   return render(request, 'recipes/history_list.html',{'histories':histories})
   


def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)

    # カンマ区切りの材料をリストに変換
    ingredients_list = recipe.ingredients.splitlines() if recipe.ingredients else []
   
    reviews = recipe.reviews.all()

    # 閲覧履歴の登録
    if request.user.is_authenticated:
        History.objects.create(user=request.user, recipe=recipe)

    # お気に入り状態の判定
    is_favorite = recipe.favorite_set.filter(user=request.user).exists() if request.user.is_authenticated else False

    # レビュー投稿の処理
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.recipe = recipe
            review.user = request.user
            review.save()
            messages.success(request, "レビューが投稿されました！")
            return redirect('recipes:recipe_detail', pk=recipe.pk)
        else:
            messages.error(request, "レビュー投稿失敗しました。入力内容を確認してください。")
    else:
        form = ReviewForm()

    return render(request, 'recipes/recipe_detail.html', {
        'recipe': recipe,
        'ingredients_list': ingredients_list,  # 修正
        'reviews': reviews,
        'form': form,
        'is_favorite': is_favorite,
    })


# レシピ編集
@login_required
def recipe_edit(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)

    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)

        if form.is_valid():
            recipe = form.save(commit=False)
            
            # `ingredients` フィールドを更新（カンマ区切りの文字列として保存）
            ingredients_text = request.POST.get('ingredients', '').strip()
            recipe.ingredients = ingredients_text
            recipe.save()

            messages.success(request, "レシピが更新されました！")
            return redirect('recipes:recipe_detail', pk=recipe.pk)
        else:
            messages.error(request, "入力に誤りがあります。修正してください。")
    else:
        # `ingredients` をフォームにセットする
        form = RecipeForm(instance=recipe, initial={'ingredients': recipe.ingredients})

    return render(request, 'recipes/recipe_edit.html', {'form': form, 'recipe': recipe})


class RecipeCreateView(CreateView):
   model = Recipe
   template_name = 'recipes/recipe_form.html'
   fields = ['title', 'instructions', 'ingredients', 'image']
   success_url = reverse_lazy('recipes:recipe_list')


@login_required
def add_review(request, pk):
   recipe = get_object_or_404(Recipe, pk=pk)

   if request.method == "POST":
      form = ReviewForm(request.POST)
      if form.is_valid():
         review = form.save(commit=False)
         review.recipe = recipe
         review.user = request.user
         review.save()
         return redirect('recipes:recipe_detail', pk=pk)
   else:
      form = ReviewForm()

   return render(request, 'recipes/add_review.html', {'form':form, 'recipe_id':pk})

@login_required
def review_delete(request, recipe_id, review_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    review = get_object_or_404(Review, pk=review_id, user=request.user)

    if request.method == "POST":
        review.delete()
        messages.success(request, "レビューが削除されました！")
        return redirect('recipes:recipe_detail', pk=recipe_id)

    return render(request, 'recipes/review_confirm_delete.html', {'recipe': recipe, 'review': review})
