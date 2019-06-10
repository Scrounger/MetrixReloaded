# -*- coding: utf-8 -*-
import os


def getVersion():
    grepcommand = 'opkg list-installed | grep enigma2-plugin-skin-metrixreloaded | cut -d " " -f 3'
    out = os.popen(grepcommand).readlines()
    try:
        return str(out[0]).strip()
    except:
        return str(out).strip()