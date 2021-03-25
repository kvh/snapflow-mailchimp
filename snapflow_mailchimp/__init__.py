from typing import TypeVar
from snapflow import SnapflowModule
from snapflow_mailchimp.snaps import export_audience

# Schemas (for type hinting in python)
MailchimpMember = TypeVar("MailchimpMember")


module = SnapflowModule(
    "mailchimp",
    py_module_path=__file__,
    py_module_name=__name__,
    schemas=["schemas/mailchimp_member.yml"],
    snaps=[export_audience.export_audience],
)
module.export()
