from birdy.twitter import UserClient

CONSUMER_KEY = "rcWa6oXEQcXywH4ibZYaTJm7M"
CONSUMER_SECRET = "fodU8RVpk1nYchlPWO0UuwMuQu8pqIIQXk0uTCn9fgnZIDDVgW"

client = UserClient(CONSUMER_KEY, CONSUMER_SECRET)

response = client.api.users.show.get(screen_name='flumemusic')
print(response.data['followers_count'])