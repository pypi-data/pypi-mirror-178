from django.test import TestCase

from model_admin.hooks.buttons.handlers.base import FieldHandler, SlugFieldHandler
from model_admin.tests.hooks.buttons.test_base.mocks import MockedModel


class TestHandler(TestCase):

    def setUp(self) -> None:
        self.obj = MockedModel(
            title="TITULO AQUI",
            slug="titulo-aqui",
            another_field="field",
            max_lgt_field="max_lgt_field"
        )

    def test_get_field_value_from_object(self):
        """Should return the field value from object"""
        fh = FieldHandler("title")
        fh.obj = self.obj
        result = fh._get_field_from_obj()
        self.assertEqual(result, "TITULO AQUI")

    def test_concatenate_prefix_and_suffix_to_field_value(self):
        """Should return the field value with suffix and prefix"""
        fh = FieldHandler("title", prefix="CÓPIA ", suffix=" QUALQUER")
        fh.obj = self.obj
        result = fh._concatenate_prefix_and_suffix_to_value()
        self.assertEqual(result, "CÓPIA TITULO AQUI QUALQUER")

    def test_return_charfield_concatenated(self):
        """Should return the charfield handled."""
        fh = FieldHandler("title")
        result = fh.handle(self.obj)
        self.assertEqual(result, "COPY TITULO AQUI")

    def test_return_slugfield(self):
        """Should return the SlugField handled."""
        fh = SlugFieldHandler("title", prefix="CÓPIA ", suffix=" DE NOVO")
        result = fh.handle(self.obj)
        self.assertEqual(result, "copia-titulo-aqui-de-novo")

    def test_max_length(self):
        """Should return the text stripped until the max length."""
        fh = SlugFieldHandler("max_lgt_field", prefix="CÓPIA ")
        result = fh.handle(self.obj)
        self.assertEqual(result, "copia-max_")
