from google import genai

client = genai.Client(api_key="AIzaSyB2q_C5QdJxbugLDEKcoRUASLKVhS0WjYU")

for model in client.models.list():
    print(model.name)