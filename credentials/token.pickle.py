import pickle
with open('token.pickle', 'rb') as token:
    creds = pickle.load(token)
    print("REFRESH_TOKEN:", creds.refresh_token)
    print("CLIENT_ID:", creds.client_id)
    print("CLIENT_SECRET:", creds.client_secret)