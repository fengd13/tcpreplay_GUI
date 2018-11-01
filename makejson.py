# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 09:50:29 2018

@author: fd
"""

import json

dic = {
    "真实流量测试":
        {
            "dspflow": ["flow.pcap"],

            "flow": ["flow2.pcap", "3.pcap"],
        },

    "恶意流量测试":
        {
            "情况1": ["6.pcap"],

            "情况2": ["7.pcap", "8.pcap"],
            "情况3": ["9.pcap", "10.pcap"],
        },
    "具体流量测试":
        {
            "ARP": ["arp.pcap"],
            "DB2": ["db2.pcap"],
            "DNS": ["dns.pcap"],
            "FTP": ["dns.pcap"],
            "HTTP": ["http.pcap"],
            "HTTPS": ["https.pcap"],
            "MEMCACHE": ["memcached.pcap"],
            "MONGO": ["mongo.pcap"],
            "MYSQL": ["mysql.pcap"],
            "ORACLE": ["oracle.pcap"],
            "REDIS": ["redis.pcap"],
            "SMTP": ["smtp.pcap"],
            "SNMPv1": ["snmp1.pcap"],
            "SNMPv2": ["snmp2.pcap"],
            "SNMPv3": ["snmp3.pcap"],
            "SSH": ["ssh.pcap"],
            "SSL": ["ssl.pcap"],
            "SYBASE": ["sybase.pcap"],
            "TELNET": ["telnet.pcap"],
            "UDP": ["udp.pcap"],
            "VLAN": ["vlan.pcap"],
        }

}
with open("config.json","w") as dump_f:
    json.dump(dic,dump_f,ensure_ascii=False)

with open('config.json', 'r') as json_file:
    """
    读取该json文件时，先按照gbk的方式对其解码再编码为utf-8的格式
    """
    data = json_file.read()
    print(type(data))    # type(data) = 'str'
    result = json.loads(data)
    print(result)
