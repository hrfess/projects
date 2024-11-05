import requests
from bs4 import BeautifulSoup

# Base URL with pagination
base_url = "https://annuaire-entreprises.data.gouv.fr/rechercherterme=&tranche_effectif_salarie=03&sap=J&page="

# Number of pages to scrape
total_pages = 528

# List to store company names
company_names = []

# Loop through each page
for page in range(1, total_pages + 1):
    # Fetch page content
    url = f"{base_url}{page}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all elements with the desired class
    results = soup.find_all('div', class_='style_result-item__fKcQt')
    
    # Extract company names
    for result in results:
        name_tag = result.find('span')
        if name_tag:
            company_name = name_tag.text.strip()
            company_names.append(company_name)

    print(f"Page {page} scraped successfully.")

# Print all company names
print("Scraped Company Names:")
for name in company_names:
    print(name)
