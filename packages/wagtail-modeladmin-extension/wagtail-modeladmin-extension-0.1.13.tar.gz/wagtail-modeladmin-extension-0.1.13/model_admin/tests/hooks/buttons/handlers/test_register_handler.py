from unittest.mock import patch

from django.test import TestCase

from model_admin.hooks.buttons.handlers.base import FieldHandler, SlugFieldHandler, RegisterHandlers
from model_admin.tests.hooks.buttons.test_base.mocks import MockedModel


class TestRegisterHandler(TestCase):

    def setUp(self) -> None:
        self.obj = MockedModel(
            id="c2a1ff40-c821-4cf0-9189-054cdd80f1f8",
            title="TITULO AQUI",
            slug="titulo-aqui",
            another_field="field",
            max_lgt_field="max_lgt_field"
        )

    def test_auto_import_unique_fields(self):
        """Should return all unique fields from django object."""
        rh = RegisterHandlers(obj=self.obj)
        expected = [
            FieldHandler("another_field"),
            FieldHandler("max_lgt_field"),
        ]
        result = rh._import_unique_fields()
        self.assertEqual(result[0].name, expected[0].name)
        self.assertEqual(result[1].name, expected[1].name)

    def test_get_all_fields(self):
        """Should return all fields including the unique fields."""
        self.obj.HANDLER_FIELDS_TO_DUPLICATE = [
            FieldHandler("title"),
        ]

        expected = [
            FieldHandler("another_field"),
            FieldHandler("max_lgt_field"),
            FieldHandler("title"),
        ]
        result = RegisterHandlers(self.obj)._get_fields()
        self.assertEqual(result[0].name, expected[0].name)
        self.assertEqual(result[1].name, expected[1].name)
        self.assertEqual(result[2].name, expected[2].name)

    @patch.object(MockedModel, 'save')
    def test_duplicate_object(self, mocked_model_save):
        """Should call the save method of model"""
        register_handler = RegisterHandlers(obj=self.obj)
        register_handler._duplicate(obj=self.obj)
        self.assertTrue(mocked_model_save.called)

    @patch.object(MockedModel, 'save')
    def test_handle_all_fields(self, mocked_model_save):
        """Should handle registered fields"""
        self.obj.HANDLER_FIELDS_TO_DUPLICATE = [
            FieldHandler("title"),
            SlugFieldHandler("slug"),
        ]

        expected = MockedModel(
            id=None,
            title="COPY TITULO AQUI",
            slug="copy-titulo-aqui",
            another_field="COPY field",
            max_lgt_field="COPY max_l"
        )
        register_handler = RegisterHandlers(obj=self.obj)
        result = register_handler.handle()

        self.assertEqual(expected.title, result.title)
        self.assertEqual(expected.slug, result.slug)
        self.assertEqual(expected.another_field, result.another_field)
        self.assertEqual(expected.max_lgt_field, result.max_lgt_field)
