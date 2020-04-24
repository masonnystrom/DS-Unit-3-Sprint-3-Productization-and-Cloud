import openaq

def api_client():
    api = openaq.OpenAQ()

    return api

if __name__ == "__main__":

    api = api_client
