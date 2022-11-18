#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#ico 图片转为 base64

import base64
open_icon = open("/Users/baijinhao/pythonProject/databaseImport/resource/tools.ico", "rb")
b64str = base64.b64encode(open_icon.read())
open_icon.close()
write_data = "img = %s" % b64str
f = open("./utils/icon.py", "w+")
f.write(write_data)
f.close()