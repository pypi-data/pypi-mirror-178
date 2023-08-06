import os
import dbs
import click

from PyInquirer import prompt
from dbscli.validators import EmailValidator, PasswordValidator, ApiKeyValidator, EmptyValidator, GSheetURLValidator, FilePathValidator
from dbscli.utils import style

def ask_account():
    questions = [
        {
            'type': 'input',
            'name': 'account',
            'message': 'Enter DeepNatural account (email address)',
            'validate': EmailValidator,
        },
    ]
    answers = prompt(questions, style=style)
    return answers


def ask_password():
    questions = [
        {
            'type': 'password',
            'name': 'password',
            'message': 'Enter DeepNatural password',
            'validate': PasswordValidator,
        },
    ]
    answers = prompt(questions, style=style)
    return answers


def ask_team_id():
    questions = [
        {
            'type': 'input',
            'name': 'team_id',
            'message': 'Enter DeepNatural Team ID (Only needed to provide once)',
            'validate': TeamIdValidator,
        },
    ]
    answers = prompt(questions, style=style)
    return answers


def ask_api_key():
    questions = [
        {
            'type': 'input',
            'name': 'api_key',
            'message': 'Enter DeepNatural API Key (Only needed to provide once)',
            'validate': ApiKeyValidator,
        },
    ]
    answers = prompt(questions, style=style)
    return answers


def ask_ewf():
    questions = [
        {
            'type': 'input',
            'name': 'ewf',
            'message': 'Enter active EWF ID (Elastic Workflow ID)',
            'validate': EmptyValidator,
        },
    ]
    answers = prompt(questions, style=style)
    return answers


def ask_ewf_choices(team_id, ewf_type):
    filters = {
        'ewf_type': ewf_type,
        'state': 'Active',
    }
    ewfs = dbs.ewf.get_items(team_id, filters)
    questions = [
        {
            'type': 'list',
            'name': 'ewf',
            'message': 'Select active EWF (Elastic Workflow)',
            'choices': [x['ewf_id'] for x in ewfs],
            'validate': EmptyValidator,
        },
    ]
    answers = prompt(questions, style=style)
    return answers


def ask_tasks():
    questions = [
        {
            'type': 'input',
            'name': 'tasks',
            'message': 'Enter .xlsx Excel file containing tasks you want to solve using human brains',
            'validate': FilePathValidator,
        },
    ]
    answers = prompt(questions, style=style)
    return answers


def ask_response_to():
    questions = [
        {
            'type': 'input',
            'name': 'response_to',
            'message': 'Google spreadsheet URL where the results are stored',
            'validate': GSheetURLValidator,
        },
    ]
    answers = prompt(questions, style=style)
    return answers


def validate_tasks(ctx, param, value):
    if value is None:
        return value
    if not os.path.isfile(value):
        raise click.BadParameter(f"Cannot find tasks file '{value}'")
    return value


def get_id_from_gsheet_url(url):
    return url.split('/d/')[1].split('/')[0]


def validate_response_to(ctx, param, value):
    if value is None:
        return value
    if not value.startswith('https://docs.google.com/spreadsheets/d/'):
        raise click.BadParameter(f"Invalid google spreadsheet URL '{value}'")
    try:
        gsheet_id = get_id_from_gsheet_url(value)
    except:
        raise click.BadParameter(f"Invalid google spreadsheet URL '{value}'")
    return value


