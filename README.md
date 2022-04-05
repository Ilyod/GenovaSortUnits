# GenovaSortUnits
Un petit programme Python permettant de trier en partie les unités de cours proposées par l'Université de Genova.

Auteur : Lucas D'aquaro


## Note d'intention

Hello ! Ceci est un petit programme que j'ai codé rapidement pour trier les différentes unités de cours proposées par l'université de Genova afin de m'aider à choisir celles que j'allais étudier durant mon erasmus. Je ne doute pas qu'il soit perfectible, bien sûr, notamment en l'optimisant (et puis Python n'est peut-être pas le langage le plus adapté, mais c'est celui que je maîtrisais le mieux à ce moment là), si jamais ça vous tente,
n'hésitez pas. Malgré tout, il m'a été bien utile, et je me suis dit qu'il pourrait l'être à d'autres, étant donné qu'aucun tri n'est proposé directement sur le site.
Tel que je l'ai fait, le tri se fait seulement sur la langue et le semestre, mais ça m'a tout de même permis de passer d'environ 5000 unités à un peu moins de 800, et ensuite, en regardant le nom des unités restantes, ça se fait finalement assez vite.

## Fonctionnement

Le fonctionnement du programme est simple :

* **1** - Récupération de la liste des unités de cours et des urls correspondant
* **2** - Pour chaque url, vérification du semestre et de la langue. Si le cours n'est pas en italien et au mauvais semestre, les informations sont récupérées dans une liste
* **3** - Un tableur .ods est créé avec les unités de cours retenues

Prévoyez du temps pour l'exécution, pour moi ça avait pris plus d'une heure.


**Bon courage, et surtout, profitez bien de votre semestre à Gênes !**

Lucas D'aquaro, entré à l'UTC en GI en A19
