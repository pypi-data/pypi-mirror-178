import dbs
import six

from dbscli.utils import log


try:
    from termcolor import colored
except ImportError:
    def colored(string, color):
        return string


def ls(team_id, ewf_type):
    filters = {
        'ewf_type': ewf_type
    }
    state_colors = {
        'Active': 'green'
    }
    ewfs = dbs.ewf.get_items(team_id, filters)
    for ewf in ewfs:
        six.print_(" - ({:10s}) {}".format(
            colored(ewf['state'], state_colors.get(ewf['state'], "white")),
            colored(ewf['ewf_id'], "cyan")
        ))


