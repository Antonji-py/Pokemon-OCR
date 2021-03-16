import requests
from bs4 import BeautifulSoup


def get_product_url(expansion, full_name):
    name = full_name.split("=")[0]
    if len(full_name.split("=")) > 1:
        index = int(full_name.split("=")[1]) + 1
    else:
        index = 1

    query_url = f"https://www.cardmarket.com/en/Pokemon/Products/Singles/{expansion}?searchString={name}&idRarity=0&perSite=30"

    response = requests.get(query_url)
    soup = BeautifulSoup(response.text, "lxml")

    pokemon_types = soup.find_all("div", {"class": "col-10 col-md-8 px-2 flex-column align-items-start justify-content-center"})

    product_endpoint = [a["href"] for a in pokemon_types[index]][0]

    if "Online-Code-Card" in product_endpoint:
        product_endpoint = [a["href"] for a in pokemon_types[index + 1]][0]

    product_url = f"https://www.cardmarket.com{product_endpoint}"

    return product_url


def get_product_data(expansion, full_name):
    url = get_product_url(expansion, full_name)

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")

    dd_tags = soup.find_all("dd", {"class": "col-6 col-xl-7"})

    name = soup.find("h1").text.split(")")[0] + ")"
    rarity = [span["data-original-title"] for span in dd_tags[0]][0]
    available_items = dd_tags[3].text
    lowest_price = dd_tags[4].text
    if "We don't have enough data to draw a price chart" in response.text:
        price_trend = "-"
        average_price_30 = [span.text for span in dd_tags[5]][0]
        average_price_7 = [span.text for span in dd_tags[6]][0]
        average_price_1 = [span.text for span in dd_tags[7]][0]
    else:
        price_trend = [span.text for span in dd_tags[5]][0]
        average_price_30 = [span.text for span in dd_tags[6]][0]
        average_price_7 = [span.text for span in dd_tags[7]][0]
        average_price_1 = [span.text for span in dd_tags[8]][0]

    data = {
        "name": name,
        "rarity": rarity,
        "available_items": available_items,
        "lowest_price": lowest_price,
        "price_trend": price_trend,
        "average_price_30": average_price_30,
        "average_price_7": average_price_7,
        "average_price_1": average_price_1
    }

    return data
