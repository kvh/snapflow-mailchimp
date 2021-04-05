from __future__ import annotations
import traceback

from dataclasses import dataclass
from typing import TYPE_CHECKING

import pandas as pd
from snapflow import DataBlock, Snap, SnapContext, Param
from loguru import logger

from mailchimp_marketing import Client
from mailchimp_marketing.api_client import ApiClientError

if TYPE_CHECKING:
    from snapflow_mailchimp import MailchimpMember

# logger.enable("snapflow")


@Snap(
    "export_audience", module="mailchimp",
)
@Param("api_key", "str")
@Param("server", "str")
@Param("list_id", "str")
def export_audience(ctx: SnapContext, members: DataBlock[MailchimpMember]):
    mailchimp = Client()
    mailchimp.set_config(
        {"api_key": ctx.get_param("api_key"), "server": ctx.get_param("server"),}
    )
    list_id = ctx.get_param("list_id")
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
            logger.error(f"{e.text} ({e.status_code})")
