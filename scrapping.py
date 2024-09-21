import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of the Nike webpage with products
url = 'https://www.nike.com/w/mens-shoes-nik1zy7ok'

# Send a GET request to the URL
response = requests.get(url)

# Initialize a list to store the product data
product_data = []

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all product cards on the page
    product_cards = soup.find_all('div', class_='product-card__body')

    # Loop through each product card and extract the desired information
    for product in product_cards:
        product_name = product.find('div', class_='product-card__title').get_text(strip=True) if product.find('div', class_='product-card__title') else 'N/A'
        product_id = product['data-product-id'] if 'data-product-id' in product.attrs else 'N/A'
        listing_price = product.find('div', class_='product-price').get_text(strip=True) if product.find('div', class_='product-price') else 'N/A'
        sale_price = product.find('div', class_='product-price__discounted')
        sale_price = sale_price.get_text(strip=True) if sale_price else 'N/A'
        discount = product.find('div', class_='product-price__discount')
        discount = discount.get_text(strip=True) if discount else 'N/A'
        brand = 'Nike'
        description = product.find('div', class_='product-card__subtitle').get_text(strip=True) if product.find('div', class_='product-card__subtitle') else 'N/A'
        rating = product.find('div', class_='product-card__rating')
        rating = rating.get_text(strip=True) if rating else 'N/A'
        reviews = product.find('div', class_='product-card__reviews')
        reviews = reviews.get_text(strip=True) if reviews else 'N/A'
        images = product.find_all('img', class_='product-card__hero-image')
        images = [img['src'] for img in images if 'src' in img.attrs]

        # Append the data to the list
        product_data.append({
            'Product Name': product_name,
            'Product ID': product_id,
            'Listing Price': listing_price,
            'Sale Price': sale_price,
            'Discount': discount,
            'Brand': brand,
            'Description': description,
            'Rating': rating,
            'Reviews': reviews,
            'Images': images
        })
else:
    print(f'Failed to retrieve content from {url}')

# Convert the list of product data to a pandas DataFrame
df = pd.DataFrame(product_data)

# Save the DataFrame to an Excel file
df.to_excel('nike_products.xlsx', index=False)
