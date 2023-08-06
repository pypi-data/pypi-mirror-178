import requests


BASE_URL = 'https://b6fojbrz1i.execute-api.ap-northeast-2.amazonaws.com/Prod/'


def get_item(team_id, ewf_id):
    url = BASE_URL + f'team/{team_id}/ewf/{ewf_id}/'
    headers = {
        "Content-Type": "application/json"
    }
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    return r.json()['ewf']


def get_items(team_id, filters=None):
    url = BASE_URL + f'team/{team_id}/ewf/'
    headers = {
        "Content-Type": "application/json"
    }
    r = requests.get(url, headers=headers, params=filters)
    r.raise_for_status()
    return r.json()['ewf']
