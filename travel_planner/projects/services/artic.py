import requests

def validate_place(external_id):
    url = f"https://api.artic.edu/api/v1/artworks/{external_id}"
    response = requests.get(url)

    if response.status_code != 200:
        return None

    data = response.json()
    if "data" not in data or not data["data"]:
        return None

    return data["data"]["title"]
