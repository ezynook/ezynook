#pip install py-zabbix
from pyzabbix import ZabbixMetric, ZabbixSender
import subprocess
import os
def ZabbixSender(key: str, message: str):
	hostname = "mgnt-etl.tat.or.th"
	ipaddress = "10.41.1.25"
	packet = [
		ZabbixMetric(hostname, key, message),
		ZabbixMetric(hostname, key, message),
	]
	result = ZabbixSender(use_config=True).send(packet)
	print(result)