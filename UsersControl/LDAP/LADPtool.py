# _*_coding:utf-8_*_

import sys
import ldap
import logging
from rest_framework.exceptions import APIException, ValidationError
from UserCenter import settings


logger = logging.getLogger('django')

reload(sys)
sys.setdefaultencoding("utf-8")


class LdapTools(object):

    def __init__(self, *args, **kwargs):
        self.LDAP_SERVER_IP = getattr(settings, 'LDAP_SERVER_IP')
        self.LDAP_ADMIN = 'cn=%s,%s' % (getattr(settings, 'LDAP_ADMIN'), getattr(settings, 'LDAP_DOMAIN'))
        self.LDAP_PASS = getattr(settings, 'LDAP_PASS')
        self.Ldap_obj = None
        self.ladp_connect(self.LDAP_ADMIN,self.LDAP_PASS)

    def ladp_connect(self, bind_name, bind_passwd):
        conn = ldap.initialize(self.LDAP_SERVER_IP)
        conn.protocol_version = ldap.VERSION3
        try:
            rest = conn.simple_bind_s(self.LDAP_ADMIN, self.LDAP_PASS)
        except ldap.SERVER_DOWN:
            raise APIException("无法连接到LDAP")
        except ldap.INVALID_CREDENTIALS:
            raise APIException("LDAP账号错误")
        except Exception as e:
            raise APIException(type(e))
        if rest[0] != 97: #97表示success
            raise APIException(rest[1])
        self.Ldap_obj = conn

    def ldap_search(self,base, keyword=None, rdn='cn'):
        """
        base: 域 ou=test, dc=test, dc=com
        keyword: 搜索的用户
        rdn: cn/uid
        """
        scope = ldap.SCOPE_SUBTREE
        _filter = "%s=%s" % (rdn,keyword)
        retrieve_attributes = None
        try:
            result_id = self.Ldap_obj.search(base, scope, _filter, retrieve_attributes)
            result_type, result_data = self.Ldap_obj.result(result_id)
            if not result_data:
                return False, []
        except ldap.LDAPError as error_message:
            raise APIException(error_message)
        return True, result_data

    def add_user(self, base_dn, add_record):
        """
        base_dn: cn=test, ou=magicstack,dc=test,dc=com  NOT NONE
        """
        if not base_dn:
            raise ValidationError(u"DN不能为空")
        try:
            result = self.Ldap_obj.add_s(base_dn, add_record)
        except ldap.LDAPError, error_message:
            raise APIException(error_message)
        else:
            if result[0] == 105:
                return True, []
            else:
                return False, result[1]

    def modify_user(self, dn, attr_list):
        """
        MOD_ADD: 如果属性存在，这个属性可以有多个值，那么新值加进去，旧值保留
        MOD_DELETE ：如果属性的值存在，值将被删除
        MOD_REPLACE ：这个属性所有的旧值将会被删除，这个值被加进去

        dn: cn=test, ou=magicstack,dc=test, dc=com
        attr_list: [( ldap.MOD_REPLACE, 'givenName', 'Francis' ),
                    ( ldap.MOD_ADD, 'cn', 'Frank Bacon' )
                   ]
        """
        try:
            result = self.Ldap_obj.modify_s(dn, attr_list)
        except ldap.LDAPError, error_message:
            raise APIException(error_message)
        else:
            if result[0] == 103:
                return True, []
            else:
                return False, result[1]

    def delete_user(self, dn):
        """
        dn: cn=test, ou=magicstack,dc=test, dc=com
        """
        try:
            result = self.Ldap_obj.delete_s(dn)
        except ldap.LDAPError, error_message:
            raise APIException(error_message)
        else:
            if result[0] == 107:
                return True, []
            else:
                return False, result[1]