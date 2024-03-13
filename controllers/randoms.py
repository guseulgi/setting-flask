from uuid import uuid4


def randomStr():
    return uuid4().hex


def randomNum():
    return uuid4().int
