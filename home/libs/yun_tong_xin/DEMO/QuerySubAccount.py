#coding=gbk

#coding=utf-8

#-*- coding: UTF-8 -*-  

from CCPRestSDK import REST
import ConfigParser

#���ʺ�
accountSid= '�������ʺ�';

#���ʺ�Token
accountToken= '�������ʺ�Token';

#Ӧ��Id
appId='����Ӧ��ID';

#�����ַ����ʽ���£�����Ҫдhttp://
serverIP='app.cloopen.com';

#����˿� 
serverPort='8883';

#REST�汾��
softVersion='2013-12-26';

  # ���ʺ���Ϣ��ѯ
  # @param friendlyName ���ʺ�����

def querySubAccount(accountName):

    
    #��ʼ��REST SDK
    rest = REST(serverIP,serverPort,softVersion)
    rest.setAccount(accountSid,accountToken)
    rest.setAppId(appId)
    
    result = rest.querySubAccount(accountName)
    for k,v in result.iteritems(): 
        
        if k=='SubAccount' :
            if v!='':
                for k,s in v.iteritems(): 
                    print '%s:%s' % (k, s)
            else:
                 print '%s:%s' % (k, v)
        else:
            print '%s:%s' % (k, v)
#querySubAccount('���ʺ�����')