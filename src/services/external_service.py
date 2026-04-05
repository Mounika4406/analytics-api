import random

def external_call():
    if random.random() < 0.5:
        raise Exception("External service failed")

    return {"data": "External success"}