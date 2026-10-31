# MTG Card Match Finder

Busca cartas que quieres comprar dentro de listas de cartas disponibles en Magic: The Gathering. La configuración mantiene separadas las listas de cartas buscadas y las listas de cartas a la venta.

## Requisitos

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Configuración

Edita `config/wanted-card-lists.yaml` para indicar las listas que contienen las cartas que buscas:

```yaml
lists:
  - https://moxfield.com/decks/example
```

Edita `config/sale-card-lists.yaml` para indicar las listas con cartas disponibles para comprar:

```yaml
lists:
  - https://manabox.app/decks/example
```

Se pueden añadir varias URLs a cada archivo.

## Uso

Desde la raíz del proyecto:

```bash
python src/main.py
```

El resultado se guarda en `output/card-matches.yaml`. Cada coincidencia incluye las cantidades buscadas y disponibles, además de las URLs de las listas donde aparece la carta:

```yaml
matches:
  - card: Sol Ring
    wanted_quantity: 1
    available_quantity: 1
    sale_links:
      - https://manabox.app/decks/example
```

Por defecto se incluyen el maindeck y el sideboard. Para excluir el sideboard:

```bash
python src/main.py --without-sideboard
```

También se pueden cambiar los archivos de configuración y salida:

```bash
python src/main.py --wanted-config config/wanted-card-lists.yaml --sale-config config/sale-card-lists.yaml --output output/card-matches.yaml
```

## Pruebas

```bash
python -m unittest discover -s tests
```
