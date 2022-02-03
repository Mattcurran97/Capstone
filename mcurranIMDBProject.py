#Matt curran

import requests
import secrets


def main():


    wot = f"https://imdb-api.com/en/API/UserRatings/{secrets.My_key}/tt7462410"
    response = requests.get(wot)
    if response.status_code != 200:
        print("Not looking good")
        return
    data = response.json()
    print(data)

    first = f"https://imdb-api.com/en/API/UserRatings/{secrets.My_key}/tt5491994"
    response = requests.get(first)
    if response.status_code != 200:
        print("Not looking good")
        return
    data = response.json()
    print(data)

    fifty = f"https://imdb-api.com/en/API/UserRatings/{secrets.My_key}/tt2297757"
    response = requests.get(fifty)
    if response.status_code != 200:
        print("Not looking good")
        return
    data = response.json()
    print(data)

    hundred = f"https://imdb-api.com/en/API/UserRatings/{secrets.My_key}/tt0286486"
    response = requests.get(hundred)
    if response.status_code != 200:
        print("Not looking good")
        return
    data = response.json()
    print(data)

    twohundred = f"https://imdb-api.com/en/API/UserRatings/{secrets.My_key}/tt1492966"
    response = requests.get(twohundred)
    if response.status_code != 200:
        print("Not looking good")
        return
    data = response.json()
    print(data)

    topTV = f"https://imdb-api.com/en/API/Top250TVs/{secrets.My_key}"
    response = requests.get(topTV)
    if response.status_code != 200:
        print("Not looking good")
        return
    data = response.json()
    print(data)

    with open('data.txt', 'a') as file:
        for item in data:
            print(item, file=file)


if __name__ == '__main__':
    main()


