"""
URL mappings for the recipe app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from recipe import views


schema_view = get_schema_view(
    openapi.Info(
        title="Recipe API",
        default_version='v1',
        description="API for Recipes",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,)
)

router = DefaultRouter()
router.register('recipes', views.RecipeViewSet)
router.register('tags', views.TagViewSet)
router.register('ingredients', views.IngredientViewSet)

app_name = 'recipe'

urlpatterns = [
    path('api/', include(router.urls)),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='api_doc'),
    path('share/', views.ShareView.as_view(), name='share'),
    path('<int:recipe_pk>/', views.RecipeDetailView.as_view(), name='detail'),
    path('<int:recipe_pk>/edit/', views.RecipeUpdateView.as_view(), name='edit'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('additem/', views.add_item, name='add_item'),
    path('api-doc/', views.swagger_view, name='custom_swagger')
]