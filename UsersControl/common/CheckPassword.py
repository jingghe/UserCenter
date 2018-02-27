#-*- coding: utf-8 -*-

import re


def check_password(passwd):
    print passwd
    if re.match(r'^(?=.*[A-Za-z])(?=.*[~!@#$%\^&*()[\]{}\\|;:,<.>/?\'"\-])(?=.*[0-9]).{7,}$', passwd):
        return True
    else:
        return False