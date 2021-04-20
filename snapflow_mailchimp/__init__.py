from typing import TypeVar
from snapflow import SnapflowModule
from snapflow_mailchimp.functions.export_audience import export_audience

# Schemas (for type hinting in python)
MailchimpMember = TypeVar("MailchimpMember")


module = SnapflowModule(
    "mailchimp",
    py_module_path=__file__,
    py_module_name=__name__,
)
module.add_function(export_audience)
