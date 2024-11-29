from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from kitchen.forms import CookCreationForm
from kitchen.models import Cook, DishType


class DishTypeModelTest(TestCase):
    def test_str_method(self):
        dish_type = DishType.objects.create(name="Salad")
        self.assertEqual(str(dish_type), "Salad")


class CookModelTest(TestCase):
    def test_str_method(self):
        cook = Cook.objects.create_user(
            username="chef", password="testpass123", years_of_experience=5
        )
        self.assertEqual(str(cook), "chef (5 years of experience)")

    def test_full_name_property(self):
        cook = Cook.objects.create_user(
            username="chef",
            password="testpass123",
            first_name="Gordon",
            last_name="Ramsay",
        )
        self.assertEqual(cook.full_name, "Gordon Ramsay")

    def test_get_absolute_url(self):
        cook = Cook.objects.create_user(
            username="chef",
            password="testpass123",
            first_name="Gordon",
            last_name="Ramsay",
        )
        self.assertEqual(
            cook.get_absolute_url(),
            reverse("kitchen:cook-detail", kwargs={"pk": cook.pk}),
        )


class CookCreationFormTest(TestCase):
    def test_form_valid_data(self):
        form = CookCreationForm(
            data={
                "username": "chef",
                "password1": "strongpassword123",
                "password2": "strongpassword123",
                "first_name": "Gordon",
                "last_name": "Ramsay",
                "years_of_experience": 5,
            }
        )
        self.assertTrue(form.is_valid(), msg=f"Form errors: {form.errors}")

    def test_form_invalid_password_mismatch(self):
        form = CookCreationForm(
            data={
                "username": "chef2",
                "password1": "strongpassword123",
                "password2": "wrongpassword",
                "first_name": "Gordon",
                "last_name": "Ramsay",
                "years_of_experience": 5,
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("password2", form.errors)
        print("Password Mismatch Errors:", form.errors)

    def test_form_invalid_years_of_experience(self):
        form = CookCreationForm(
            data={
                "username": "chef3",
                "password1": "strongpassword123",
                "password2": "strongpassword123",
                "first_name": "Gordon",
                "last_name": "Ramsay",
                "years_of_experience": -1,
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("years_of_experience", form.errors)
        print("Years of Experience Errors:", form.errors)


class DishTypeListViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="user", password="testpass123"
        )
        DishType.objects.create(name="Salad")
        DishType.objects.create(name="Soup")

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse("kitchen:dish-type-list"))
        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('kitchen:dish-type-list')}",
        )

    def test_view_url_exists_at_desired_location(self):
        self.client.login(username="user", password="testpass123")
        response = self.client.get("/dish-types/")
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(username="user", password="testpass123")
        response = self.client.get(reverse("kitchen:dish-type-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "kitchen/dish_type_list.html")

    def test_pagination_is_ten(self):
        self.client.login(username="user", password="testpass123")
        for i in range(10):
            DishType.objects.create(name=f"Type {i}")
        response = self.client.get(reverse("kitchen:dish-type-list"))
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] is True)
        self.assertEqual(len(response.context["dish_type_list"]), 10)
