import os
import click
import dbs
import datetime
import pandas as pd
import six

from pytz import utc
from configstore import ConfigStore

from dbscli import ewf
from dbscli.utils import log, OrderedGroup
from dbscli.ask import *

try:
    from termcolor import colored
except ImportError:
    def colored(string, color):
        return string


conf = ConfigStore("dbs-cli")


@click.group(cls=OrderedGroup)
@click.pass_context
def main(ctx):
    """
    CLI for DeepNatural Brain Services
    """


@main.command()
def init():
    log("DeepNatural Brain Services", color="blue", figlet=True)
    log("Welcome to DBS CLI", "green")

    conf.clear()
    try:
        api_key = conf.get("api_key")
    except KeyError:
        api_key = ask_api_key()
        conf.set(api_key)

    log(f" - Team ID: {conf.get('team_id')}", color='white')
    log(f" - Team Name: {conf.get('team_name')}", color='white')
    log(f" - Team API Key: {conf.get('api_key')[:4] + '*' * 20}", color='white')


# @main.command()
def account():
    try:
        account = conf.get("account")
        expires_at = datetime.datetime.fromisoformat(conf.get('expires_at'))
        if expires_at < utc.localize(datetime.datetime.utcnow()) - datetime.timedelta(seconds=60):
            r = dbs.auth.refresh_token(conf.get("refresh_token"))
            r['expires_at'] = (utc.localize(datetime.datetime.utcnow()) + datetime.timedelta(seconds=r['expires_in'])).isoformat()
            conf.set(r)
        r = dbs.auth.get_user_profile(conf.get("access_token"))
    except KeyError:
        account = ask_account()
        conf.set(account)
        password = ask_password()

    log(f" - Account: {conf.get('account')}", color='white')


# text-classification
@main.group()
@click.pass_context
def text_classification(ctx):
    pass


@text_classification.command('ls')
@click.pass_context
def text_classification_ls(ctx):
    ewf.ls(team_id=conf.get('team_id'), ewf_type=ctx.parent.command.name)


@text_classification.command('request')
@click.pass_context
@click.option('--ewf', help='Elastic Worfklow ID')
@click.option('--tasks', help='Excel file containing tasks you want to solve using human brains', callback=validate_tasks)
def text_classification_request(ctx, ewf, tasks):
    # check command options
    if not ewf:
        ewf = ask_ewf_choices(team_id=conf.get('team_id'), ewf_type=ctx.parent.command.name)['ewf']
    if not tasks:
        tasks = ask_tasks()['tasks']

    # fetch ewf information
    ewf_id = ewf
    ewf = dbs.ewf.get_item(team_id=conf.get('team_id'), ewf_id=ewf_id)

    six.print_(colored(f"Image Description v{ewf['version']}", "green"))
    six.print_(colored(" * Team Name: ", "white") + colored(conf.get('team_name'), "cyan"))
    six.print_(colored(" * Team ID: ", "white") + colored(conf.get('team_id'), "cyan"))
    six.print_(colored(" * Elastic Workflow ID: ", "white") + colored(ewf_id, "cyan"))

    # read xlsx file
    six.print_(colored(f" * Read tasks from Excel file: ", "white") + colored(tasks, "cyan"))
    df = pd.read_excel(tasks, dtype={"text": str})

    task_items = []
    for idx, row in df.iterrows():
        text_id = row['text_id']
        text = row['text']
        task_items.append({
            "text_id": row['text_id'],
            "text": row['text'],
        })

    six.print_(colored(f" * Tasks: ", "white") + colored(f"{len(task_items)} items", "cyan"))
    six.print_(colored(f" * Store results to: ", "white") + colored(ewf.get('response_to_url'), "cyan"))
    six.print_(colored(f" * Request tasks:", "white"))

    with click.progressbar(task_items) as bar:
        for task in bar:
            dbs.text_classification.request_task(ewf, task)


# image-description
@main.group()
@click.pass_context
def image_description(ctx):
    pass


@image_description.command('ls')
@click.pass_context
def image_description_ls(ctx):
    ewf.ls(team_id=conf.get('team_id'), ewf_type=ctx.parent.command.name)


@image_description.command('request')
@click.pass_context
@click.option('--ewf', help='Elastic Worfklow ID')
@click.option('--tasks', help='Excel file containing tasks you want to solve using human brains', callback=validate_tasks)
def image_description_request(ctx, ewf, tasks):
    # check command options
    if not ewf:
        ewf = ask_ewf_choices(team_id=conf.get('team_id'), ewf_type=ctx.parent.command.name)['ewf']
    if not tasks:
        tasks = ask_tasks()['tasks']

    # fetch ewf information
    ewf_id = ewf
    ewf = dbs.ewf.get_item(team_id=conf.get('team_id'), ewf_id=ewf_id)

    six.print_(colored(f"Image Description v{ewf['version']}", "green"))
    six.print_(colored(" * Team Name: ", "white") + colored(conf.get('team_name'), "cyan"))
    six.print_(colored(" * Team ID: ", "white") + colored(conf.get('team_id'), "cyan"))
    six.print_(colored(" * Elastic Workflow ID: ", "white") + colored(ewf_id, "cyan"))

    # read xlsx file
    six.print_(colored(f" * Read tasks from Excel file: ", "white") + colored(tasks, "cyan"))
    df = pd.read_excel(tasks, dtype={"image": str, "image_id": str})
    image_dir = os.path.dirname(tasks)

    task_items = []
    for idx, row in df.iterrows():
        image = row['image']
        if not os.path.isfile(os.path.join(image_dir, image)):
            raise click.ClickException(f"Cannot find image file '{image}'")
        task_items.append({
            "image_id": row['image_id'],
            "image": image,
        })

    six.print_(colored(f" * Tasks: ", "white") + colored(f"{len(task_items)} items", "cyan"))
    six.print_(colored(f" * Store results to: ", "white") + colored(ewf.get('response_to_url'), "cyan"))
    six.print_(colored(f" * Request tasks:", "white"))

    with click.progressbar(task_items) as bar:
        for task in bar:
            dbs.image_description.upload_image(ewf, task, image_dir)
            dbs.image_description.request_task(ewf, task)


if __name__ == '__main__':
    main()
