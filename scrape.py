import requests
from bs4 import BeautifulSoup
url = "https://codeforces.com/ratings/organization/314"


def top10():
    r = requests.get(url)
    htmlContent = r.text

    soup = BeautifulSoup(htmlContent, 'lxml')
    mainPage = soup.find('div', class_="content-with-sidebar")
    user = mainPage.find_all('a', class_="rated-user", limit=10)

    users = []

    for user in user: 
        user_name = user.text
        users.append(user_name)

    return users




