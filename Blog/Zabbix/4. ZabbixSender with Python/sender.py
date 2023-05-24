from ZabbixSender import ZabbixSender, ZabbixPacket
server = ZabbixSender('192.168.10.121', 10051)

packet = ZabbixPacket()
packet.add('myhost','key', 'value')

server.send(packet)

print(server.status)