from django.shortcuts import render

# База данных рецептов
DATA = {
    'omlet': {
        'яйца, шт': 2,
        'молоко, л': 0.1,
        'соль, ч.л.': 0.5,
    },
    'pasta': {
        'макароны, г': 100,
        'сыр, г': 50,
    },
    'buter': {
        'хлеб, ломтик': 1,
        'колбаса, ломтик': 1,
        'сыр, ломтик': 1,
        'помидор, ломтик': 1,
    }
}

def recipe_view(request, dish):
    servings = request.GET.get('servings', 1)  
    try:
        servings = int(servings)  
    except ValueError:
        servings = 1  # Если не число — по умолчанию 1

    recipe = DATA.get(dish)  # Получаем рецепт блюда
    if recipe:
        scaled_recipe = {ingredient: amount * servings for ingredient, amount in recipe.items()}
    else:
        scaled_recipe = None  # Если блюда нет в базе

    context = {'recipe': scaled_recipe}
    return render(request, 'calculator/index.html', context)
