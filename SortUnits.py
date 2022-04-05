'''
**Note d'intention**
Hello ! Ceci est un petit programme que j'ai codé rapidement pour trier les différentes unités de cours proposées
par l'université de Genova afin de m'aider à choisir celles que j'allais étudier durant mon erasmus.
Je ne doute pas qu'il soit perfectible, bien sûr, notamment en l'optimisant (et puis Python n'est peut-être pas le
langage le plus adapté, mais c'est celui que je maîtrisais le mieux à ce moment là), si jamais ça vous tente,
n'hésitez pas. Malgré tout, il m'a été bien utile, et je me suis dit qu'il pourrait l'être à d'autres, étant donné
qu'aucun tri n'est proposé directement sur le site.
Tel que je l'ai fait, le tri se fait seulement sur la langue et le semestre, mais ça m'a tout de même permis de
passer d'environ 5000 unités à un peu moins de 800, et ensuite en regardant le nom des unités restantes, ça se fait
finalement assez vite.

**Fonctionnement**
Le fonctionnement du programme est simple :
1 - Récupération de la liste des unités de cours et des urls correspondant
2 - Pour chaque url, vérification du semestre et de la langue. Si le cours n'est pas en italien et au mauvais semestre, les informations sont récupérées dans une liste
3 - Un tableur .ods est créé avec les unités de cours retenues
Prévoyez du temps pour l'exécution, pour moi ça avait pris plus d'une heure.

Bon courage, et surtout, profitez bien de votre semestre à Gênes !

Lucas D'aquaro, entré à l'UTC en GI en A19
'''


import os
import requests
from bs4 import BeautifulSoup
import pyexcel

# --- Paramètres ---
annee = "2021"                                      # ex: 2021 pour l'année 2021/2022
mauvaisSemestre = "1"                               # ex: "1" pour garder les cours du 2e semestre
nomTableur = "Genova_sorted_units.ods"                                  # Nom du tableur généré
dossierTableur = os.path.join(os.environ['USERPROFILE'], 'Desktop')     # Chemin du dossier du tableur


def getAllUvs():
    # Retourne la liste des url incomplètes des UVs (ex: "/en/off.f/2021/ins/48177")
    res = requests.get('https://unige.it/en/off.f/'+ annee +'/ins/index')
    if not res.ok:
        raise Exception('open url error')

    soup = BeautifulSoup(res.text, 'html.parser')
    listeUvs = []
    UvPrec = ''
    for tag in soup.find_all("a"):
        Uv = tag.get('href')
        if Uv and "/en/off.f/2021/ins/" in Uv and Uv != UvPrec:
            UvPrec = Uv
            listeUvs.append(Uv)

    return listeUvs


def testUv(finUrl):
    # Récupère les informations de l'UV et vérifie la langue et le semestre
    url = 'https://unige.it' + finUrl
    res = requests.get(url)
    if not res.ok:
        raise Exception('open url error: {}'.format(url))
    release_html = res.text

    soup = BeautifulSoup(release_html, 'html.parser')

    uv = {'Lien': url, 'Nom':'', 'Code':'', 'Langue':'', 'Semestre':'', 'Lieu':'', 'Credits':''}
    flag = ''
    textBadSemester = mauvaisSemestre + '° Semester'
    for tag in soup.find_all("div"):
        texte = tag.text

        if flag == 'code':
            flag = ''
            uv['Code'] = texte

        if flag == 'langue':
            flag = ''
            # Si la langue est seulement 'italien', on ne prend pas l'uv
            if texte == 'Italian':
                return None
            uv['Langue'] = texte

        if flag == 'semestre':
            flag = ''
            # Si le semestre n'est pas bon, on ne prend pas l'uv
            if texte == 'Annual' or texte == textBadSemester:
                return None
            uv['Semestre'] = texte

        if flag == 'lieu':
            flag = ''
            uv['Lieu'] = texte

        if flag == 'credits':
            flag = ''
            uv['Credits'] = texte

        if texte == 'Code':
            flag = 'code'
        if texte == 'CREDITS':
            flag = 'credits'
        if texte == 'LANGUAGE':
            flag = 'langue'
        if texte == 'TEACHING LOCATION':
            flag = 'lieu'
        if texte == 'semester':
            flag = 'semestre'

    uv['Nom'] = soup.find("title").text

    return uv


def getSortedUv(listeUrlUvs = None):
    # Fonction principale, crée le tableur avec les unités triées
    if listeUrlUvs:
        AllUvs = listeUrlUvs
    else:
        print("Obtention de la liste des UVs...")
        # Liste de la fin des urls de toutes les Uvs
        AllUvs = getAllUvs()
        print("Liste obtenue.\n")

    # Liste de dictionnaires correspondant aux UVs
    UvsSorted = []

    print("\nTest des UVs...")
    for compteur in range(len(AllUvs)):
        print(compteur)
        #if compteur%25 == 0:
            #print(compteur, " UVs testées")

        # Décommenter les 2 lignes suivantes pour tester
        #if compteur == 15:
            #break

        try:
            uv = testUv(urlUv)
        except:
            print("Erreur Uvs n.", compteur, ", url : ", AllUvs[compteur])
            continue
        # Si l'uv est en italien ou pas au bon semestre, uv vaut None. Sinon, on l'ajoute.
        if uv:
            UvsSorted.append(uv)


    print("Les ", compteur, " Uvs ont été testées.")

    # Création du tableau avec les UVs
    try:
        pyexcel.save_as(records=UvsSorted, dest_file_name=os.path.join(dossierTableur, nomTableur))
        print("\nLe tableur récapitulatif a été créé.\n")
    except:
        print("Le tableur n'a pas pu être créé.'")

    return UvsSorted
