from bs4 import BeautifulSoup
import requests
import datetime
from csv import writer
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

class WebScraper:
    def __init__(self):
        self.date = ""
        self.matches = []
        self.url = ""
        options = Options()
        options.add_argument("--log-level=3")
        options.headless = True
        self.driver = webdriver.Chrome(options=options, executable_path="C:\Program Files (x86)\chromedriver.exe")

    def getPreviousMatchInfo(self, date):
        self.date = date
        new_date = datetime.datetime.strptime(self.date, "%Y-%m-%d").date()
        targetDate = datetime.date.today() - datetime.timedelta(days=1)
        while new_date <= targetDate:
            self.url = "https://www.nba.com/games?date=" + str(new_date)
            page = requests.get(self.url)
            soup = BeautifulSoup(page.content, 'html.parser')
            contents = soup.find_all('section', class_="GameCard_gcMain__q1lUW")
            if len(contents) != 0:
                for content in contents:
                    score_1 = self.getScore1(content)
                    score_2 = self.getScore2(content)
                    team_1, team_2 = self.getTeams(content)
                    team_1_injured, team_2_injured = self.getInjuredPlayers(content)
                    winner = self.getWinner(team_1, team_2, score_1, score_2)
                    win_percent_1, win_percent_2 = self.getWinPercentage(content)
                    self.matches.append([team_1, team_2, team_1_injured, team_2_injured,
                                         win_percent_1, win_percent_2, team_2, str(new_date), winner])
            new_date += datetime.timedelta(days=1)
        self.driver.quit()

    def getInjuredPlayers(self, content):
        base_url = "https://www.nba.com"
        end_url = content.find('ul', class_="Tabs_tab__rnewb").findAll('li', class_="TabLink_tab__uKOPj")\
            [1].find('a', class_="Anchor_anchor__cSc3P TabLink_link__f_15h")
        self.driver.get(base_url + end_url['href'])
        try:
            team_1_names = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#__next > div.Layout_base__6IeUC.Layout_withShortStrip__krLX0.Layout_justNav__2H4H0 > div.Layout_mainContent__jXliI > div:nth-child(7) > section.Block_block__62M07.GameBoxscoreInactivePlayers_block__tJ3T6 > div > p:nth-child(2) > span.GameBoxscoreInactivePlayers_player__sop6b" ))
            )
            team_2_names = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#__next > div.Layout_base__6IeUC.Layout_withShortStrip__krLX0.Layout_justNav__2H4H0 > div.Layout_mainContent__jXliI > div:nth-child(7) > section.Block_block__62M07.GameBoxscoreInactivePlayers_block__tJ3T6 > div > p:nth-child(3) > span.GameBoxscoreInactivePlayers_player__sop6b"))
            )
        except:
            self.driver.refresh()
            team_1_names = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#__next > div.Layout_base__6IeUC.Layout_withShortStrip__krLX0.Layout_justNav__2H4H0 > div.Layout_mainContent__jXliI > div:nth-child(7) > section.Block_block__62M07.GameBoxscoreInactivePlayers_block__tJ3T6 > div > p:nth-child(2) > span.GameBoxscoreInactivePlayers_player__sop6b"))
            )
            team_2_names = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR,
                                                "#__next > div.Layout_base__6IeUC.Layout_withShortStrip__krLX0.Layout_justNav__2H4H0 > div.Layout_mainContent__jXliI > div:nth-child(7) > section.Block_block__62M07.GameBoxscoreInactivePlayers_block__tJ3T6 > div > p:nth-child(3) > span.GameBoxscoreInactivePlayers_player__sop6b"))
            )
        team_1_list = team_1_names.text.split(',')
        team_2_list = team_2_names.text.split(',')
        print(team_1_list, team_2_list)
        if len(team_1_list) == 0:
            team_1_list.append("None")
        elif len(team_2_list) == 0:
            team_2_list.append("None")
        return team_1_list, team_2_list

    def getWinPercentage(self, content):
        records = content.find_all('p', class_="MatchupCardTeamRecord_record__20YHe")
        record_1 = records[0].getText().split("-")
        record_1_wins = int(record_1[0])
        record_1_loss = int(record_1[1])
        record_1_total_games = record_1_wins + record_1_loss
        record_1_win_percentage = record_1_wins / record_1_total_games

        record_2 = records[1].getText().split("-")
        record_2_wins = int(record_2[0])
        record_2_loss = int(record_2[1])
        record_2_total_games = record_2_wins + record_2_loss
        record_2_win_percentage = record_2_wins / record_2_total_games
        return record_1_win_percentage, record_2_win_percentage


    def getTeams(self, content):
        teams = content.find_all('span', class_="MatchupCardTeamName_teamName__9YaBA")
        team_1 = teams[0].getText()
        team_2 = teams[1].getText()
        return team_1, team_2

    def getScore1(self, content):
        return content.find('div', class_="GameCardMatchup_matchupScoreCardWrapper__X50gw") \
                    .find('p', class_="MatchupCardScore_p__dfNvc GameCardMatchup_matchupScoreCard__owb6w").getText()

    def getScore2(self, content):
        return content.find('div', class_="GameCardMatchup_matchScorecardAlignRight__n20ov") \
            .find('p', class_="MatchupCardScore_p__dfNvc GameCardMatchup_matchupScoreCard__owb6w").getText()

    def getWinner(self, team_1, team_2, score_1, score_2):
        if int(score_1) > int(score_2):
            return team_1
        return team_2

    def generate_csv(self):
        with open('NBA.csv', 'w', encoding='utf8', newline='') as f:
            the_writer = writer(f)
            header = ["team_1", "team_2", "team_1_out", "team_2_out", "Team_1_win_%",
                      "Team_2_win_%", "homeTeam", "date", "winner"]
            the_writer.writerow(header)
            for i in range(len(self.matches)):
                the_writer.writerow(self.matches[i])