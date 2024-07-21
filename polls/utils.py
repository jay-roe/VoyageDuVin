import os.path
from openpyxl import Workbook, load_workbook
from django.core.exceptions import ObjectDoesNotExist
from django.core.files import File
from polls.models import Wine, Tag, Session
from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
import argparse

from VoyageDuVin import settings

filename = "results.xlsx"
path = os.path.join(settings.MEDIA_ROOT, filename)

def create_workbook(session_ids):
    if not os.path.exists(settings.MEDIA_ROOT):
        os.makedirs(settings.MEDIA_ROOT, exist_ok=True)

    wb = Workbook()
    for session_id in session_ids:
        session = Session.objects.get(pk=session_id)
        wines = session.wines.order_by('order').all()

        ws = wb.create_sheet(title=f"Session_{session_id}")
        ws['A1'] = "Name"
        for idx, wine in enumerate(wines, start=1):
            ws[f'{chr(65 + idx)}1'] = wine.short_name

    if 'Sheet' in wb.sheetnames:
        wb.remove(wb['Sheet'])
    wb.save(path)


def add_score_excel(data, session_id):
    if not os.path.isfile(path):
        # Create workbook with at least one session sheet if it doesn't exist
        create_workbook([session_id])

    wb = load_workbook(filename=path)
    sheet_name = f"Session_{session_id}"
    if sheet_name not in wb.sheetnames:
        # Add a new sheet for the session if it doesn't exist
        session = Session.objects.get(pk=session_id)
        wines = session.wines.order_by('order').all()

        ws = wb.create_sheet(title=sheet_name)
        ws['A1'] = "Name"
        for idx, wine in enumerate(wines, start=1):
            ws[f'{chr(65 + idx)}1'] = wine.short_name
    else:
        ws = wb[sheet_name]
    ws.append(data)
    wb.save(path)


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

def _create_wines():
    try:
        wine = Wine.objects.get(short_name=" ".join(wineDict["name"].split(" ")[:-1]))
    except ObjectDoesNotExist as DoesNotExist:
        new_wine = Wine(
            short_name=" ".join(wineDict["name"].split(" ")[:-1]),
            full_name=wineDict["name"],
            image=wineDict["photo_url"],
            order=1,
            variety=wineDict["grape_variety"],
            region=wineDict["country"],
            alcohol_content=float(wineDict["degree_alcohol"].split(" ")[0].replace(",", ".")),
            sweetness=float(wineDict["sugar_content"].split(" ")[0].replace(",", ".").replace("<","")),
            color=wineDict["color"],
            price=float(wineDict["price"].split(u'\xa0')[0].replace(",", "."))
        )

        # Download the image from photo_url and save it to the Wine object
        img_temp = urlopen(wineDict["photo_url"])
        image_name = wineDict["name"] + ".jpg"  # Adjust the name as needed
        # Assign the downloaded image to the 'image' field of your new_wine object
        new_wine.image.save(image_name, File(img_temp), save=True)
        new_wine.save()
    

        # Adding tags to the newly created Wine object
        for key, feature in wineDict["special_feature_photo_url"].items():
            # Check if the tag exists or create a new one
            tag, created = Tag.objects.get_or_create(name=key)
            if created:
                tag_image_name = key + ".jpg"
                tag_img_temp = urlopen(feature)
                tag.image.save(tag_image_name, File(tag_img_temp), save=True)

            new_wine.tags.add(tag)




def _scrape_wines(line):
    r = requests.get(line)
    soup = BeautifulSoup(r.content, "html.parser")
    # Extracting wine name
    wine_name = soup.find("h1", class_="page-title").text.strip()
    wineDict["name"] = wine_name

    # Extracting price
    price = soup.find("span", class_="price").text.strip()
    wineDict["price"] = price

    # Extracting country
    try:
        country = soup.find("strong", attrs={"data-th": "Pays"}).text.strip()
        wineDict["country"] = country
        
        # Extracting region
        try:
            region = soup.find("strong", attrs={"data-th": "Région"}).text.strip()
            wineDict["country"] = wineDict["country"] + ", " + region
        except:
            pass
    except:
        pass

    # Extracting regulated designation
    regulated_designation = soup.find("strong", attrs={"data-th": "Désignation réglementée"}).text.strip()
    wineDict["regulated_designation"] = regulated_designation

    try:
        # Extracting grape variety
        grape_variety = soup.find("strong", attrs={"data-th": "Cépage"}).text.strip()
        wineDict["grape_variety"] = grape_variety
    except:
        pass

    # Extracting degree of alcohol
    degree_alcohol = soup.find("strong", attrs={"data-th": "Degré d'alcool"}).text.strip()
    wineDict["degree_alcohol"] = degree_alcohol

    # Extracting sugar content
    try:
        sugar_content = soup.find("strong", attrs={"data-th": "Taux de sucre"}).text.strip()
        wineDict["sugar_content"] = sugar_content
    except:
        wineDict["sugar_content"] = "-1,1"

    # Extracting color
    color = soup.find("strong", attrs={"data-th": "Couleur"}).text.strip()
    wineDict["color"] = color
    
    # Extracting special features
    try:
        special_features = soup.find("strong", attrs={"data-th": "Particularité"}).text.strip().split(", ")
        wineDict["special_feature"] = special_features
    except:
        wineDict["special_feature"] = []

    # Extracting size
    size = soup.find("strong", attrs={"data-th": "Format"}).text.strip()
    wineDict["size"] = size

    # Extracting producer
    producer = soup.find("strong", attrs={"data-th": "Producteur"}).text.strip()
    wineDict["producer"] = producer

    # Extracting SAQ code
    saq_code = soup.find("strong", attrs={"data-th": "Code SAQ"}).text.strip()
    wineDict["saq_code"] = saq_code

    photo_url = soup.find("div", attrs={"id": "mtImageContainer"}).find("img", attrs={"itemprop": "image"})["src"]
    wineDict["photo_url"] = photo_url
    
    try:
        special_feature_photo_url = soup.find("div", attrs={"class", "wrapper-special-features"}).findAll("img")
        wineDict["special_feature_photo_url"] = {img["alt"].split(":")[1].strip(): img["src"] for img in special_feature_photo_url}
    except:
        wineDict["special_feature_photo_url"] = {}

def handle_new_wines(file):
    print(file)
    file =  open(file, "r")
    lines = file.readlines()
    for line in lines:
        _scrape_wines(line.strip())
        _create_wines()