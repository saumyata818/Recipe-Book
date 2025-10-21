import datetime
import calendar

from django_reorder.reorder import reorder

from django.views.generic import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse

from django.db.models import Q

from .models import Meal
from recipes.models import Recipe

import random


class MealPlanner(LoginRequiredMixin, TemplateView):
    """
    View Meal Planner
    """

    template_name = "meal_planner/meal_planner.html"

    def get_context_data(self, **kwargs):
        today = datetime.date.today()
        days_in_mon = calendar.monthrange(today.year, today.month)[1]

        days = [
            datetime.date(today.year, today.month, day)
            for day in range(1, days_in_mon + 1)
        ]

        meals = Meal.objects.filter(
            user=self.request.user, meal_date__in=days
        ).order_by(reorder(meal_type=["breakfast", "lunch", "dinner"]))

        context = {"days": days, "meals": meals}

        return context


class GetMeal(TemplateView):
    """
    Class to handle getting a random meal based on
    search queries or empty input
    """

    template_name = "meal_planner/create_meal.html"

    def get_context_data(self, **kwargs):
        """
        Get calories and query from the form
        """
        calories = self.request.GET.get("calories")
        query = self.request.GET.get("search")

        if query:
            if not calories:
                calories = 9999

            calories = int(calories)

            recipes = Recipe.objects.filter(
                Q(description__icontains=query)
                | Q(title__icontains=query)
                | Q(ingredients__icontains=query)
                | Q(cuisine_types__icontains=query)
                | Q(instructions__icontains=query)
                & Q(calories__lte=calories)
                & Q(meal_type=kwargs["meal_type"])
            )

        elif calories:
            recipes = Recipe.objects.filter(
                calories__lte=calories, meal_type=kwargs["meal_type"]
            )

        else:
            if len(Recipe.objects.all()) < 1:
                recipes = []
            else:
                recipes = Recipe.objects.filter(meal_type=kwargs["meal_type"])

        if len(recipes) > 0:
            recipe = random.choice(recipes)
            context = {
                "meal_date": kwargs["meal_date"],
                "meal_type": kwargs["meal_type"],
                "recipe": recipe,
            }

        else:
            context = {
                "meal_date": kwargs["meal_date"],
                "meal_type": kwargs["meal_type"],
            }
        return context


class AddMeal(View):
    """Post the form back"""

    def post(self, *args, **kwargs):
        pk = kwargs["pk"]
        recipe = Recipe.objects.get(pk=pk)
        meal_date = kwargs["meal_date"]
        meal_type = kwargs["meal_type"]

        meal, created = Meal.objects.update_or_create(
            meal_date=meal_date,
            meal_type=meal_type,
            defaults={
                "user": self.request.user,
                "recipe": recipe,
                "meal_date": meal_date,
            },
        )

        return HttpResponseRedirect(reverse("meal_planner"))
