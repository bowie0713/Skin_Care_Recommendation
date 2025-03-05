import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By  # Import By 
from selenium.webdriver.common.keys import Keys  # Import Keys for scrolling
import requests
import time
import re

categorized_df = pd.read_excel("/Users/bowiechuang/Documents/GitHub/Skin_Care_Recommendation/sephora_product_list.xlsx")
#Testing
test_links = categorized_df['link'][401:405]

def scrollDown(driver, n_scroll):
    elem = driver.find_element(By.TAG_NAME, "html")
    while n_scroll >= 0:
        elem.send_keys(Keys.PAGE_DOWN)
        n_scroll -= 1
    return driver

# Setup Chrome options
options = Options()
options.add_argument("--disable-gpu")

options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.90 Safari/537.36")
# options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.90 Safari/537.36") #Christina's agent 
options.add_argument("--disable-blink-features=AutomationControlled")

# Initialize the WebDriver
driver = webdriver.Chrome(options=options)  # Ensure ChromeDriver is installed and in PATH

# Loop through each link in categorized_df['link']
products_list = []
for link in test_links:
    try:
        driver.get(link)
        time.sleep(10)  # Give page time to load
        
        #Check link if the page redirects to "productnotcarried"
        if "/search?" in driver.current_url:
          print(f" Skipping unavailable product: {link}")
          continue
        
        while True:
            browser = scrollDown(driver, 20) #scroll down the page
            time.sleep(10) #give it time to load
            break
        
        #Parse Page Source
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        # Extract product name
        prod_name_element = soup.find('span', {'data-at': 'product_name'})  # Use find instead of find_all

        if prod_name_element:
          prod_name = prod_name_element.text.strip()  # Extract text
          prod_name = " ".join(word for word in prod_name.split() if word.lower() != "hair")  # Remove "Hair" from product           name
        else:
          prod_name = "N/A"  # Default value if not found

         # Extract brand name
        prod_element = soup.find('a', class_=['css-1kj9pbo e15t7owz0', 'css-wkag1e e15t7owz0'])
        brand_name = prod_element.text.strip() if prod_element else "N/A"
        
        # Removed 'size' from string. 
        #Extract brand size
        size = soup.find(['span', 'div'], class_ = ['css-15ro776', 'css-1wc0aja e15t7owz0'])
        if size:
          prod_size = size.text.strip()   # Extract text 
          prod_size = prod_size.replace('Size:', '').replace('Size', '').strip()  # Remove "Size" and extra details
        else:
          prod_size = "N/A"  # Default if not found
          
        #Product type
        category = categorized_df.loc[categorized_df['link'] == link, 'category'].values
        category = category[0] if len(category) > 0 else "N/A"  
        
        #Extract product price
        price = soup.find('b', class_='css-0')
        prod_price = price.text.strip() if price else "N/A"
        
        #Extract product rating class="css-egw4ri e15t7owz0" 
        #rating = soup.find_all("span", attrs={"class": "css-egw4ri e15t7owz0"})
        rating = soup.find_all("span", class_=re.compile(".*css-egw4ri.*e15t7owz0.*"))

        # Ensure there's at least one match before accessing index 0
        if rating:
          prod_rating = rating[0].text.strip()  # Get first match
        else:
          prod_rating = "N/A"  # Default value if no match found
        
        #Extract brand reviews
        review = soup.find_all('span', class_ = 'css-1dae9ku e15t7owz0')
        if review:
          prod_reviews = review[0].text.strip()  # Get full text
          match = re.search(r'\d+', prod_reviews)  # Extract only the first number
          prod_reviews = match.group(0) if match else "N/A"  # Get the matched number

        #Extract Description
        # Locate all divs that may contain product descriptions
        description_classes = soup.find_all('div', class_=['css-1v2oqzv e15t7owz0', 'css-1j9v5fd e15t7owz0', 'css-1uzy5bx e15t7owz0'])

        description_tags = ['p', 'b', 'strong']

        # Initialize default value
        prod_desc = "N/A"

        element_desc = []
        for class_name in description_classes:
          element_desc.extend(soup.find_all('div', class_=class_name))

        for div in element_desc:
          for tag in description_tags:
            element = div.find(tag)
            # Check if the element contains "What it is:"
            if element and "What it is:" in element.text:
            # Extract text while handling possible formatting issues
              extracted_text = element.get_text(separator=" ", strip=True).replace("What it is:", "").strip()

            # Case 2: The description follows the tag as a sibling text
              if not extracted_text and element.next_sibling:
                extracted_text = element.next_sibling.strip()

            # Case 3: Handle cases where the text is split across multiple <br> tags
              if not extracted_text:
                extracted_text = []
                next_element = element.find_next_sibling(text=True)
                while next_element:
                  extracted_text.append(next_element.strip())
                  next_element = next_element.find_next_sibling(text=True)
                extracted_text = " ".join(extracted_text).strip()

          # If valid text is found, set it and stop searching
              if extracted_text:
                prod_desc = extracted_text
                break # Stop searching once we find a valid description

          if prod_desc != "N/A":
            break  # Stop checking other divs once we get the correct description

        # Print the extracted product description
        print(f"Product Description: {prod_desc}")


        #Extract Skin Types
        element_types = soup.find_all('div', class_ = ['css-1v2oqzv e15t7owz0', 'css-1j9v5fd e15t7owz0', 'css-1uzy5bx e15t7owz0'])

        skin_type = "N/A"

        for div in element_types:
          strong_elements = div.find_all(['strong', 'b'])  # Find all <strong> and <b> elements in this div

          for tag in strong_elements:
            if "Skin Type:" in tag.text:
              next_text = tag.next_sibling
              if next_text and next_text.strip():
                skin_type = next_text.strip()
              else:
                next_container = tag.find_next_sibling()  # Backup check for next sibling
                if next_container:
                  skin_type = next_container.get_text(strip=True)

        #Extract Concerns
        element_concerns = soup.find_all('div', class_ = ['css-1v2oqzv e15t7owz0', 'css-1j9v5fd e15t7owz0', 'css-1uzy5bx e15t7owz0'])

        # Initialize default values
        skin_concerns = "N/A"

        for div in element_concerns:
          strong_elements = div.find_all(['strong','b'])  # Find all <strong> elements in this div

          for tag in strong_elements:
            if "Skincare Concerns:" in tag.text:
              next_text = tag.next_sibling  # Get text after <b> or <strong>
              if next_text and next_text.strip():
                skin_concerns = next_text.strip().replace("-", "")
              else:
                next_container = tag.find_next_sibling()  # Backup check for next sibling
                if next_container:
                  skin_concerns = next_container.get_text(strip=True).replace("-", "")


          # Handle cases where concerns are listed inside separate `<p>` tags
          p_tags = div.find_all('p')
          p_concerns = [p.text.strip().replace("-", "").strip() for p in p_tags if p.text.strip()]
          # If `<p>` contains concerns, update values
          if p_concerns:
            if "Skincare Concerns:" in strong_elements:
              skin_concerns = ", ".join(p_concerns)  # Join multiple concerns
              
        #Extract Ingredients
        ingredient_element = soup.find('div', class_ = 'css-1mb29v0 e15t7owz0')
        if ingredient_element:
          prod_ingredients = ingredient_element.text.strip()
        else:
          prod_ingredients = 'N/A'
  
        # Append data
        products_list.append({"Brand Name": brand_name,
                              "Product Name": prod_name,
                              "Product Category": category,
                              "Product Price": prod_price,
                              "Product Rating": prod_rating,
                              "Product Size": prod_size,
                              "Product Reviews": prod_reviews,
                              "Product Description": prod_desc,
                              "Product Ingredients": prod_ingredients,
                              "Skin Type": skin_type,
                              "Skin Concerns": skin_concerns,
                              "URL": link})
        #check if it processes link 
        print(f" processed: {link}")

    except Exception as e:
        print(f" Error processing {link}: {e}")

# Close WebDriver *after* processing all links
driver.quit()

product_df = pd.DataFrame(products_list)
print(product_df)



