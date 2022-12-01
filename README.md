# Tour de App - Flask boiler plate

Šablona pro vývoj aplikace pro Tour de App společně s vytvořením a nahráním výstupu

## Lokální spuštění

### Python

#### Prerekvizity
- Python 3 (pokud nemáš python nainstalovaný, podívej se na https://naucse.python.cz/course/pyladies/)
- pipenv (odkaz na jak přidat pipenv na windows, `pip install --user pipenv` pro Windows, https://pypi.org/project/pipenv/#installation pro Linux dle distribuce) 
#### Spuštění


```
pipenv install
pipenv shell
````

Windows
````
flask --app app\app.py init-db
flask --app app\app.py run
````


Linux / macOS
````
flask --app app/app.py init-db
flask --app app/app.py run
````
Aplikace bude přístupná na `http://127.0.0.1:5000`

### Docker 
#### Prerekvizity
- Docker
- (Windows) aktivovaný wsl2 

#### Spuštění
```
docker build . -t tda-flask
docker run -p 8080:80 -v ${PWD}:/app tda-flask
```


Aplikace bude přístupná na `http://127.0.0.1:8080`

## Virtuální prostředí a správa balíčků

Je využit nástroj [Pipenv](https://pypi.org/project/pipenv/), který kombinuje pip a virtualenv. 

## Odevzdání
V rámci GitHub akce se aplikace automaticky odevzdává, jediné co je potřeba udělat je v rámci repozitáře si nastavit svůj vlastní TEAM\_SECRET, který dostanete po registraci do soutěže
