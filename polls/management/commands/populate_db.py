from django.core.management.base import BaseCommand
from django.core.files import File
from polls.models import Wine, Tag
from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
import argparse

class Command(BaseCommand):
    args = '[saq_urls]'
    help = 'our help string comes here'
    wineDict = {
        "name": "",
        "price": "",
        "country": "",
        "region": "",
        "regulated_designation": "",
        "grape_variety": "",
        "degree_alcohol": "",
        "sugar_content": "",
        "color": "",
        "special_feature": [],
        "size": "",
        "producer": "",
        "saq_code": "",
        "photo_url": "",
        "special_feature_photo_url": {}
    }

    def _create_wines(self):
        try:
            wine = Wine.objects.get(short_name=" ".join(self.wineDict["name"].split(" ")[:-1]))
        except DoesNotExist:
            new_wine, created = Wine(
                short_name=" ".join(self.wineDict["name"].split(" ")[:-1]),
                full_name=self.wineDict["name"],
                image=self.wineDict["photo_url"],
                order=1,
                variety=self.wineDict["grape_variety"],
                region=self.wineDict["country"],
                alcohol_content=float(self.wineDict["degree_alcohol"].split(" ")[0].replace(",", ".")),
                sweetness=float(self.wineDict["sugar_content"].split(" ")[0].replace(",", ".")),
                color=self.wineDict["color"],
                price=float(self.wineDict["price"].split(u'\xa0')[0].replace(",", "."))
            )

            # Download the image from photo_url and save it to the Wine object
            img_temp = urlopen(self.wineDict["photo_url"])
            image_name = self.wineDict["name"] + ".jpg"  # Adjust the name as needed
            # Assign the downloaded image to the 'image' field of your new_wine object
            new_wine.image.save(image_name, File(img_temp), save=True)
            new_wine.save()
        

            # Adding tags to the newly created Wine object
            for key, feature in self.wineDict["special_feature_photo_url"].items():
                # Check if the tag exists or create a new one
                tag, created = Tag.objects.get_or_create(name=key)
                if created:
                    tag_image_name = key + ".jpg"
                    tag_img_temp = urlopen(feature)
                    tag.image.save(tag_image_name, File(tag_img_temp), save=True)

                new_wine.tags.add(tag)




    def _scrape_wines(self, line):
        r = requests.get(line)
        soup = BeautifulSoup(r.content, "html.parser")
        # Extracting wine name
        wine_name = soup.find("h1", class_="page-title").text.strip()
        self.wineDict["name"] = wine_name

        # Extracting price
        price = soup.find("span", class_="price").text.strip()
        self.wineDict["price"] = price

        # Extracting country
        try:
            country = soup.find("strong", attrs={"data-th": "Pays"}).text.strip()
            self.wineDict["country"] = country
            
            # Extracting region
            try:
                region = soup.find("strong", attrs={"data-th": "Région"}).text.strip()
                self.wineDict["country"] = self.wineDict["country"] + ", " + region
            except:
                pass
        except:
            pass

        # Extracting regulated designation
        regulated_designation = soup.find("strong", attrs={"data-th": "Désignation réglementée"}).text.strip()
        self.wineDict["regulated_designation"] = regulated_designation

        # Extracting grape variety
        grape_variety = soup.find("strong", attrs={"data-th": "Cépage"}).text.strip()
        self.wineDict["grape_variety"] = grape_variety

        # Extracting degree of alcohol
        degree_alcohol = soup.find("strong", attrs={"data-th": "Degré d'alcool"}).text.strip()
        self.wineDict["degree_alcohol"] = degree_alcohol

        # Extracting sugar content
        try:
            sugar_content = soup.find("strong", attrs={"data-th": "Taux de sucre"}).text.strip()
            self.wineDict["sugar_content"] = sugar_content
        except:
            self.wineDict["sugar_content"] = "-1,1"

        # Extracting color
        color = soup.find("strong", attrs={"data-th": "Couleur"}).text.strip()
        self.wineDict["color"] = color
        
        # Extracting special features
        try:
            special_features = soup.find("strong", attrs={"data-th": "Particularité"}).text.strip().split(", ")
            self.wineDict["special_feature"] = special_features
        except:
            self.wineDict["special_feature"] = []

        # Extracting size
        size = soup.find("strong", attrs={"data-th": "Format"}).text.strip()
        self.wineDict["size"] = size

        # Extracting producer
        producer = soup.find("strong", attrs={"data-th": "Producteur"}).text.strip()
        self.wineDict["producer"] = producer

        # Extracting SAQ code
        saq_code = soup.find("strong", attrs={"data-th": "Code SAQ"}).text.strip()
        self.wineDict["saq_code"] = saq_code

        photo_url = soup.find("div", attrs={"id": "mtImageContainer"}).find("img", attrs={"itemprop": "image"})["src"]
        self.wineDict["photo_url"] = photo_url
        
        try:
            special_feature_photo_url = soup.find("div", attrs={"class", "wrapper-special-features"}).findAll("img")
            self.wineDict["special_feature_photo_url"] = {img["alt"].split(":")[1].strip(): img["src"] for img in special_feature_photo_url}
        except:
            self.wineDict["special_feature_photo_url"] = {}

    def add_arguments(self, parser):
        parser.add_argument('--file', type=argparse.FileType('r'))

    def handle(self, *args, **options):
        file = options["file"]
        lines = file.readlines()
        for line in lines:
            self._scrape_wines(line.strip())
            self._create_wines()



# English version
''' 
# Extracting wine name
        wine_name = soup.find("h1", class_="page-title").text.strip()
        self.wineDict["name"] = wine_name

        # Extracting price
        price = soup.find("span", class_="price").text.strip()
        self.wineDict["price"] = price

        # Extracting country
        country = soup.find("strong", attrs={"data-th": "Country"}).text.strip()
        self.wineDict["country"] = country

        # Extracting regulated designation
        regulated_designation = soup.find("strong", attrs={"data-th": "Regulated Designation"}).text.strip()
        self.wineDict["regulated_designation"] = regulated_designation

        # Extracting grape variety
        grape_variety = soup.find("strong", attrs={"data-th": "Grape variety"}).text.strip()
        self.wineDict["grape_variety"] = grape_variety

        # Extracting degree of alcohol
        degree_alcohol = soup.find("strong", attrs={"data-th": "Degree of alcohol"}).text.strip()
        self.wineDict["degree_alcohol"] = degree_alcohol

        # Extracting sugar content
        sugar_content = soup.find("strong", attrs={"data-th": "Sugar content"}).text.strip()
        self.wineDict["sugar_content"] = sugar_content

        # Extracting color
        color = soup.find("strong", attrs={"data-th": "Color"}).text.strip()
        self.wineDict["color"] = color

        # Extracting special features
        special_features = soup.find("strong", attrs={"data-th": "Special feature"}).text.strip().split(", ")
        self.wineDict["special_feature"] = special_features

        # Extracting size
        size = soup.find("strong", attrs={"data-th": "Size"}).text.strip()
        self.wineDict["size"] = size

        # Extracting producer
        producer = soup.find("strong", attrs={"data-th": "Producer"}).text.strip()
        self.wineDict["producer"] = producer

        # Extracting SAQ code
        saq_code = soup.find("strong", attrs={"data-th": "SAQ code"}).text.strip()
        self.wineDict["saq_code"] = saq_code

        photo_url = soup.find("div", attrs={"id": "mtImageContainer"}).find("img", attrs={"itemprop": "image"})["src"]
        self.wineDict["photo_url"] = photo_url
'''