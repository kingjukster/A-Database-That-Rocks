import requests
from bs4 import BeautifulSoup
import csv
import re

# URL of the Wikipedia page
url = "https://en.wikipedia.org/wiki/List_of_rock_types"

response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

targetHeadings = ["Igneous rocks", "Sedimentary rocks", "Metamorphic rocks"]
targetClasses = ["Plutonic", "Intrusive", "Volcanic", "Extrusive", "Clastic", "Clay", "Silt", "Sand", "Gravel", "Cobbles", "Boulders", "Foliated", "Schists", "Gneiss", "Slates", "Phyllites", "Mylonite", "Marble", "Soapstone", "Serpentine"]
with open("rock.csv", "w", newline="", encoding="utf-8") as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(["Name", "Class", "SubClass"])
    for target in targetHeadings:
        # Find the target heading by locating the h2 or h3 tag that contains class name
        heading = soup.find(lambda tag: tag.name in ["h2", "h3"] and target in tag.text)
        if heading:
            ul = heading.find_next("ul")
            if ul:
                for li in ul.find_all("li"):
                    first_word = li.text.split()[0]
                    description = li.text.split(" – ")[1] if " – " in li.text else li.text
                    # Search for a classification word in the description
                    classification = None
                    for keyword in targetClasses:
                        if re.search(rf"\b{keyword}\b", description, re.IGNORECASE):
                            classification = keyword
                            break
                        # If no classification is found, set it as "Unknown"
                        if not classification:
                            classification = "Unknown"
                    
                    csv_writer.writerow([first_word, heading.text.strip().split()[0], classification])

print("Data has been written to rock.csv")
