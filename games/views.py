from django.shortcuts import render, get_object_or_404
from .models import Game, Category

# Главная страница
def main_page(request):
    latest_games = Game.objects.order_by('-created_at')[:3]
    return render(request, 'games/main_page.html', {'games': latest_games})

# Универсальная вьюшка для каталога и категорий.
# Поддерживает фильтрацию по категории, поиск и сортировку.
def catalog(request, category_slug=None):
    categories = Category.objects.all()
    games = Game.objects.all()
    category = None

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        games = games.filter(category=category)

    # Поиск по названию
    query = request.GET.get('q', '').strip()
    if query:
        games = games.filter(title__icontains=query)

    # Сортировка
    sort = request.GET.get('sort', '')
    if sort == 'price_asc':
        games = games.order_by('price')
    elif sort == 'price_desc':
        games = games.order_by('-price')
    elif sort == 'newest':
        games = games.order_by('-created_at')
    else:
        games = games.order_by('title')

    return render(request, 'games/catalog.html', {
        'categories': categories,
        'games': games,
        'category': category,
        'query': query,
        'sort': sort,
    })

# Страница товара
def game_detail(request, game_slug):
    game = get_object_or_404(Game, slug=game_slug)
    return render(request, 'games/game_detail.html', {'game': game})

# Политика конфиденциальности
def privacy(request):
    return render(request, 'games/privacy.html')

