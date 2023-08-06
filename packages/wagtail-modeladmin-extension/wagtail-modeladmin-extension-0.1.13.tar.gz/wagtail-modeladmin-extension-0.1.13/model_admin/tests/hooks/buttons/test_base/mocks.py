import uuid
from unittest.mock import Mock

from django.db import models

VIEW_MOCK = Mock(
            model=Mock(
                _meta=Mock(
                    pk=Mock(attname="id"),
                    verbose_name="Helper",
                    verbose_name_plural="Helpers",
                )
            ),
            url_helper=Mock(
                create_url="add.url"
            ),
            permission_helper=Mock()
        )
REQUEST_MOCK = Mock()
PERMISSION_HELPER_MOCK = Mock(
    user_can_delete_obj=Mock(return_value=True)
)
OBJECT_MOCK = Mock(id="UUID_QUALQUER")


class MockedModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField("title", max_length=255)
    slug = models.CharField("slug", max_length=255)
    another_field = models.CharField("Another Field", max_length=255, unique=True)
    max_lgt_field = models.CharField("Max LGT Field", max_length=10, unique=True)

