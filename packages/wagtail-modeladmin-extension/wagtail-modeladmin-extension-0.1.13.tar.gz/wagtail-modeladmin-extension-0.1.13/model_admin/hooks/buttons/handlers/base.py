import abc
from abc import ABC
from typing import Type, List, Union
from django.db.models import Model
from django.utils.text import slugify


class IFieldHandler(ABC):
    """
    Base handler class

    Args:
        obj (Model): A django model, where we need to extract the field
        field (str): the field name that we want take the value
        prefix (str): the prefix that will be concatenated to the field. COPY is default
        suffix (str): a suffix that will be concatenated after the text of field. Empty is default
    """
    @abc.abstractmethod
    def __init__(self, *args, **kwargs) -> None:
        pass

    @abc.abstractmethod
    def _get_field_from_obj(self) -> str:
        pass

    @abc.abstractmethod
    def _concatenate_prefix_and_suffix_to_value(self) -> str:
        pass

    @abc.abstractmethod
    def _pre_handle(self) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def handle(self, obj: Model) -> str:
        raise NotImplementedError


class FieldHandler(IFieldHandler):

    def __init__(self, field, prefix="COPY ", suffix=""):
        self.obj = None
        self.name = field
        self.prefix = prefix
        self.suffix = suffix

    def _get_max_length(self) -> Union[int, None]:
        """Return text according to the max_length defined in Django field

        Args:
            obj (Model): A Django model
            field (str): The field name that will want to be found

        Returns:
            int: The maximum length of field
            None: If field has no maximum length
        """
        max_length = None
        field = self.obj._meta.get_field(self.name) # noqa
        if hasattr(field, "max_length"):
            max_length = field.max_length

        return max_length

    def _get_field_from_obj(self) -> str:
        field_value = getattr(self.obj, self.name)
        return field_value

    def _concatenate_prefix_and_suffix_to_value(self) -> str:
        formatted_text = "{prefix}{field_value}{suffix}".format(
            prefix=self.prefix,
            field_value=self._get_field_from_obj(),
            suffix=self.suffix
        )
        return formatted_text

    def _pre_handle(self) -> str:
        return self._concatenate_prefix_and_suffix_to_value()

    def handle(self, obj: Model) -> str:
        self.obj = obj
        return self._pre_handle()[0:self._get_max_length()]


class SlugFieldHandler(FieldHandler):
    def _pre_handle(self):
        result_text = super()._pre_handle()
        return slugify(result_text)


class IHandlers(ABC):
    """A class to handle any field registered

    Args:
        obj (Model): A django model, where we need to extract the field
        fields (List[IFieldHandler]): A list of all fields to be handle
        auto_import_unique_fields (bool): If is True, import all unique fields from model object
    """

    @abc.abstractmethod
    def __init__(self,
                 obj: Type[Model],
                 fields: List[IFieldHandler],
                 auto_import_unique_fields: bool = False):
        pass

    def handle(self):
        raise NotImplementedError()


class RegisterHandlers(IHandlers):
    """
    Implementation example:

    HANDLER_FIELDS_TO_DUPLICATE = RegisterHandlers(
        obj=self,
        fields=[
            FieldHandler("title"),
            SlugFieldHandler("slug"),
            FieldHandler("subtitle", prefix="CÓPIA", suffix="Anyshit")
        ],
        auto_import_unique_fields=True
    )
    """

    def __init__(self,
                 obj: Model,
                 auto_import_unique_fields: bool = True):
        self.obj = obj
        self.auto_import_unique_fields = auto_import_unique_fields

    def _import_unique_fields(self) -> List[IFieldHandler]:
        """Auto retrieve all unique fields defined in model

        Returns:
            List[str]: A list with all fields to modify
        """
        fields = []
        for field in self.obj._meta.get_fields():  # noqa
            if hasattr(field, "unique") and field.unique:
                if "id" not in field.name:
                    f = FieldHandler(field.name)
                    fields.append(f)
        return fields

    def _get_fields(self) -> List[IFieldHandler]:
        """Get all fields to concatenate the text COPY.

        Args:
            obj (Model): A Django model

        Returns
        """
        fields = self._import_unique_fields() if self.auto_import_unique_fields else []

        if hasattr(self.obj, "HANDLER_FIELDS_TO_DUPLICATE"):
            register_handlers = getattr(self.obj, "HANDLER_FIELDS_TO_DUPLICATE")
            fields = fields + register_handlers
        return fields

    @staticmethod
    def _duplicate(obj):
        obj.pk = None
        obj.save()
        return obj

    def handle(self) -> Model:
        obj = self.obj
        for field in self._get_fields():
            setattr(obj, field.name, field.handle(obj))
        return self._duplicate(obj)


