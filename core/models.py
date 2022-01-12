import logging
from decimal import Decimal

from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Case, When
from django.utils.translation import pgettext_lazy, ugettext_lazy

logger = logging.getLogger(__name__)


class User(AbstractUser):
    """Modify standard User by adding field."""

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

    customer_table = models.CharField(
        pgettext_lazy("user", "customer table"),
        max_length=10,
        null=True,
        blank=True,
    )

    @property
    def is_bartender(self):
        return self.role == self.Role.BARTENDER

    @property
    def is_waiter(self):
        return self.role == self.Role.WAITER

    @property
    def is_in_staff(self):
        return self.role == self.Role.BARTENDER or self.role == self.Role.WAITER

    @property
    def is_customer(self):
        return self.role == self.Role.CUSTOMER


class Drink(models.Model):
    """Store name of Dring, is it possible to make it information."""

    class ComplicatedLevels(models.TextChoices):
        """Store complicated level of Drink."""

        EASY = "EASY", pgettext_lazy("drink", "easy")
        MEDIUM = "MEDIUM", pgettext_lazy("drink", "medium")
        HARD = "HARD", pgettext_lazy("drink", "hard")

    class Types(models.TextChoices):
        """Store types of Drink."""

        ONE_SHOT = "ONE_SHOT", pgettext_lazy("drink", "one shot")
        MULTIPLE_SHOT = "MULTIPLE_SHOT", pgettext_lazy("drink", "multiple shot")
        ALCOHOLIC = "ALCOHOLIC", pgettext_lazy("drink", "alcoholic")
        NON_ALCOHOLIC = "NON_ALCOHOLIC", pgettext_lazy("drink", "non alcoholic")

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

    preparation_description = models.CharField(
        max_length=1024,
        blank=False,
        null=False,
        verbose_name=pgettext_lazy("drink", "preparation description"),
    )

    type = models.CharField(
        max_length=255,
        choices=Types.choices,
        blank=False,
        verbose_name=pgettext_lazy("drink", "type"),
    )
    amount = models.PositiveIntegerField(
        default=1,
        null=False,
        blank=False,
        verbose_name=pgettext_lazy("drink", "amount"),
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
        upload_to="drinks",
        null=True,
        blank=True,
    )

    def check_if_is_possible_to_make_and_update_status(self):
        """Function with logic changing drink is possible to make status."""

        # Get all ingredient related to drink
        ingredient_needed = IngredientNeeded.objects.filter(drink=self).select_related(
            "storage_ingredient"
        )
        # Creating list for status if we have enough ingredient to make another drink
        ingredient_status_list = []
        for ingredient in ingredient_needed:
            # Update info about ingredient amount in storage and ingredient needed status
            ingredient.storage_ingredient.update_amount_ingredients()
            # Append ingredient needed status to list
            ingredient_status_list.append(ingredient.is_enough_to_make_drink)

        # Check if one of ingredient status was False (not enough to make drink)
        if False in ingredient_status_list:
            # If drink already has status impossible to make we dont need to modify field
            if self.is_possible_to_make:
                self.is_possible_to_make = False
                self.save()
            return False
        elif False not in ingredient_status_list:
            # If drink already has status possible to make we dont need to modify field
            if not self.is_possible_to_make:
                self.is_possible_to_make = True
                self.save()
            return True

    def make_a_drink(self):
        """Function with logic to subtract ingredient change ingredient amount status"""

        # Get all ingredient related to drink
        ingredient_needed = IngredientNeeded.objects.filter(drink=self).select_related(
            "storage_ingredient"
        )
        [ing.if_enough_ingredient_in_storage() for ing in ingredient_needed]
        ingredient_list = [ing.is_enough_to_make_drink for ing in ingredient_needed]
        if False not in ingredient_list:
            for ingredient in ingredient_needed:
                # Subtract ingredient from storage
                ingredient.subtract_ingredient()

        # Check if we have enough ingredient left to make another drink
        self.check_if_is_possible_to_make_and_update_status()

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
        BEER = "BEER", pgettext_lazy("ingredient_storage", "beer")
        FRUIT = "FRUIT", pgettext_lazy("ingredient_storage", "fruit")
        VEGETABLE = "VEGETABLE", pgettext_lazy("ingredient_storage", "vegetable")
        SNACK = "SNACK", pgettext_lazy("ingredient_storage", "snack")
        OTHER = "OTHER", pgettext_lazy("ingredient_storage", "other")

    class Units(models.TextChoices):
        """Store unit of Ingredient."""

        MILLILITER = "MILLILITER", pgettext_lazy("ingredient_storage", "milliliter")
        PIECE = "PIECE", pgettext_lazy("ingredient_storage", "piece")
        PACK = "PACK", pgettext_lazy("ingredient_storage", "pack")

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
        verbose_name=pgettext_lazy("ingredient_storage", "image"),
        upload_to="ingredients",
        null=True,
        blank=True,
    )

    storage_amount = models.DecimalField(
        max_digits=20,
        decimal_places=3,
        blank=False,
        validators=[MinValueValidator(Decimal("0"))],
        verbose_name=pgettext_lazy("ingredient_storage", "amount in storage"),
    )

    price = models.PositiveIntegerField(
        default=0,
        null=False,
        blank=True,
        verbose_name=pgettext_lazy("ingredient_storage", "price"),
    )

    has_alcohol = models.BooleanField(
        blank=False,
        null=False,
        verbose_name=pgettext_lazy("ingredient_storage", "has alcohol"),
    )

    can_be_ordered = models.BooleanField(
        blank=False,
        null=False,
        verbose_name=pgettext_lazy("ingredient_storage", "can be ordered"),
    )

    def update_amount_ingredients(self):
        IngredientNeeded.objects.filter(storage_ingredient=self).update(
            is_enough_to_make_drink=Case(
                When(amount__lte=self.storage_amount, then=True),
                When(amount__gt=self.storage_amount, then=False),
            )
        )

    def save(self, *args, **kwargs):
        self.update_amount_ingredients()
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

    def if_enough_ingredient_in_storage(self):
        return self.amount < self.storage_ingredient.storage_amount

    def subtract_ingredient(self):
        """Function for subtract used ingredient"""
        if self.if_enough_ingredient_in_storage():
            # Calculate new storage amount
            self.storage_ingredient.storage_amount -= self.amount
            self.storage_ingredient.save()
        return self.if_enough_ingredient_in_storage()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.is_enough_to_make_drink = self.if_enough_ingredient_in_storage()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = pgettext_lazy("ingredient_needed", "ingredient needed")
        verbose_name_plural = pgettext_lazy("ingredient_needed", "ingredients needed")

    def __str__(self):
        return ugettext_lazy("{name}: {amount} ({unit})").format(
            name=self.storage_ingredient.name,
            amount=self.amount,
            unit=self.storage_ingredient.get_unit_display(),
        )


