import os
import requests


class Attachment:
    def __init__(self, name, path):
        self.name = name
        self.path = path
        self.link = 'https://2ch.hk' + self.path


class Post:
    def __init__(self, num, date, name, op, subject, comment, files):
        self.num = num
        self.date = date
        self.name = name
        self.op = op
        self.subject = subject
        self.comment = comment
        self.files = files


class Thread:
    def __init__(self, num):
        self.num = num


class Board:
    def __init__(self, code):
        self.code = code


class Navigator:
    def __init__(self):
        pass
