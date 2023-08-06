# -*- encoding: utf-8 -*-

import os
import json
import getpass
from urllib.parse import urlparse

from metadata.utils.time import get_current_datetime
from metadata.ensure import ensure_true, ensure_endpoint_format
from metadata.exception import MetadataException
from metadata.context import MetadataContext
from metadata.cli.auth import set_user_context


def do_login(args):
    endpoint = ensure_endpoint_format(args.endpoint)
    name = args.name or get_current_datetime().strftime('%Y%m%d%H%M%S')
    if args.token:
        token = args.token
    else:
        token = getpass.getpass('Token : ')
    with MetadataContext(endpoint=endpoint, token=token) as context:
        user_email = context.user_email

    lbg_config_path = os.path.expanduser('~/.lbg/lbg_cli_context.json')
    config = {}
    if os.path.exists(lbg_config_path):
        with open(lbg_config_path) as f:
            config = json.load(f)

    bohrium_user = args.bohrium_user or config.get('ACCOUNT_EMAIL')
    bohrium_password = args.bohrium_password or config.get('ACCOUNT_PASSWORD')
    bohrium_project = args.bohrium_project or config.get('PROGRAM_CURRENT_PROGRAM_ID')

    ensure_true(bohrium_user, 'Bohrium user required')
    ensure_true(bohrium_password, 'Bohrium user required')
    ensure_true(bohrium_project, 'Bohrium project required')

    set_user_context(
        name,
        endpoint, token, args.project,
        user_email=user_email,
        bohrium_user=bohrium_user,
        bohrium_password=bohrium_password,
        bohrium_project=str(bohrium_project),
    )
    print(f'login into {endpoint} with {user_email} successfully, context named as {name}')
