# scrapper-rolandgarros

Ce scrapper permet de récupérer l'ensemble des données des tableaux masculin et féminin du tournoi de Roland-Garros sur le site du journal l'équipe.

## Input 
Voir https://www.lequipe.fr/Tennis/roland-garros/epreuve-simple-messieurs/annee-1976/page-tableau-tournoi

## Output 
[
{"year": "1968", "tournament": "SINGLES_MAN", "player": "Rosewall", "nationality": "AUS", "performance": "WINNER_FINAL"},
{"year": "1968", "tournament": "SINGLES_MAN", "player": "Edlefsen", "nationality": "USA", "performance": "DEFEAT_FIRST_ROUND"},
{"year": "1968", "tournament": "SINGLES_MAN", "player": "Stubs", "nationality": "AUS", "performance": "DEFEAT_SECOND_ROUND"},

(...)
]


Vous pouvez utiliser le résultat déjà généré dans ce repo (fichier results.json)

Ou si besoin, vous pouvez regénérer les données :


pip install requirements.txt


scrapy crawl rg_lequipe



# licence GNU 3.0

