import json
import os
import shutil

import pandas as pd
import requests
from bs4 import BeautifulSoup


class wallpaper:
    def __init__(self, main_tag, tags_included=[], tags_excluded=[]) -> None:
        self.main_tag = main_tag
        self.tags = tags_included
        self.tags_excluded = tags_excluded
        self.query = None

    def create_query_string(self):
        keywords_with_signs = ["+" + keyword for keyword in self.tags]
        exclusions_with_signs = ["-" + exclusion for exclusion in self.tags_excluded]
        query = (
            self.main_tag
            + " "
            + " ".join(keywords_with_signs)
            + "|"
            + " ".join(exclusions_with_signs)
        )
        self.query = query

    def send_request(self):
        print(self.query)
        self.main_tag = self.main_tag.replace(" ", "")
        request = f"https://wallhaven.cc/api/v1/search?q=+{self.main_tag}+-videogames+-digitalart+-videogameart+-games+-gaming"
        return requests.get(request)

    def process_data(self, link):
        data = json.loads(link.text)["data"]
        final = pd.DataFrame(data)
        print(final)
        return final

    def get_wallpaper(self):
        self.create_query_string()
        linkdata = self.send_request()
        return self.process_data(linkdata)

    def download_wallpaper(self, data):
        path = os.path.join(os.getcwd(), "wallpapers")
        if os.path.exists(os.path.join(os.getcwd(), "wallpapers")):
            pass
        else:
            os.mkdir(path)
        for i, dat in enumerate(data.index):
            link = data["url"][dat]
            print("working on", link)
            rr = requests.get(link).text
            Soup = BeautifulSoup(rr, "html5lib")
            img = Soup.find("img", {"id": "wallpaper"})
            fimg = requests.get(img["src"])
            type = data["file_type"][dat].split("/")[1]
            final = os.path.join(path, data["id"][dat] + "." + type)
            with open(final, "wb") as f:
                f.write(fimg.content)
            progress_percentage = i / len(data.index)
            yield f"Downloading wallpaper {i}/{len(data.index)}...", progress_percentage
        yield f"Downloading wallpaper {24}/{len(data.index)}...", 100


if __name__ == "__main__":
    wall = wallpaper(
        main_tag="Sports Car",
        tags_included=["Ferrari", "Lamborghini", "BMW"],
        tags_excluded=["gaming", "videoGames", "Anime"],
    )
    link = wall.get_wallpaper()
    wall.download_wallpaper(link)
