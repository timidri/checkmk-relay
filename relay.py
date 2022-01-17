#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) 2019 tribe29 GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

import socket

import cmk.utils.version as cmk_version
import cmk.gui.mkeventd as mkeventd
import cmk.gui.config as config
from cmk.gui.i18n import _
from cmk.gui.globals import html

from cmk.gui.valuespec import (
    Age,
    Alternative,
    CascadingDropdown,
    DEF_VALUE,
    Dictionary,
    DropdownChoice,
    EmailAddress,
    FixedValue,
    HTTPUrl,
    Integer,
    IPv4Address,
    ListChoice,
    ListOfStrings,
    Password,
    TextAreaUnicode,
    TextAscii,
    TextUnicode,
    Transform,
    Tuple,
)

from cmk.gui.plugins.wato import (
    notification_parameter_registry,
    NotificationParameter,
    passwordstore_choices,
    HTTPProxyReference,
    IndividualOrStoredPassword,
)

from cmk.gui.plugins.wato.utils import (
    PasswordFromStore,)

@notification_parameter_registry.register
class NotificationParameterRelay(NotificationParameter):
    @property
    def ident(self):
        return "relay"

    @property
    def spec(self):
        return Dictionary(
            title=_("Create notification with the following parameters"),
            optional_keys=["ignore_ssl", "proxy_url"],
            elements=[
                ("api_token",
                 TextAscii(
                     title=_("API Token"),
                     help=
                     _("You need to provide a valid API key to be able to send push notifications "
                       "using Relay. Register and login to <a href=\"https://www.relay.sh\" "
                       "target=\"_blank\">Relay</a>, create your workflow and add a Push trigger to obtain an API token."),
                     size=400,
                     allow_empty=False,
                     regex="[a-zA-Z0-9\.]{300,400}",
                 )),
                (
                    "proxy_url",
                    Transform(
                        HTTPProxyReference(),
                        # Transform legacy explicit TextAscii() proxy URL
                        forth=lambda v: ("url", v) if isinstance(v, str) else v,
                    )),
                    ("ignore_ssl",
                     FixedValue(
                         True,
                         title=_("Disable SSL certificate verification"),
                         totext=_("Disable SSL certificate verification"),
                         help=_("Ignore unverified HTTPS request warnings. Use with caution."),
                     )),
		],
		)
