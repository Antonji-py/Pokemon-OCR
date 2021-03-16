import requests
import time
from datetime import datetime
from bs4 import BeautifulSoup

start_time = time.time()

soup = BeautifulSoup(requests.get("https://www.pokellector.com/sets/SWSH45-Shining-Fates").text, "lxml")
images = soup.find_all("img", {"class": "card lazyload"})

done_names = []

for i, img in enumerate(images):
    name = img["data-src"].split("/")[-1].split(".")[0]
    img_url = img["data-src"].replace(".thumb", "")

    response = requests.get(img_url).content

    if name in done_names:
        name = name + "-shiny"
    done_names.append(name)

    with open(f"imagesQuery/{name}.png", "wb+") as file:
        file.write(response)

    print(f"{datetime.now()}    {name}    {i+1}/{len(images)}")
    time.sleep(0.1)

print(time.time() - start_time)
