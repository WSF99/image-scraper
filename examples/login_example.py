import requests

url = "https://www.freeimages.com/ajax/user/signin"
username = "USERNAME_HERE"
password = "PASSWORD_HERE"

# We need to use the form data!
form_data = {
    "username": username,
    "password": password,
}

# We need to make a post request with the form_data.
response = requests.post(url, data=form_data)

# If ok!
if response.status_code == 200:
    # We must get the refresh and access tokens after a successfull request.
    print(response.text)
else:
    print(f"Failed to log-in. Status Code: {response.status_code}")
    print(response.text)  # Error response
