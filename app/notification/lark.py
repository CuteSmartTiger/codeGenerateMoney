import requests

from app.config import get_settings

settings = get_settings()


has_trigger ={}

def trigger_lark(body,remove_duplicates=True):
    if remove_duplicates:
        key = "{}-{}".format(body['timeId'], body['instId'])
        if not key in has_trigger:
            requests.post(url=settings.LARK_URL, json=body, headers={'Content-Type': 'application/json'})
            has_trigger[key] = True