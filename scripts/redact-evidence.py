"""Redact environment identifiers without altering test results or metric values."""

import ipaddress
import re


def redact(text):
    text = re.sub(r"\x1b\[[0-9;]*m", "", text)
    text = re.sub(r"/(?:home/runner|workspace|tmp|opt)/[^\s\"']+", "<REDACTED_PATH>", text)
    text = re.sub(r"[a-f0-9]{8}(?:-[a-f0-9]{4}){3}-[a-f0-9]{12}", "<REDACTED_RUNNER_ID>", text)
    text = re.sub(r"arn:aws:[^\s\"']+", "<REDACTED_ARN>", text)

    def hide_private(match):
        value = match.group(0)
        try:
            address = ipaddress.ip_address(value)
            return (
                "<REDACTED_CLUSTER_IP>" if address.is_private and not address.is_loopback else value
            )
        except ValueError:
            return value

    return re.sub(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", hide_private, text)
