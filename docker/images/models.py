#coding: utf-8
__author__ = 'aaron'
import json
class Image:
    def __init__(self):
        self.image_id=None
        self.repository = None
        self.host = None
        self.history = None
    def __unicode__(self):
        img_id = 'unknown'
        if self.image_id:
            img_id = self.image_id[:12]
        return "{} ({})".format(self.repository, img_id)

    def get_history(self):
        history = {}
        if self.history:
            history = json.loads(self.history)
        return history