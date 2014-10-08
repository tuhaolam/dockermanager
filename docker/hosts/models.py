#coding: utf-8
__author__ = 'aaron'


class Host:
    def __init__(self,*args,**kwargs):
        self.name =None
        self.hostname = None
        self.public_hostname=None
        self.port = None
        self.agent_key = None
        self.last_updated = None
        self.enabled = False

    def __unicode__(self):
        return self.name