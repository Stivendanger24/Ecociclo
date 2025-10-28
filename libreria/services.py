import requests

def get_current_datetime():
    try:
        response = requests.get('http://localhost:5000/api/get-current-datetime')
        if response.status_code == 200:
            return response.json().get('datetime', None)
        else:
            return None
    except requests.RequestException as e:
        print(f"Error fetching datetime: {e}")
        return None