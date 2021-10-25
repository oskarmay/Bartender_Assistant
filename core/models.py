from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import pgettext_lazy, ugettext_lazy
from django.conf import settings
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Add field to User model"""

    class Role(models.TextChoices):
        BARTENDER = "bt", ugettext_lazy("bartender")
        WAITER = "wt", ugettext_lazy("waiter")
        CUSTOMER = "ct", ugettext_lazy("customer")

    one_use_account_password = models.CharField(
        pgettext_lazy("user", "one-time account password"),
        null=True,
        blank=True,
        max_length=50,
    )

    expire_date = models.DateTimeField(
        pgettext_lazy("user", "expire date"), null=True, blank=True
    )

    role = models.CharField(
        pgettext_lazy("user", "role"),
        max_length=2,
        choices=Role.choices,
        null=True,
        blank=True,
    )

    def is_bartender(self):
        return self.role == self.Role.BARTENDER

    def is_waiter(self):
        return self.role == self.Role.WAITER

    def is_customer(self):
        return self.role == self.Role.CUSTOMER


class Drink(models.Model):
    """Store name of Dring, is it possible to make it information."""

    class ComplicatedLevels(models.TextChoices):
        """Store complicated level of Drink."""

        EASY = "EASY", pgettext_lazy("drink", "easy")
        MEDIUM = "MEDIUM", pgettext_lazy("drink", "medium")
        HARD = "HARD", pgettext_lazy("drink", "hard")

    name = models.CharField(
        max_length=255,
        blank=False,
        unique=True,
        verbose_name=pgettext_lazy("drink", "name"),
    )

    complicated = models.CharField(
        max_length=255,
        choices=ComplicatedLevels.choices,
        blank=False,
        verbose_name=pgettext_lazy("drink", "complicated"),
    )

    price = models.PositiveIntegerField(
        default=0,
        null=False,
        blank=False,
        verbose_name=pgettext_lazy("drink", "price"),
    )

    is_possible_to_make = models.BooleanField(
        default=False,
        verbose_name=pgettext_lazy("drink", "is possible to make"),
    )

    date_creation = models.DateField(
        auto_now_add=True,
        verbose_name=pgettext_lazy("drink", "date created"),
    )

    date_modified = models.DateField(
        auto_now=True,
        verbose_name=pgettext_lazy("drink", "date modified"),
    )

    image = models.FileField(
        verbose_name=pgettext_lazy("drink", "drink image"),
        upload_to=settings.MEDIA_ROOT,
        null=True,
    )

    def make_a_drink(self):
        """Function subtract ingredient use for making drink"""
        ingredient_needed = IngredientNeeded.objects.filter(drink=self)
        for ingredient in ingredient_needed.all():
            ingredient.subtract_ingredient()
        self.drink_is_possible_to_make()

    def drink_is_possible_to_make(self):
        """Function checking if we have enough ingredient in storage to make this drink."""
        related_ingredient = IngredientNeeded.objects.filter(drink=self)
        for ingredient in related_ingredient:
            if not ingredient.is_enough_to_make_drink and self.is_possible_to_make:
                self.is_possible_to_make = False
                self.save()
                break
            elif ingredient.is_enough_to_make_drink and not self.is_possible_to_make:
                self.is_possible_to_make = True
                self.save()

    class Meta:
        verbose_name = pgettext_lazy("drink", "drink")
        verbose_name_plural = pgettext_lazy("drink", "drinks")

    def __str__(self):
        return ugettext_lazy(
            "Drink: {name} | Is possible to make?: {answer} | Complicated: {level} "
        ).format(
            name=self.name,
            answer=ugettext_lazy("yes")
            if self.is_possible_to_make
            else ugettext_lazy("no"),
            level=self.complicated,
        )


class IngredientStorage(models.Model):
    """Store FK for Ingredient model, amount of Ingredient in our storage."""

    class Types(models.TextChoices):
        """Store types of Ingredient."""

        LIQUID = "LIQUID", pgettext_lazy("ingredient_storage", "liquid")
        FRUIT = "FRUIT", pgettext_lazy("ingredient_storage", "fruit")
        VEGETABLE = "VEGETABLE", pgettext_lazy("ingredient_storage", "vegetable")
        SNACK = "SNACK", pgettext_lazy("ingredient_storage", "snack")
        OTHER = "OTHER", pgettext_lazy("ingredient_storage", "other")

    class Units(models.TextChoices):
        """Store unit of Ingredient."""

        MILLILITER = "MILLILITER", pgettext_lazy("ingredient_storage", "milliliter")
        PIECE = "PIECE", pgettext_lazy("ingredient_storage", "piece")

    name = models.CharField(
        max_length=255,
        blank=False,
        verbose_name=pgettext_lazy("ingredient_storage", "name"),
        unique=True,
    )

    type = models.CharField(
        max_length=255,
        choices=Types.choices,
        blank=False,
        verbose_name=pgettext_lazy("ingredient_storage", "type"),
    )

    unit = models.CharField(
        max_length=255,
        choices=Units.choices,
        blank=False,
        verbose_name=pgettext_lazy("ingredient_storage", "unit"),
    )

    image = models.FileField(
        verbose_name=pgettext_lazy("ingredient_storage", "ingredient image"),
        upload_to=settings.MEDIA_ROOT,
        null=True,
    )

    storage_amount = models.DecimalField(
        max_digits=20,
        decimal_places=3,
        blank=False,
        validators=[MinValueValidator(Decimal("0"))],
        verbose_name=pgettext_lazy("ingredient_storage", "amount in storage"),
    )

    def save(self, *args, **kwargs):
        """Modify save logic.
        When user add amount to storage we check if drink related to ingredient is possible to make."""
        related_drinks = Drink.objects.filter(
            ingredient_needed__storage_ingredient=self
        ).prefetch_related("ingredient_needed")

        for drink in related_drinks:
            for ingredient in drink.ingredient_needed.all():
                ingredient.check_if_enough_ingredient()
            drink.drink_is_possible_to_make()

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = pgettext_lazy("ingredient_storage", "ingredient in storage")
        verbose_name_plural = pgettext_lazy(
            "ingredient_storage", "ingredients in storage"
        )

    def __str__(self):
        return ugettext_lazy("{name}: {amount} ({unit})").format(
            name=self.name, amount=self.storage_amount, unit=self.get_unit_display()
        )


class IngredientNeeded(models.Model):
    """Store FK for Ingredient model, amount needed for drink."""

    drink = models.ForeignKey(
        Drink,
        on_delete=models.CASCADE,
        related_name="ingredient_needed",
        verbose_name=pgettext_lazy("ingredient_needed", "drink"),
    )

    storage_ingredient = models.ForeignKey(
        IngredientStorage,
        on_delete=models.CASCADE,
        related_name="ingredient_needed",
        verbose_name=pgettext_lazy("ingredient_needed", "ingredient in storage"),
    )

    amount = models.DecimalField(
        max_digits=20,
        decimal_places=3,
        blank=False,
        validators=[MinValueValidator(Decimal("0"))],
        verbose_name=pgettext_lazy("ingredient_needed", "amount needed"),
    )

    is_enough_to_make_drink = models.BooleanField(default=False)

    def subtract_ingredient(self):
        """Function subtract ingredient amount needed for drink from storage."""
        self.storage_ingredient.storage_amount = (
            self.storage_ingredient.storage_amount - self.amount
        )
        self.storage_ingredient.save()

    def check_if_enough_ingredient(self):
        """Function checking if we have enough amount of this ingredient in storage to make drink."""
        output = True if self.amount < self.storage_ingredient.storage_amount else False
        self.is_enough_to_make_drink = output
        self.save()
        return output

    class Meta:
        verbose_name = pgettext_lazy("ingredient_needed", "ingredient needed")
        verbose_name_plural = pgettext_lazy("ingredient_needed", "ingredients needed")

    def __str__(self):
        return ugettext_lazy("{name}: {amount} ({unit})").format(
            name=self.storage_ingredient.name,
            amount=self.amount,
            unit=self.storage_ingredient.get_unit_display(),
        )


class DrinkQueue(models.Model):
    """Drinking queue for client drink orders."""

    class DrinkQueueStatus(models.TextChoices):
        """Available status for order."""

        CREATED = "CREATED", pgettext_lazy("drink_queue", "created")
        ACCEPTED = "ACCEPTED", pgettext_lazy("drink_queue", "accepted")
        IN_PROGRESS = "IN_PROGRESS", pgettext_lazy("drink_queue", "in progress")
        COMPLETED = "COMPLETED", pgettext_lazy("drink_queue", "completed")
        REJECTED = "REJECTED", pgettext_lazy("drink_queue", "rejected")

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="drink_queue",
        verbose_name=pgettext_lazy("drink_queue", "user"),
    )

    drink = models.ForeignKey(
        Drink,
        on_delete=models.SET_NULL,
        null=True,
        related_name="drink_queue",
        verbose_name=pgettext_lazy("drink_queue", "order"),
    )

    status = models.CharField(
        max_length=255,
        choices=DrinkQueueStatus.choices,
        blank=False,
        verbose_name=pgettext_lazy("drink_queue", "complicated"),
    )

    order_date = models.DateField(
        auto_now_add=True,
        verbose_name=pgettext_lazy("drink_queue", "order date"),
    )

    class Meta:
        verbose_name = pgettext_lazy("drink_queue", "order")
        verbose_name_plural = pgettext_lazy("drink_queue", "orders")

    def __str__(self):
        return ugettext_lazy(
            "User: {username}, Order: {order}, Status: {status}"
        ).format(username=self.user.username, order=self.drink, status=self.status)

    def set_created(self):
        """Set drink in queue status to created."""
        self.status = self.DrinkQueueStatus.CREATED
        self.save()

    def set_accepted(self):
        """Set drink in queue status to accepted."""
        self.status = self.DrinkQueueStatus.ACCEPTED
        self.drink.make_a_drink()
        self.save()

    def set_in_progress(self):
        """Set drink in queue status to in progress."""
        self.status = self.DrinkQueueStatus.IN_PROGRESS
        self.save()

    def set_completed(self):
        """Set drink in queue status to completed."""
        self.status = self.DrinkQueueStatus.COMPLETED
        self.save()

    def set_rejected(self):
        """Set drink in queue status to rejected."""
        self.status = self.DrinkQueueStatus.REJECTED
        self.save()


class Earnings(models.Model):
    sum_date = models.DateField(
        auto_now_add=True,
        verbose_name=pgettext_lazy("earnings", "sum date"),
    )
    sum = models.PositiveIntegerField(
        null=False,
        blank=False,
        verbose_name=pgettext_lazy("earnings", "sum"),
    )
