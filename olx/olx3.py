import requests
from bs4 import BeautifulSoup
import csv

# Open CSV file for writing
csv_file = open('olx_listings.csv', 'a', newline='', encoding='utf-8')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Creation Date', 'Location', 'Title', 'Type', 'Price', 'Combined Area', 'Image Links'])

# Iterate over multiple pages
for page_num in range(1, 6):  # Change the range according to the number of pages you want to scrape
    
    url = f"https://www.olx.com.pk/lahore_g4060673/land-plots_c40?page={page_num}&filter=ft_unit_eq_marla"
    
    response = requests.get(url)
    html_content = response.content
    soup = BeautifulSoup(html_content, 'html.parser')
    
    
    listings = soup.find_all('li', class_='')

    # Iterate over listings on the page
    for listing in listings:
        try:
            link = listing.find('a')['href']
            full_link = "https://www.olx.com.pk" + link
            print(f"Full Link: {full_link}")
            
            
            response = requests.get(full_link)
            listing_html = response.content
            
            listing_soup = BeautifulSoup(listing_html, 'html.parser')
            
            overview_div = listing_soup.find('div', {'aria-label': 'Overview'})
            
            creation_date = overview_div.find('span', {'aria-label': 'Creation date'}).text
            
            location = overview_div.find('span', class_='_34a7409b').text
            
            title = listing_soup.find('h1', class_='a38b8112').text
            
            # print(f"Creation Date: {creation_date}")
            
            # print(f"Location: {location}")
            
            # print(f"Title: {title}")
            
            details_div = listing_soup.find('div', class_='cf4781f0', attrs={'aria-label': 'Details'})
            
            type_info = None
            price = None
            area_unit = None
            area = None
            
            for div in details_div.find_all('div', class_='_676a547f'):
                span_elements = div.find_all('span')
            
                if len(span_elements) >= 2:
                    label = span_elements[0].text
                    value = span_elements[1].text
            
                    if label == 'Type':
                        type_info = value
            
                    elif label == 'Price':
                        price = value
            
                    elif label == 'Area unit':
                        area_unit = value
            
                    elif label == 'Area':
                        area = value

            combined_area = f"{area} {area_unit}" if area and area_unit else None

            # print(f"Type: {type_info}")

            # print(f"Price: {price}")

            # print(f"Combined Area: {combined_area}")

            gallery_div = listing_soup.find('div', class_='cf4781f0 _765ea128')

            image_links = []

            if gallery_div:
                image_tags = gallery_div.find_all('img')
                for img_tag in image_tags:
                    src = img_tag.get('src')
                    if src:
                        image_links.append(src)

            # print(f"Image Links: {image_links}")

            csv_writer.writerow([creation_date, location, title, type_info, price, combined_area, ', '.join(image_links)])

            print("----------------------")

        except Exception as e:
            print(f"Error scraping listing: {e}")
            break

    print(f"Scraped page {page_num}")

# Close CSV file
csv_file.close()