class Orders(models.Model):
    """Drinking queue for client drink orders."""

    class OrdersStatus(models.TextChoices):
        """Available status for order."""

        CREATED = "CREATED", pgettext_lazy("drink_queue", "created")
        ACCEPTED = "ACCEPTED", pgettext_lazy("drink_queue", "accepted")
        IN_PROGRESS = "IN_PROGRESS", pgettext_lazy("drink_queue", "in progress")
        COMPLETED = "COMPLETED", pgettext_lazy("drink_queue", "completed")
        REJECTED = "REJECTED", pgettext_lazy("drink_queue", "rejected")
        CANCELED = "CANCELED", pgettext_lazy("drink_queue", "canceled")

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="drink_queue",
        verbose_name=pgettext_lazy("drink_queue", "user"),
    )

    drink = models.ForeignKey(
        Drink,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="drink_queue",
        verbose_name=pgettext_lazy("drink_queue", "order"),
    )

    storage_order = models.ForeignKey(
        IngredientStorage,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="drink_queue",
        verbose_name=pgettext_lazy("drink_queue", "order"),
    )

    status = models.CharField(
        max_length=255,
        choices=OrdersStatus.choices,
        blank=False,
        verbose_name=pgettext_lazy("drink_queue", "complicated"),
    )

    order_date = models.DateTimeField(
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

    @property
    def is_created(self):
        return self.status == Orders.OrdersStatus.CREATED

    @property
    def is_accepted(self):
        return self.status == Orders.OrdersStatus.ACCEPTED

    @property
    def is_in_progress(self):
        return self.status == Orders.OrdersStatus.IN_PROGRESS

    @property
    def is_completed(self):
        return self.status == Orders.OrdersStatus.COMPLETED

    @property
    def is_rejected(self):
        return self.status == Orders.OrdersStatus.REJECTED

    @property
    def is_canceled(self):
        return self.status == Orders.OrdersStatus.CANCELED

    def set_created(self):
        """Set drink in queue status to created."""
        self.status = self.OrdersStatus.CREATED
        self.save()

    def set_accepted(self):
        """Set drink in queue status to accepted."""
        self.status = self.OrdersStatus.ACCEPTED
        # self.drink.make_a_drink()  # TODO Sprawdzic czemu to jest zakomentowane
        self.save()

    def set_in_progress(self):
        """Set drink in queue status to in progress."""
        self.status = self.OrdersStatus.IN_PROGRESS
        self.save()

    def set_completed(self):
        """Set drink in queue status to completed."""
        self.status = self.OrdersStatus.COMPLETED
        self.save()

    def set_rejected(self):
        """Set drink in queue status to rejected."""
        self.status = self.OrdersStatus.REJECTED
        self.save()

    def set_canceled(self):
        """Set drink in queue status to rejected."""
        self.status = self.OrdersStatus.CANCELED
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
