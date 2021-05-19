import os
import requests

def sendmail(mail_to, subject, content, subtype=None):

    # 要调用的发件接口地址，例如http://192.168.1.11:8888/mail_sys/send_mail_http.json
    url = 'http://wu5bocheng:8888/mail_sys/send_mail_http.json'
    pdata = {}
    pdata['mail_from'] = 'wubocheng@wu5bocheng.top'
    pdata['password'] = 'ZJwbc902410'
    pdata['mail_to'] = mail_to
    pdata['subject'] = subject
    pdata['content'] = content
    pdata['subtype'] = subtype

    resp_data = requests.post(url, pdata).json()
    print(resp_data)