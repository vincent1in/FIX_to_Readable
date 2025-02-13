import requests
from bs4 import BeautifulSoup
import pandas as pd
import json

def scrape_fix_dictionary(version):
    """
    Scrapes the OnixS FIX dictionary page for a given FIX version
    (e.g. "4.0", "4.1", "4.2", "4.4") and returns a dictionary mapping
    tag numbers (as integers) to their human–readable field names.
    """
    url = f"https://www.onixs.biz/fix-dictionary/{version}/fields_by_tag.html"
    response = requests.get(url)
    response.raise_for_status()  # Ensures valid response
    soup = BeautifulSoup(response.text, 'html.parser')
    mapping = {}
    
    table = soup.find('table')
    if table is None:
        raise ValueError(f"No table found on the page for FIX {version}.")
    
    rows = table.find_all('tr')
    for row in rows[1:]:
        cells = row.find_all(['td', 'th'])
        if len(cells) < 2:
            continue
        tag_text = cells[0].get_text(strip=True)
        field_name = cells[1].get_text(strip=True)
        try:
            tag_num = int(tag_text)
            mapping[tag_num] = field_name
        except ValueError:
            continue
    return mapping

versions = ["4.0", "4.1", "4.2", "4.3", "4.4"]
fix_mappings = {}
for v in versions:
    try:
        fix_mappings[v] = scrape_fix_dictionary(v)
        print(f"Scraped FIX {v} dictionary with {len(fix_mappings[v])} entries.")
    except Exception as e:
        print(f"Error scraping FIX {v}: {e}")

# saves the mappings to a json so that it can be converted back to a dictionary later
# (each version is a separate json file)
for version, mappings in fix_mappings.items():
    with open(f"version_jsons/fix_{version}.json", "w") as f:
        # saves it to the versions_jsons folder
        json.dump(mappings, f)