from django.test import TestCase

from .models import Drink, IngredientNeeded, IngredientStorage


class DrinkModelTest(TestCase):
    def setUp(self):
        malibu = Drink.objects.create(
            name="Malibu",
            complicated=Drink.ComplicatedLevels.EASY,
            preparation_description="Przepis na drinka Easy",
            type=Drink.Types.ALCOHOLIC,
            price=20,
        )

        rum = IngredientStorage.objects.create(
            name="Rum",
            type=IngredientStorage.Types.LIQUID,
            unit=IngredientStorage.Units.MILLILITER,
            storage_amount=2500,
        )

        coconut_milk = IngredientStorage.objects.create(
            name="Mleko Kokosowe",
            type=IngredientStorage.Types.LIQUID,
            unit=IngredientStorage.Units.MILLILITER,
            storage_amount=3000,
        )

        IngredientNeeded.objects.create(
            drink=malibu,
            storage_ingredient=rum,
            amount=50,
        )

        IngredientNeeded.objects.create(
            drink=malibu,
            storage_ingredient=coconut_milk,
            amount=120,
        )

    def test_update_drink_possible_status1(self):
        malibu = Drink.objects.get(name="Malibu")
        self.assertEqual(
            malibu.check_if_is_possible_to_make_and_update_status(),
            malibu.is_possible_to_make,
        )

    def test_update_drink_possible_status2(self):
        malibu = Drink.objects.get(name="Malibu")

        coconut_milk = IngredientStorage.objects.get(name="Mleko Kokosowe")
        coconut_milk.storage_amount = 110
        coconut_milk.save()
        self.assertFalse(
            malibu.check_if_is_possible_to_make_and_update_status(),
            malibu.is_possible_to_make,
        )

    def test_update_drink_possible_status3(self):
        malibu = Drink.objects.get(name="Malibu")

        coconut_milk = IngredientStorage.objects.get(name="Mleko Kokosowe")
        coconut_milk.storage_amount = 120
        coconut_milk.save()
        self.assertTrue(
            malibu.check_if_is_possible_to_make_and_update_status(),
            malibu.is_possible_to_make,
        )

    def test_update_drink_possible_status4(self):
        malibu = Drink.objects.get(name="Malibu")

        coconut_milk = IngredientStorage.objects.get(name="Mleko Kokosowe")
        coconut_milk.storage_amount = 0
        coconut_milk.save()
        self.assertFalse(
            malibu.check_if_is_possible_to_make_and_update_status(),
            malibu.is_possible_to_make,
        )

    def test_update_drink_possible_status5(self):
        malibu = Drink.objects.get(name="Malibu")

        coconut_milk = IngredientStorage.objects.get(name="Mleko Kokosowe")
        coconut_milk.storage_amount = 119
        coconut_milk.save()
        self.assertFalse(
            malibu.check_if_is_possible_to_make_and_update_status(),
            malibu.is_possible_to_make,
        )

    def test_make_a_drink1(self):
        malibu = Drink.objects.get(name="Malibu")
        coconut_milk = IngredientStorage.objects.get(name="Mleko Kokosowe")
        coconut_milk.storage_amount = 120
        coconut_milk.save()
        malibu.make_a_drink()
        self.assertTrue(malibu.is_possible_to_make)

    def test_make_a_drink2(self):
        malibu = Drink.objects.get(name="Malibu")
        coconut_milk = IngredientStorage.objects.get(name="Mleko Kokosowe")
        coconut_milk.storage_amount = 1000
        coconut_milk.save()
        malibu.make_a_drink()
        self.assertTrue(malibu.is_possible_to_make)

    def test_make_a_drink3(self):
        malibu = Drink.objects.get(name="Malibu")
        coconut_milk = IngredientStorage.objects.get(name="Mleko Kokosowe")
        coconut_milk.storage_amount = 119
        coconut_milk.save()
        malibu.make_a_drink()
        self.assertFalse(malibu.is_possible_to_make)
