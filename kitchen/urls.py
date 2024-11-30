from django.urls import path

from kitchen.views import (
    CookCreateView,
    CookDeleteView,
    CookDetailView,
    CookListView,
    CookUpdateExperienceView,
    DishCreateView,
    DishDeleteView,
    DishDetailView,
    DishListView,
    DishTypeBulkCreateView,
    DishTypeDeleteView,
    DishTypeListView,
    DishTypeUpdateView,
    DishUpdateView,
    index,
    IngredientBulkCreateView,
    IngredientDeleteView,
    IngredientListView,
    IngredientUpdateView,
)

app_name = "kitchen"


urlpatterns = [
    path("", index, name="index"),
    # Cook URLs
    path(
        "cooks/",
        CookListView.as_view(),
        name="cook-list",
    ),
    path(
        "cooks/create/",
        CookCreateView.as_view(),
        name="cook-create",
    ),
    path(
        "cooks/<int:pk>/",
        CookDetailView.as_view(),
        name="cook-detail",
    ),
    path(
        "cooks/<int:pk>/update/",
        CookUpdateExperienceView.as_view(),
        name="cook-update",
    ),
    path(
        "cooks/<int:pk>/delete/",
        CookDeleteView.as_view(),
        name="cook-delete",
    ),
    # Dish URLs
    path(
        "dishes/",
        DishListView.as_view(),
        name="dish-list",
    ),
    path(
        "dishes/create",
        DishCreateView.as_view(),
        name="dish-create",
    ),
    path(
        "dishes/<int:pk>",
        DishDetailView.as_view(),
        name="dish-detail",
    ),
    path(
        "dishes/<int:pk>/update/",
        DishUpdateView.as_view(),
        name="dish-update",
    ),
    path(
        "dishes/<int:pk>/delete/",
        DishDeleteView.as_view(),
        name="dish-delete",
    ),
    # DishType URLs
    path(
        "dish-types/",
        DishTypeListView.as_view(),
        name="dish-type-list",
    ),
    path(
        "dish-types/bulk-create/",
        DishTypeBulkCreateView.as_view(),
        name="dish-type-bulk-create",
    ),
    path(
        "dish-types/<int:pk>/update/",
        DishTypeUpdateView.as_view(),
        name="dish-type-update",
    ),
    path(
        "dish-types/<int:pk>/delete/",
        DishTypeDeleteView.as_view(),
        name="dish-type-delete",
    ),
    # Ingredient URLs
    path(
        "ingredients/",
        IngredientListView.as_view(),
        name="ingredient-list",
    ),
    path(
        "ingredients/bulk-create/",
        IngredientBulkCreateView.as_view(),
        name="ingredient-bulk-create",
    ),
    path(
        "ingredients/<int:pk>/update/",
        IngredientUpdateView.as_view(),
        name="ingredient-update",
    ),
    path(
        "ingredients/<int:pk>/delete/",
        IngredientDeleteView.as_view(),
        name="ingredient-delete",
    ),
]
