# scrapper-rolandgarros

Ce scrapper permet de récupérer l'ensemble des données des tableaux masculin et féminin du tournoi de Roland-Garros sur le site du journal l'équipe.


Utilisation : 
pip install requirements.txt

scrapy crawl rg_lequipe

Génère un fichier results.json à la racine du projet avec la structure suivante : 



[
{"year": "1968", "tournament": "SINGLES_MAN", "player": "Rosewall", "nationality": "AUS", "performance": "WINNER_FINAL"},
{"year": "1968", "tournament": "SINGLES_MAN", "player": "Edlefsen", "nationality": "USA", "performance": "DEFEAT_FIRST_ROUND"},
{"year": "1968", "tournament": "SINGLES_MAN", "player": "Stubs", "nationality": "AUS", "performance": "DEFEAT_SECOND_ROUND"},

(...)
]



# licence GNU 3.0

