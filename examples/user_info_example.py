import requests

url = "https://www.freeimages.com/ajax/user/me"

access_token = "PLACE HERE YOUR ACCESS TOKEN"
headers = {"Authorization": f"Bearer {access_token}"}

# We need to make a get request with the headers.
response = requests.get(url, headers=headers)

# If ok!
if response.status_code == 200:
    # We must get the user info after a successfull request.
    print(response.text)
else:
    print(f"Error. Status Code: {response.status_code}")
    print(response.text)  # Error response
