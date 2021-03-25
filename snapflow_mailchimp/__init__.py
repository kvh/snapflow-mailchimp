from typing import TypeVar
from snapflow import SnapflowModule


# Schemas (for type hinting in python)
MailchimpMember = TypeVar("MailchimpMember")


module = SnapflowModule(
    "mailchimp",
    py_module_path=__file__,
    py_module_name=__name__,
    schemas=["schemas/mailchimp_audience.yml"],
    snaps=[],
)
module.export()
