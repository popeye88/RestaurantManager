from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import generic

from kitchen.forms import (
    CookCreationForm,
    DishCreationForm,
    DishTypeFormSet,
    IngredientFormSet,
    SearchForm,
)
from kitchen.models import Cook, Dish, DishType, Ingredient


@login_required
def index(request):
    num_cooks = Cook.objects.count()
    num_dishes = Dish.objects.count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_cooks": num_cooks,
        "num_dishes": num_dishes,
        "num_visits": num_visits + 1,
    }

    return render(request, "kitchen/index.html", context=context)


class CookListView(LoginRequiredMixin, generic.ListView):
    model = Cook
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Cook List"
        context["create_path"] = "kitchen:cook-create"
        context["create_button"] = "Register new cook"
        context["search_form"] = SearchForm(
            self.request.GET,
            placeholder="Search by username",
        )
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get("search", "")
        if search_query:
            queryset = queryset.filter(username__icontains=search_query)
        # Prefetch dishes if they are used in the template
        return queryset.prefetch_related("dishes")


class CookCreateView(LoginRequiredMixin, generic.CreateView):
    model = Cook
    form_class = CookCreationForm
    template_name = "kitchen/cook_form.html"
    success_url = reverse_lazy("kitchen:cook-list")


class CookDetailView(LoginRequiredMixin, generic.DetailView):
    model = Cook
    template_name = "kitchen/cook_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cook"] = self.object
        context["control"] = True
        context["title"] = "Username: " + self.object.username
        context["delete_path"] = "kitchen:cook-delete"
        context["update_path"] = "kitchen:cook-update"
        context["pk"] = self.object.pk
        return context

    def get_queryset(self):
        # Prefetch dishes and within them, prefetch dish types
        return super().get_queryset().prefetch_related("dishes__dish_type")


class CookUpdateExperienceView(LoginRequiredMixin, generic.UpdateView):
    model = Cook
    fields = ["years_of_experience"]
    template_name = "kitchen/cook_form.html"

    def get_success_url(self):
        return reverse_lazy(
            "kitchen:cook-detail", kwargs={"pk": self.object.pk}
        )


class CookDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Cook
    success_url = reverse_lazy("kitchen:cook-list")


class DishListView(LoginRequiredMixin, generic.ListView):
    model = Dish
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Dish List"
        context["create_path"] = "kitchen:dish-create"
        context["create_button"] = "Add new dish"
        context["search_form"] = SearchForm(
            self.request.GET,
            placeholder="Search by dish name",
        )
        return context

    def get_queryset(self):
        queryset = (
            super()
            .get_queryset()
            .select_related("dish_type")
            .prefetch_related("cooks")
        )
        search_query = self.request.GET.get("search", "")
        if search_query:
            queryset = queryset.filter(name__icontains=search_query)
        return queryset


class DishCreateView(LoginRequiredMixin, generic.CreateView):
    model = Dish
    form_class = DishCreationForm
    template_name = "kitchen/dish_form.html"
    success_url = reverse_lazy("kitchen:dish-list")


class DishDetailView(LoginRequiredMixin, generic.DetailView):
    model = Dish
    template_name = "kitchen/dish_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["dish"] = self.object
        context["control"] = True
        context["title"] = "Dish: " + self.object.name
        context["delete_path"] = "kitchen:dish-delete"
        context["update_path"] = "kitchen:dish-update"
        context["pk"] = self.object.pk
        return context

    def get_queryset(self):
        # Use select_related for dish_type and prefetch cooks and ingredients
        return (
            super()
            .get_queryset()
            .select_related("dish_type")
            .prefetch_related("cooks", "ingredients")
        )


class DishUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Dish
    form_class = DishCreationForm
    template_name = "kitchen/dish_form.html"

    def get_success_url(self):
        return reverse_lazy(
            "kitchen:dish-detail", kwargs={"pk": self.object.pk}
        )


class DishDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Dish
    success_url = reverse_lazy("kitchen:dish-list")
    template_name = "kitchen/dish_confirm_delete.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cancel_url"] = reverse_lazy("kitchen:dish-list")
        return context


class DishTypeListView(LoginRequiredMixin, generic.ListView):
    model = DishType
    template_name = "kitchen/dish_type_list.html"
    context_object_name = "dish_type_list"
    paginate_by = 10

    def get_queryset(self):
        return super().get_queryset().prefetch_related("dishes")


class DishTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = DishType
    fields = ["name"]
    template_name = "kitchen/dish_type_form.html"
    success_url = reverse_lazy("kitchen:dish-type-list")


class DishTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = DishType
    fields = ["name"]
    template_name = "kitchen/dish_type_form.html"
    success_url = reverse_lazy("kitchen:dish-type-list")


class DishTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = DishType
    template_name = "kitchen/dish_type_confirm_delete.html"
    success_url = reverse_lazy("kitchen:dish-type-list")


class IngredientListView(LoginRequiredMixin, generic.ListView):
    model = Ingredient
    template_name = "kitchen/ingredient_list.html"
    context_object_name = "ingredient_list"
    paginate_by = 15

    def get_queryset(self):
        # Prefetch dishes and their dish types
        return super().get_queryset().prefetch_related("dishes__dish_type")


class IngredientBulkCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = "kitchen/ingredient_bulk_create.html"
    formset_class = IngredientFormSet
    success_url = "kitchen:ingredient-list"

    def get(self, request, *args, **kwargs):
        formset = self.formset_class(queryset=Ingredient.objects.none())
        return render(request, self.template_name, {"formset": formset})

    def post(self, request, *args, **kwargs):
        formset = self.formset_class(
            request.POST, queryset=Ingredient.objects.none()
        )
        if formset.is_valid():
            formset.save()
            return redirect(self.success_url)
        return render(request, self.template_name, {"formset": formset})


class DishTypeBulkCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = "kitchen/dish_type_bulk_create.html"
    formset_class = DishTypeFormSet
    success_url = "kitchen:dish-type-list"

    def get(self, request, *args, **kwargs):
        formset = self.formset_class(queryset=DishType.objects.none())
        return render(request, self.template_name, {"formset": formset})

    def post(self, request, *args, **kwargs):
        formset = self.formset_class(
            request.POST, queryset=DishType.objects.none()
        )
        if formset.is_valid():
            formset.save()
            return redirect(self.success_url)
        return render(request, self.template_name, {"formset": formset})


class IngredientUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Ingredient
    fields = ["name"]
    template_name = "kitchen/ingredient_form.html"
    success_url = reverse_lazy("kitchen:ingredient-list")


class IngredientDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Ingredient
    template_name = "kitchen/ingredient_confirm_delete.html"
    success_url = reverse_lazy("kitchen:ingredient-list")
