"""
Views for the recipe APIs.
"""
from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiParameter,
    OpenApiTypes
)
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Recipe, Tag, Ingredient
from recipe import serializers
from recipe.forms import RecipeForm

from django.views.generic import CreateView, DetailView, ListView, UpdateView, View
from django.db.models import Count, Q
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import redirect, render


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                'tags',
                OpenApiTypes.STR,
                description='Comma separated list of IDs to filter'
            ),
            OpenApiParameter(
                'ingredients',
                OpenApiTypes.STR,
                description='Comma separated list of ingredient IDs to filter'
            )
        ]
    )
)

class RecipeViewSet(viewsets.ModelViewSet):
    """View for manage recipe APIs."""
    serializer_class = serializers.RecipeDetailSerializer
    queryset = Recipe.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def _params_to_ints(self, qs):
        """Convert a list of strings to integers."""
        return [int(str_id) for str_id in qs.split(',')]

    def get_queryset(self):
        """Retrieve recipes for authenticated user."""
        tags = self.request.query_params.get('tags')
        ingredients = self.request.query_params.get('ingredients')
        queryset = self.queryset
        if tags:
            tag_ids = self._params_to_ints(tags)
            queryset = queryset.filter(tags__id__in=tag_ids)
        if ingredients:
            ingredient_ids = self._params_to_ints(ingredients)
            queryset = queryset.filter(ingredients__id__in=ingredient_ids)

        return queryset.filter(
            user=self.request.user
        ).order_by('-id').distinct()

    
    def get_serializer_class(self):
        """Return the serializer for request."""
        if self.action == 'list':
            return serializers.RecipeSerializer
        elif self.action == 'upload_image':
            return serializers.RecipeImageSerializer
        
        return self.serializer_class
    
    def perform_create(self, serializer):
        """Create a new recipe."""
        serializer.save(user=self.request.user)

    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """Upload an image to a recipe."""
        recipe = self.get_object()
        serializer = self.get_serializer(recipe, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                'assigned_only',
                OpenApiTypes.INT, enum=[0, 1],
                description='Filter by items assigned to recipes.'
            )
        ]
    )
)
class BaseRecipeAttrViewSet(mixins.DestroyModelMixin,
                            mixins.UpdateModelMixin, 
                            mixins.ListModelMixin, 
                            viewsets.GenericViewSet):
    """Base viewsets for recipe attributes."""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter queryset to authenticated user."""
        assigned_only = bool(
            int(self.request.query_params.get('assigned_only', 0))
        )
        queryset = self.queryset
        if assigned_only:
            queryset = queryset.filter(recipe__isnull=False)

        return queryset.filter(
            user=self.request.user
        ).order_by('-name').distinct()


class TagViewSet(BaseRecipeAttrViewSet):
    """Manage tags in the database."""
    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()
    
    
class IngredientViewSet(BaseRecipeAttrViewSet):
    """Manage ingredients in the database."""
    serializer_class = serializers.IngredientSerializer
    queryset = Ingredient.objects.all()


#################################################################################################
################################  Views for frontend  ###########################################


class RecipeListView(ListView):
    model = Recipe
    ordering = "-title"
    context_object_name = "recipes"
    template_name = "recipe/recipes.html"
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ingredients"] = Ingredient.objects.annotate(
            recipe_count=Count("recipe")
        ).order_by("-recipe_count")[:5]
        return context
    

class RecipeDetailView(DetailView):
    model = Recipe
    context_object_name = "recipe"
    pk_url_kwarg = "recipe_pk"
    template_name = "recipe/detail.html"


@method_decorator(login_required, name="dispatch")
class RecipeUpdateView(UpdateView):
    model = Recipe
    form_class = RecipeForm
    template_name = "recipe/edit_recipe.html"
    pk_url_kwarg = "recipe_pk"
    context_object_name = "recipe"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)

    def form_valid(self, form):
        recipe = form.save(commit=False)
        recipe.save()
        form.save_m2m()
        return redirect("detail", recipe_pk=recipe.pk)
  

@method_decorator(login_required, name="dispatch")
class ShareView(CreateView):
    model = Recipe
    form_class = RecipeForm
    success_url = reverse_lazy("home")
    context_object_name = "share_recipe"
    template_name = "recipe/share.html"

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)
    

class SearchView(RecipeListView):
    model = Recipe
    context_object_name = "search_recipes"
    template_name = "recipe/recipes.html"

    def get_queryset(self):
        search = self.request.GET.get("search")
        if search:
            search = search.replace(",", " ").split()  # Fjerner komma, og lager en liste med søkeordene
            
            query = Q()
            for keyword in search:
                query |= Q(title__icontains=keyword)
                query |= Q(tags__name__icontains=keyword)
                query |= Q(ingredients__name__icontains=keyword) # |= legger hvert element inn i Q objektet med en OR operator.
            print(query)

            obj_list = (
                self.model.objects.filter(query).order_by("-title").distinct()
            )
            print(obj_list)
        else:
            obj_list = self.model.objects.all().order_by("-title")
        return obj_list

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_item(request):
    item_type = request.data.get('type')
    value = request.data.get('value')

    if not value:
        return Response({'message': 'Legg til her'}, status=status.HTTP_400_BAD_REQUEST)

    if item_type == 'ingredient':
        Ingredient.objects.create(name=value, user=request.user)
    elif item_type == 'tag':
        Tag.objects.create(name=value, user=request.user)
    else:
        return Response({'message': 'Ikke gyldig'}, status=status.HTTP_400_BAD_REQUEST)

    return Response({'message': 'Lagt til'}, status=status.HTTP_201_CREATED)


def swagger_view(request):
    return render(request, 'recipe/swagger.html')