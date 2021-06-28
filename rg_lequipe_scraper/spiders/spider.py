import scrapy
import re
import logging
from scrapy.crawler import CrawlerProcess


class RGScrapper(scrapy.Spider):
    name = "rg_lequipe"

    def start_requests(self):

        YEAR_MIN = 1968
        YEAR_MAX = 2020

        years = [i for i in range(YEAR_MIN, YEAR_MAX+1)]
        
        base_url = 'https://www.lequipe.fr/Tennis/roland-garros/epreuve-simple-{genre}/annee-{yyyy}/page-tableau-tournoi/tour-1'

        urls = [base_url.format(yyyy=y,genre="messieurs") for y in years] # voilà pour les hommes
        urls = urls + [base_url.format(yyyy=y,genre="dames") for y in years] # voilà pour les dames

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        
        all_players = list(map(str.strip,response.xpath("//div[@infos-round='0']//span[@class='TennisScore__player' or @class='TennisScore__player TennisScore__player--french']/text()").extract()))
        all_nationalities = list(map(lambda url: re.findall("\/([A-Z]+)\/",url)[0],response.xpath("//div[@infos-round='0']//div[@class='TennisScore__flag']/img/@data-src").extract()))
        
        winners_first_round = list(map(str.strip,response.xpath("//div[@infos-round='0']//div[contains(@class,'TennisScore__name--winner')]/span/text()").extract()))
        winners_second_round = list(map(str.strip,response.xpath("//div[@infos-round='1']//div[contains(@class,'TennisScore__name--winner')]/span/text()").extract()))
        winners_third_round = list(map(str.strip,response.xpath("//div[@infos-round='2']//div[contains(@class,'TennisScore__name--winner')]/span/text()").extract()))
        winners_huitiemes = list(map(str.strip,response.xpath("//div[@infos-round='3']//div[contains(@class,'TennisScore__name--winner')]/span/text()").extract()))
        winners_quarts = list(map(str.strip,response.xpath("//div[@infos-round='4']//div[contains(@class,'TennisScore__name--winner')]/span/text()").extract()))
        winners_demis = list(map(str.strip,response.xpath("//div[@infos-round='5']//div[contains(@class,'TennisScore__name--winner')]/span/text()").extract()))
        winner_finale = list(map(str.strip,response.xpath("//div[@infos-round='6']//div[contains(@class,'TennisScore__name--winner')]/span/text()").extract()))

        losers_first_round = [player for player in all_players if player not in winners_first_round]
        losers_second_round = [player for player in winners_first_round if player not in winners_second_round]
        losers_third_round = [player for player in winners_second_round if player not in winners_third_round]
        losers_huitiemes = [player for player in winners_third_round if player not in winners_huitiemes]
        losers_quarts = [player for player in winners_huitiemes if player not in winners_quarts]
        losers_demis = [player for player in winners_quarts if player not in winners_demis]
        loser_finale = [player for player in winners_demis if player not in winner_finale]

        for i in range(0, len(all_players)):
            player = all_players[i]
            nationality = all_nationalities[i]

            logging.info(response.request.url)
            year = re.findall("annee-(\d*)\/",response.request.url)[0]
            genre = re.findall("epreuve-simple-(.*)\/annee", response.request.url)[0]

            if (player in losers_first_round):
                performance = "DEFEAT_FIRST_ROUND"
            elif (player in losers_second_round):
                performance = "DEFEAT_SECOND_ROUND"
            elif (player in losers_third_round):
                performance = "DEFEAT_THIRD_ROUND"
            elif(player in losers_huitiemes):
                performance = "DEFEAT_ROUND_OF_16"
            elif(player in losers_quarts):
                performance = "DEFEAT_ROUND_OF_8"
            elif(player in losers_quarts):
                performance = "DEFEAT_QUARTER_FINALS"
            elif(player in losers_demis):
                performance = "DEFEAT_SEMI_FINALS"
            elif(player in loser_finale):
                performance = "DEFEAT_FINAL"
            elif(player in winner_finale):
                performance = "WINNER_FINAL"
            else:
                performance = "ERROR_PLAYER_NOT_FOUND"
            
            yield {
                'year': year,
                'tournament' : "SINGLES_MAN" if genre =="messieurs" else "SINGLES_WOMAN",
                'player': player,
                'nationality': nationality,
                'performance': performance
            }


filename = "results.json"

process = CrawlerProcess(settings={
    'CSV_DELIMITER' : ';',
    'FEED_FORMAT': 'json',
    'FEED_URI': filename,
    'COOKIES_ENABLED' : 'False'
})
                
process.crawl(RGScrapper)
process.start() # the script will block here until the crawling is finished