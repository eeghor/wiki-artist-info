import soundcloud

SOUNDCLOUD_CLIENT_ID = "SMojzQ0UzLRl4MHSh3Opv2zHyTPuLUvY"

client = soundcloud.Client(client_id=SOUNDCLOUD_CLIENT_ID)

a = client.get('/users', q='milky chance')[0]

print(a.username)
print(a.id)
print(a.full_name)
print(a.followers_count)




