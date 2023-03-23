import requests
from bs4 import BeautifulSoup
import json


mainUrl = "https://yaniperfume.com"

request = requests.get(mainUrl + "/product/all")
soup = BeautifulSoup(request.text, "html.parser")

for i in soup.find_all('div', {"class": "grid-item iso-item web px-2"}):

    # Product URL
    productDetails = i.find(
        "div", {"class": "prooduct-img-container"})
    productUrl = productDetails.get("onclick")[14:-2]
    print("Product - " + str(productDetails.get("onclick")[31:-2]))

    # Main Image
    productMainImage = i.find("img", {"class": "d-block w-100 main-img"})
    productMainImageSource = productMainImage.get("src")

    # Brand Image
    productBrandImage = i.find("img", {"class": "rounded-circle my-group"})
    productBrandImageSource = productBrandImage.get("src")

    # Details
    productDetailsRequest = requests.get(mainUrl + productUrl)
    productDetailsSoup = BeautifulSoup(
        productDetailsRequest.text, "html.parser")

    # Data
    productData = {
        "title": productDetailsSoup.find("h5", {"class": "h5 text-dark"}).get_text(separator=" ", strip=True),
        "description": productDetailsSoup.find("p", {"class": "text-muted"}).get_text(separator=" ", strip=True),
        "pricePerGeram": productDetailsSoup.find("p", {"class": "pt-1 text-dark"}).get_text(separator=" ", strip=True)[12:].strip(),
        "productImage": mainUrl + productMainImageSource,
        "productBrandImage": mainUrl + productBrandImageSource
    }

    with open(str(productUrl[17::]) + ".json", "w", encoding='utf-8') as productFile:
        json.dump(productData, productFile, indent=4, ensure_ascii=False)
