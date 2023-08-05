# SPDX-FileCopyrightText: Mintlab B.V.
#
# SPDX-License-Identifier: EUPL-1.2

from copy import copy
from dataclasses import dataclass, field
from email.message import EmailMessage
from minty import Base
from smtplib import SMTP
from typing import Any, Dict, Optional


@dataclass
class EmailConfiguration:
    smarthost_mode: str = field(default="custom")
    smarthost_username: Optional[str] = field(default=None)
    smarthost_password: Optional[str] = field(default=None)

    smarthost_token: Optional[str] = field(default=None)

    smarthost_hostname: Optional[str] = field(default=None)
    smarthost_port: Optional[int] = field(default=25)

    # "none" or "starttls"
    smarthost_security: str = field(default="none")


def EmailInfrastructure(config: Dict[str, Any]) -> "OutgoingEmail":
    """Return a new `OutgoingEmail` instance for the current context."""

    return OutgoingEmail(
        default_smtp_smarthost=config["email"]["smarthost_hostname"],
        default_smtp_smarthost_port=config["email"].get("smarthost_port", 25),
        default_smtp_starttls=bool(
            config["email"].get("smarthost_starttls", False)
        ),
    )


class OutgoingEmail(Base):
    def __init__(
        self,
        default_smtp_smarthost: str,
        default_smtp_smarthost_port: int = 25,
        default_smtp_starttls: bool = False,
    ):
        """
        Infrastructure class to send email.

        :param default_smtp_smarthost: Hostname of the default SMTP smart host
        :type default_smtp_smarthost: str
        :param default_smtp_smarthost_port: TCP port used to connect to the
            SMTP smart host, defaults to 25
        :type default_smtp_smarthost_port: int, optional
        """

        self.default_smtp_smarthost = default_smtp_smarthost
        self.default_smtp_smarthost_port = default_smtp_smarthost_port
        self.default_smtp_starttls = default_smtp_starttls

    def _merge_configuration(
        self, email_configuration: EmailConfiguration
    ) -> EmailConfiguration:
        merged: EmailConfiguration = copy(email_configuration)

        if merged.smarthost_hostname is None:
            merged.smarthost_hostname = self.default_smtp_smarthost
            merged.smarthost_port = self.default_smtp_smarthost_port
            merged.smarthost_username = None
            merged.smarthost_password = None
            merged.smarthost_security = (
                "starttls" if self.default_smtp_starttls else "none"
            )
        return merged

    def _authenticate(
        self, connection: SMTP, config: EmailConfiguration
    ) -> None:
        if config.smarthost_mode == "oauth2":

            def _generate_oauth2_response(
                challenge: Optional[bytes] = None,
            ) -> str:
                username = config.smarthost_username
                token = config.smarthost_token
                return f"user={username}\x01auth=Bearer {token}\x01\x01"

            connection.auth(
                mechanism="XOAUTH2",
                authobject=_generate_oauth2_response,
                initial_response_ok=False,
            )
        elif config.smarthost_username:
            assert config.smarthost_password is not None
            connection.login(
                user=config.smarthost_username,
                password=config.smarthost_password,
            )

    def send(
        self, message: EmailMessage, email_configuration: EmailConfiguration
    ) -> None:
        """Send an `email.Message` using the email smart-host configured in
        `email_configuration`.

        :param message: Message to send out
        :type message: EmailMessage
        :param email_configuration: Email configuration of the current context
            (usually retrieved from a database)
        :type email_configuration: EmailConfiguration
        """
        config = self._merge_configuration(email_configuration)

        assert config.smarthost_hostname is not None
        assert config.smarthost_port is not None
        with SMTP(
            host=config.smarthost_hostname, port=config.smarthost_port
        ) as connection:
            if config.smarthost_security == "starttls":
                connection.starttls()

            connection.ehlo_or_helo_if_needed()

            self._authenticate(connection, config)
            connection.send_message(message)

        return
