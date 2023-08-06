import requests
import json
import os


def request_task(ewf, task):
    url = ewf['endpoints']['request']
    headers = {
        "Content-Type": "application/json"
    }

    assert 'image' in task
    assert 'image_id' in task

    payload = {
        'image_id': task['image_id'],
        'image': task['image'],
        'language': task.get('language', 'ko')
    }

    r = requests.request("POST", url, headers=headers, data=json.dumps(payload))
    r.raise_for_status()
    return r.json()


def get_image_upload_url(ewf, task):
    url = ewf['endpoints']['upload_image']
    headers = {
        "Content-Type": "application/json"
    }

    assert 'image' in task

    payload = {
        'image': task['image'],
    }

    r = requests.request("PUT", url, headers=headers, data=json.dumps(payload))
    r.raise_for_status()
    return r.json()


def upload_image(ewf, task, image_dir):
    res = get_image_upload_url(ewf, task)

    with open(os.path.join(image_dir, task['image']), 'rb') as f:
        files = {
            'file': (task['image'], f)
        }
        r = requests.post(res['url'], data=res['fields'], files=files, timeout=60)

    r.raise_for_status()

