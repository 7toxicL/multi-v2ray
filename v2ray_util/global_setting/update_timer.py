#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import time
import platform

from ..util_core.config import Config
from ..util_core.utils import ColorStr

IS_CENTOS = True if "centos" in platform.linux_distribution()[0].lower() else False

def planUpdate():
    if Config().get_data("lang") == "zh":
        origin_time_zone = int(time.strftime("%z", time.gmtime())[0:-2])
        beijing_time_zone, beijing_update_time = 8, 3
        diff_zone = beijing_time_zone - origin_time_zone
        local_time = beijing_update_time - diff_zone
        if local_time < 0:
            local_time = 24 + local_time
        elif local_time >= 24:
            local_time = local_time - 24
        ColorStr.cyan("{}: {}".format(_("Beijing time: 3, VPS time"), local_time))
    else:
        local_time = 3
    os.system('echo "SHELL=/bin/bash" >> crontab.txt && echo "$(crontab -l)" >> crontab.txt')
    os.system('echo "0 {} * * * bash <(curl -L -s https://install.direct/go.sh) | tee -a /root/v2rayUpdate.log && service v2ray restart" >> crontab.txt'.format(local_time))
    os.system("crontab crontab.txt && rm -f crontab.txt")
    if IS_CENTOS:
        os.system("service crond restart >/dev/null 2>&1")
    else:
        os.system("service cron restart >/dev/null 2>&1")
    print(ColorStr.green(_("success open schedule update task!")))
    
def manage():
    check_result = os.popen("crontab -l|grep v2ray").readlines()

    status = _("open") if check_result else _("close")

    print("{}: {}".format(_("schedule update v2ray task"), status))

    print("")
    print(_("1.open schedule task"))
    print("")
    print(_("2.close schedule task"))
    print("")
    print(_("Tip: open schedule update v2ray at 3:00"))

    choice = input(_("please select: "))

    if choice == "1":
        if check_result:
            print(ColorStr.yellow(_("have open schedule!")))
            return
        else:
            planUpdate()
    elif choice == "2":
        os.system("crontab -l|sed '/SHELL=/d;/v2ray/d' > crontab.txt && crontab crontab.txt && rm -f crontab.txt")
        print(ColorStr.green(_("close shedule task success")))
        if IS_CENTOS:
            os.system("service crond restart >/dev/null 2>&1")
        else:
            os.system("service cron restart >/dev/null 2>&1")