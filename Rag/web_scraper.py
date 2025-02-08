import requests
from bs4 import BeautifulSoup

def scrape_website(url):
    response = requests.get(url)  # Fetch the website content
    soup = BeautifulSoup(response.text, "html.parser")  # Parse the HTML of the website
    
    # Extract all paragraphs and headings from the page
    content = [p.text for p in soup.find_all("p")]  # Get all paragraphs (<p> tags)
    headings = [h.text for h in soup.find_all(["h1", "h2", "h3"])]  # Get headings (<h1>, <h2>, <h3> tags)

    # Return the extracted headings and content
    return {"headings": headings, "content": content}

# Test the scraper on Stanford's website (or replace with another URL)
url = "https://www.stanford.edu/"
data = scrape_website(url)

# Print the extracted information (headings and paragraphs)
if "headings" in data and data["headings"]:
    print("Headings:")
    for heading in data["headings"]:
        print(f"- {heading}")
else:
    print("No headings found!")

if "content" in data and data["content"]:
    print("\nContent:")
    for paragraph in data["content"]:
        print(f"- {paragraph[:100]}...")  # Display only the first 100 characters for brevity
else:
    print("No content found!")