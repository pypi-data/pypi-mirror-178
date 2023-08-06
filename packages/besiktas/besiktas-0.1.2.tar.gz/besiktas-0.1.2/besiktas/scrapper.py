import requests
from bs4 import BeautifulSoup


class Scraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/39.0.2171.95 Safari/537.36 "
            }
        )

        response = self.session.get(
            url="https://www.transfermarkt.com.tr/besiktas-istanbul/startseite/verein/114/saison_id/2022"
        )
        response_team = self.session.get(
            url="https://www.transfermarkt.com.tr/besiktas-istanbul/startseite/verein/114/saison_id/2022"
        )
        self.soup = BeautifulSoup(response.content, "html.parser")
        self.teams = BeautifulSoup(response_team.content, "html.parser")

    @property
    def matches(self):
        return self.session.get("https://www.transfermarkt.com.tr/ceapi/nextMatches/team/114").json()

    @property
    def rumors(self):
        return self.session.get("https://www.transfermarkt.com.tr/ceapi/rumors/team/114").json()["rumors"]

    @property
    def team_value(self):
        data = self.soup.select_one("a.data-header__market-value-wrapper")
        data.select_one("p").clear()
        return data.get_text(strip=True)

    @property
    def cups(self):
        cups = []
        for each in self.soup.select(".data-header__badge-container a"):
            cups.append(
                [
                    each.select_one("span").get_text(strip=True),
                    each.get("title"),
                ]
            )
        return cups

    @property
    def standings(self):
        standings = []
        table = self.soup.find("div", attrs={"data-viewport": "Tabelle"})
        for each in table.select("tbody tr"):
            n, _, c, m, a, p = each.select("td")
            row = [
                n.get_text(strip=True),  # no
                c.get_text(strip=True),  # club
                m.get_text(strip=True),  # matches
                a.get_text(strip=True),  # average
                p.get_text(strip=True),  # points
                "table-highlight" in each.attrs.get("class", [])  # highlight
            ]
            standings.append(row)

        return standings

    @property
    def truths(self):
        table = self.soup.find("div", attrs={"data-viewport": "Daten_und_Fakten"})
        truths = {
            "legal_name": table.find("span", attrs={"itemprop": "legalName"}).get_text(strip=True),
            "address": " ".join([i.get_text(strip=True) for i in table.find_all("div", attrs={"itemprop": "address"})]),
            "telephone": table.find("span", attrs={"itemprop": "telephone"}).get_text(strip=True),
            "fax": table.find("span", attrs={"itemprop": "faxNumber"}).get_text(strip=True),
            "url": table.find("span", attrs={"itemprop": "url"}).get_text(strip=True),
            "founded": table.find("span", attrs={"itemprop": "foundingDate"}).get_text(strip=True),
            "members": table.find("span", attrs={"itemprop": "member"}).get_text(strip=True)
        }
        return truths

    @property
    def players(self):
        table = self.teams.find('table', attrs={'class': 'items'})
        # list of footballer names
        player = []
        players = table.find_all('img', attrs={'class': "bilderrahmen-fixed lazy lazy"})
        for row in players:
            player.append(str(str(row).split('" class', 1)[0].split('<img alt="', 1)[1]))
        position = []
        pos = [i.find_all('td')[-1] for i in table.find_all('table', attrs={'class': 'inline-table'})]
        for i in range(0, len(pos), 1):
            position.append(str(pos[i]).replace(" ", "").split('>', 1)[1].split('<', 1)[0].replace("\n", ""))

        players = {
            "Player": player,
            "Position": position
        }
        return players
