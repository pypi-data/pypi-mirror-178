from django.conf import settings
from appconf import AppConf

class FECRepaymentConf(AppConf):
    # WSDL = 'https://publicapi-uat.fecredit.com.vn:4444/APS_RepaymentSchedule?WSDL'
    # WSDL = 'file:///tmp/repayment/repayment.wsdl.xml'
    WSDL = 'https://api-uat-internal.fecredit.com.vn/APS_RepaymentSchedule?WSDL'
    USERNAME = '36f8ffe70dbf43cfbef5ab3c435e7932'
    PASSWORD = '87156FC6369541cd8A0726DD7678e479'

    REQUEST_MORA = """<![CDATA[<?xml version="1.0" encoding="UTF-8"?><FIXML xsi:schemaLocation="http://www.finacle.com/fixml executeFinacleScript.xsd" xmlns="http://www.finacle.com/fixml" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">{}</FIXML>]]>"""
    REQUEST_NONMORA = """<![CDATA[<?xml version="1.0" encoding="UTF-8"?><FIXML xsi:schemaLocation="http://www.finacle.com/fixml executeFinacleScript.xsd" xmlns="http://www.finacle.com/fixml" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">{}</FIXML>]]>"""
    REQUEST_APS = """<![CDATA[<?xml version="1.0" encoding="UTF-8"?><FIXML xmlns="http://www.finacle.com/fixml" xmlns="http://www.finacle.com/fixml">{}</FIXML>]]>"""

    class Meta:
        prefix = 'repayment'
