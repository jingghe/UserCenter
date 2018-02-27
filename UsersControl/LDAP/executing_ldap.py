#-*- coding: utf-8 -*-

import logging
import ldap.modlist
from UserCenter import settings
from UsersControl.LDAP.LADPtool import LdapTools
from UsersControl.email.send_email import SendEmail

logger = logging.getLogger('django_log_file')


class ExecutingLdap(object):
    def __init__(self):
        self.User = None
        self.Receiver_user = None
        self.Receiver_pass = None
        self.ldaptools = LdapTools()


    def executing_add_user_to_LDAP(self, form, uid, password):
        """添加LDAP账户"""
        add_record = self.build_record(form, uid, password)
        dn = "cn=%s,ou=%s,%s" % (form.cleaned_data['username'],
                              getattr(settings, 'LDAP_OU'),
                              getattr(settings, 'LDAP_DOMAIN'))

        add_user_result = self.ldaptools.add_user(dn, add_record)
        if add_user_result:
            sendemail = SendEmail(Receiver_user=self.Receiver_user,
                                  Receiver_pass=self.Receiver_pass,
                                  Receiver_nikname=self.Receiver_nikname,
                                  username=self.User)
            send_email_result = sendemail.send(first=True)
        if add_user_result and send_email_result:
            return True
        return False

    def build_record(self, form, uid, password):
        """构建LDAP账户参数"""
        email_suffix = str(getattr(settings, 'MAIL_USER')).split('@')
        email = str(form.cleaned_data['username'])+'@'+email_suffix[1]
        add_record = dict()
        add_record['cn'] = [str(form.cleaned_data['username'])]
        add_record['uid'] = [str(form.cleaned_data['username'])]
        add_record['uidNumber'] = [str(uid)]
        add_record['gidNumber'] = [str(getattr(settings, 'gidNumber'))]
        add_record['homeDirectory'] = ['/home/%s' % str(form.cleaned_data['username'])]
        add_record['userPassword'] = [str(password)]
        add_record['objectClass'] = ['top', 'posixAccount', 'inetOrgPerson']
        add_record['o'] = ['\xe5\xb9\xbf\xe5\xb7\x9e']
        add_record['street'] = ['\xe5\xb9\xbf\xe5\xb7\x9e']
        add_record['sn'] = [str(form.cleaned_data['username'])]
        add_record['givenName'] = [str(form.cleaned_data['nickname'])]
        add_record['mail'] = email
        add_record['telephoneNumber'] = [str(form.cleaned_data['phone'])]
        self.User = form.cleaned_data['username']
        self.Receiver_user = form.cleaned_data['email'] if form.cleaned_data['email'] else email
        self.Receiver_pass = add_record['userPassword'][0]
        self.Receiver_nikname = add_record['sn'][0]
        add_record = ldap.modlist.addModlist(add_record)
        return add_record

    def modify_user_to_ldap(self, user, attr_list):
        """重置LDAP密码"""
        dn = "cn=%s,ou=%s,%s" % (user.username,
                              getattr(settings, 'LDAP_OU'),
                              getattr(settings, 'LDAP_DOMAIN'))
        res = self.ldaptools.modify_user(dn, attr_list)
        self.User = user.username
        self.Receiver_user = user.email
        self.Receiver_pass = attr_list[0][2]
        self.Receiver_nikname = user.nickname

        if res:
            sendemail = SendEmail(Receiver_user=self.Receiver_user,
                                  Receiver_pass=self.Receiver_pass,
                                  Receiver_nikname=self.Receiver_nikname,
                                  username=self.User)
            send_email_result = sendemail.send()
            if send_email_result:
                return True
            return False

    def delete_ldap_user(self, user):
        """删除LDAP用户"""
        dn = "cn=%s,ou=%s,%s" % (user.username,
                              getattr(settings, 'LDAP_OU'),
                              getattr(settings, 'LDAP_DOMAIN'))
        status, res = self.ldaptools.delete_user(dn)
        if status:
            return True, res
        return False, res