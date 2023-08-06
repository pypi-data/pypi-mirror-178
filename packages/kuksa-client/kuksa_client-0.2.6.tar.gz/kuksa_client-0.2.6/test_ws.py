import kuksa_client

client = kuksa_client.KuksaClientThread({'protocol': 'ws'})
client.start()
print("authorize", client.authorize())
