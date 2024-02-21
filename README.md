# CLIMeteo

CLIMeteo est une application permettant de récupérer les informations météorologique d'une ville .

## Installation 
Pour installer tous les packages nécessaires pour l'utilisation de l'application , lancez dans votre terminal bash :

```bash
./installation.sh
```

## Utilisation 

Il faudra tout d'abord créer une clée API [Open Weather Map](https://openweathermap.org) et la placer dans un fichier credentials.py qui contient :

```python
OWM_API_KEY = "YourAPIKey"
```

Ensuite, lancez dans votre terminal la commande suivante : 

```bash
python cliMeteo.py -city city [ -country country -mode 1]
```

## Sortie de l'application

Voici un exemple de résultat sorti :



## Librairie utilisé
* [Requests](https://requests.readthedocs.io/en/latest/)
* [GeoPy](https://geopy.readthedocs.io/en/stable/)
* [datetime](https://docs.python.org/fr/3/library/datetime.html)
* [rich_](https://rich.readthedocs.io/en/latest/)
* [plotext](https://github.com/piccolomo/plotext)
* [asyncio](https://docs.python.org/3/library/asyncio.html)
* [prompt_toolkit](https://python-prompt-toolkit.readthedocs.io/en/master/)
