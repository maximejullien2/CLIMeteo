# CLIMeteo

CLIMeteo est une application permettant de récupérer les informations météorologique d'une ville.

## Installation 

Pour installer tous les packages nécessaires pour l'utilisation de l'application, lancez dans votre terminal bash:

```bash
./installation.sh
```

## Utilisation 

Il faudra tout d'abord créer une clé API [Open Weather Map](https://openweathermap.org) et la placer dans un fichier credentials.py qui contient:

```python
OWM_API_KEY = "YourAPIKey"
```

Ensuite, lancez dans votre terminal la commande suivante: 

```bash
python cliMeteo.py -city city [ -country country ]
```

## Sortie de l'application

Voici un exemple de résultat sorti:

## Interactions avec l'application

Une fois l'application lancée, vous pouvez appuyer sur:
- R, pour chercher les informations de météo sur un autre ville;
- P, pour afficher les pourcentages de chance qu'il pleuve;
- V, pour afficher la vitesse des vents;
- Barre espace, pour basculer entre les modes d'affichage (précipitation et vent); 
- Flèche de gauche ou de droite, pour parcourir les différentes dates/heures à afficher;
- I, pour changer le type d'icons;
- Ctrl+C, pour arrêter le programme.

## Documentation de l'API openWeatherMap

Voici le lien de la documentation de l'api d'openWeatherMap [documentation](https://openweathermap.org/api/hourly-forecast/)

## Librairies utilisées

* [Requests](https://requests.readthedocs.io/en/latest/)
* [GeoPy](https://geopy.readthedocs.io/en/stable/)
* [datetime](https://docs.python.org/3/library/datetime.html)
* [rich_](https://rich.readthedocs.io/en/latest/)
* [plotext](https://github.com/piccolomo/plotext)
* [asyncio](https://docs.python.org/3/library/asyncio.html)
* [prompt_toolkit](https://python-prompt-toolkit.readthedocs.io/en/master/)
* [rich_pixels](https://github.com/darrenburns/rich-pixels)
* [sys](https://docs.python.org/3/library/sys.htm)
* [os](https://docs.python.org/fr/3/library/os.html)
* [PIL](https://he-arc.github.io/livre-python/pillow/index.html)
