import requests
from requests.auth import *
import datetime
import json

def request_tweets(id, api_bearer):
    def bearer_oauth(r):
        r.headers["Authorization"] = f"Bearer {api_bearer}"
        r.headers["User-Agent"] = "v2UserLookupPython"
        return r

    url     = f'https://api.twitter.com/2/users/{id}/tweets?tweet.fields=created_at&max_results=100'
    res = requests.request('GET', url, auth=bearer_oauth)
    return res

def fetch_times(data):
    times = {}
    for tweet in data['data']:
        dt = datetime.datetime.strptime(tweet['created_at'][11:16], '%H:%M')
        dt = dt - datetime.timedelta(minutes=dt.minute % 30)
        if str(dt.time()) not in times:
            times[str(dt.time())] = 0
        else:
            times[str(dt.time())] += 1
    sortedKeys = sorted(times.keys())

    newTimes = {}
    for key in sortedKeys:
        newTimes[key] = times[key]

    return newTimes

def handle_rest_error(res):
    if (res.status_code == 401):
        print("Make sure your bearer token is correctly set in .secret file.")
        return
    print(res.text)

def main(id, bearer):
    res = request_tweets(id, bearer)
    if res.status_code != 200:
        handle_rest_error(res)
        return
    data = json.loads(res.text)
    try:
        times = fetch_times(data)
        f = open("data.js", "w")
        f.write("tweets=")
        json.dump(times, f)
        f.close()
    except:
        print("Error")
        print(data["errors"])
    print("Complete!")
    print("Open index.html to see results")

if __name__ == '__main__':
    try:
        api = open(".secret", "r")
        api_bearer = api.readline()
        api.close()
    except:
        print("Error: Could not find .secret file")
        exit(1)

    print("Visit https://tweeter.id.com/ to get your user id")
    try:
        id=int(input("Twitter ID: "))
    except:
        print("Error: Invalid ID")
        print("ID must be a number with no letters or spaces")
        exit(1)

    main(id, api_bearer)

    