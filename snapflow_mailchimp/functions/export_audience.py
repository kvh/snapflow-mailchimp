from __future__ import annotations
import traceback

from dataclasses import dataclass
from typing import TYPE_CHECKING

import pandas as pd
from snapflow import DataBlock, Function, FunctionContext
from loguru import logger

from mailchimp_marketing import Client
from mailchimp_marketing.api_client import ApiClientError

if TYPE_CHECKING:
    from snapflow_mailchimp import MailchimpMember


@Function(
    "export_audience", namespace="mailchimp", display_name="Export Mailchimp audience"
)
def export_audience(
    members: DataBlock[MailchimpMember],
    api_key: str,
    server: str,
    list_id: str,
):
    mailchimp = Client()
    mailchimp.set_config(
        {
            "api_key": api_key,
            "server": server,
        }
    )
    member_records = members.as_records()
    for record in member_records:
        member = {
            k: record.get(k)
            for k in ["email_address", "status", "merge_field"]
            if record.get(k) is not None
        }
        if "status" not in member:
            member["status"] = "subscribed"
        try:
            response = mailchimp.lists.add_list_member(list_id, member)
        except ApiClientError as e:
            # TODO: emit bad row? Error? ctx.emit("error", row) or collect and at end ctx.emit("error", error_records)
            logger.error(f"Mailchimp error: {e.text} ({e.status_code})")
