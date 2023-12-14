"""
URL mappings for the recipe app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from recipe import views


router = DefaultRouter()
router.register('recipes', views.RecipeViewSet)
router.register('tags', views.TagViewSet)
router.register('ingredients', views.IngredientViewSet)

app_name = 'recipe'

urlpatterns = [
    path('api/', include(router.urls)),
    path('share/', views.ShareView.as_view(), name='share'),
    path('<int:recipe_pk>/', views.RecipeDetailView.as_view(), name='detail'),
    path('<int:recipe_pk>/edit/', views.RecipeUpdateView.as_view(), name='edit'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('additem/', views.add_item, name='add_item')
]