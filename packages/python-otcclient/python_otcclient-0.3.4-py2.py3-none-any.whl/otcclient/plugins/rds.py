#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of OTC Tool released under MIT license.
# Copyright (C) 2016 T-systems Kurt Garloff, Zsolt Nagy

from otcclient.core.OtcConfig import OtcConfig 
from otcclient.utils import utils_http, utils_templates

from otcclient.core.otcpluginbase import otcpluginbase
from otcclient.core.pluginmanager import getplugin
import json
from otcclient.plugins.ecs import ecs
import os
    
class rds(otcpluginbase):
    ar = {}    
    
    @staticmethod
    def otcOutputHandler(): 
        return getplugin(OtcConfig.OUTPUT_FORMAT)
 
    def otctype(self):
        return "func" 

    @staticmethod
    def add():
        ret = utils_templates.create_request("as_modify")
        print ret
#        print ret

        #url = rds.baseurl + "/rds/v1/"+ OtcConfig.PROJECT_ID + "/instances"
        #ret = utils_http.get(url)
        return ret


    #print utils_templates.create_request("index")
#        print url       
#        print ret

    @staticmethod
    def describe_db_instances():
        url = rds.baseurl + "/rds/v1/"+ OtcConfig.PROJECT_ID + "/instances"
        ret = utils_http.get(url)
        return ret
