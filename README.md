Šablona pro vývoj aplikace pro Tour de App společně s vytvořením a nahráním výstupu

## Lokální spuštění

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