# Big Data Smart Socket
# Copyright (C) 2016 Clemson University
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#

import logging
import requests

from ..config import client_destination, metadata_repository_url


cli_help = "Check client configuration."


logger = logging.getLogger("bdss")


def configure_parser(parser):
    pass


def ping_metadata_repository():
    """Check that the /transfers endpoint exists at the configured metadata repository URL."""
    try:
        response = requests.get("%s/%s" % (metadata_repository_url, "transfers"))
        return response.status_code == 200
    except:
        return False


def get_destinations():
    """Request list of destinations from metadata repository."""
    response = requests.get("%s/%s" % (metadata_repository_url, "destinations"), headers={
        "accept": "application/json"
    })
    if response.status_code == 200:
        return response.json()["destinations"]
    else:
        response.raise_for_status()


def handle_action(args, parser):
    if ping_metadata_repository():
        logger.info("Metadata repository URL OK")
    else:
        logger.error("%s does not appear to be a BDSS metadata repository", metadata_repository_url)

    if not client_destination:
        logger.info("No client location configured")
    else:
        try:
            destinations = get_destinations()
        except:
            logger.warn("Unable to load destinations from metadata repository")
        else:
            if client_destination in [d["label"] for d in destinations]:
                logger.info("Client location OK")
            else:
                logger.error("%s is not a recognized destination", client_destination)
