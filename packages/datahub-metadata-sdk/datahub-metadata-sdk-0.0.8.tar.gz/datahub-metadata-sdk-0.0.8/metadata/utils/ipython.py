# -*- encoding: utf-8 -*-

import sys
import json
import os
import logging
import argparse
from traitlets.config import get_config

from metadata.context import MetadataContext
from metadata.entity.dataset import Dataset # noqa
from metadata.entity.dataset_group import DatasetGroup # noqa
from metadata.entity.model import Model # noqa
from metadata.entity.model_group import ModelGroup # noqa


logger = logging.getLogger(__name__)


def main(args):
    try:
        import IPython
    except ImportError:
        print("IPython not found, run `pip install ipython` to install")
        sys.exit(1)
    load_presets(args)
    c = get_config()
    c.InteractiveShellEmbed.colors = "Linux"
    IPython.embed(config=c)


def load_presets(args):
    context = MetadataContext(project=args.project)
    globals()['context'] = context
    globals()['client'] = context.client
    context.start()

    from dflow import s3_config
    from dflow.plugins import bohrium
    from dflow.plugins.bohrium import TiefblueClient
    lbg_config_path = os.path.expanduser('~/.lbg/lbg_cli_context.json')
    config = {}
    if os.path.exists(lbg_config_path):
        with open(lbg_config_path) as f:
            config = json.load(f)
            bohrium.config["username"] = config['ACCOUNT_EMAIL']
            bohrium.config["password"] = config['ACCOUNT_PASSWORD']
            bohrium.config["project_id"] = config['PROGRAM_CURRENT_PROGRAM_ID']
            s3_config["repo_key"] = "oss-bohrium"
            s3_config["storage_client"] = TiefblueClient()
            globals()['storage_client'] = s3_config["storage_client"] 
    return config


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--project', required=False, default='default')
    args = parser.parse_args()
    main(args)
