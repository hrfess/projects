import requests
from bs4 import BeautifulSoup

def get_company_names(url):
  """
  Extracts company names from a single page of search results.

  Args:
      url (str): The URL of the page to scrape.

  Returns:
      list: A list of company names extracted from the page.
  """
  response = requests.get(url)
  soup = BeautifulSoup(response.content, 'html.parser')

  # Find all company name elements
  company_names = [
      item.text.strip() for item in soup.find_all('span', class_='style_title__lAmLf')]

  return company_names

def scrape_all_companies(base_url, total_pages):
  """
  Scrapes company names from all pages of search results.

  Args:
      base_url (str): The base URL for pagination.
      total_pages (int): The total number of pages.
  """
  all_companies = []
  for page_number in range(1, total_pages + 1):
    url = f"{base_url}&page={page_number}"
    company_names = get_company_names(url)
    all_companies.extend(company_names)
    print(f"Scraped page {page_number} with {len(company_names)} companies")

  # Save scraped company names to a file (optional)
  with open("company_names.txt", "w", encoding="utf-8") as f:
    for name in all_companies:
      f.write(f"{name}\n")

  print("Scrape completed. All companies saved to company_names.txt")

# Modify these values as needed
base_url = "https://annuaire-entreprises.data.gouv.fr/rechercherterme=&tranche_effectif_salarie=03&sap=J"
total_pages = 528  # Update with actual number of pages

scrape_all_companies(base_url, total_pages)
