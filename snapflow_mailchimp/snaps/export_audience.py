from __future__ import annotations

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
    "export_audience",
    module="mailchimp",
)
@Param("api_key", "str")
@Param("server", "str")
@Param("list_id", "str")
def export_audience(
    ctx: SnapContext, members: DataBlock[MailchimpMember]
):
    mailchimp = Client()
    mailchimp.set_config({
        "api_key": ctx.get_param("api_key"),
        "server": ctx.get_param("server"),
    })
    list_id = ctx.get_param("list_id")
    member_records = members.as_records()
    for record in member_records:
        try:
            response = mailchimp.lists.add_list_member(list_id, record)
        except ApiClientError as e:
            # TODO: emit bad row? Error? ctx.emit("error", row) or collect and at end ctx.emit("error", error_records)
            logger.error(e)
