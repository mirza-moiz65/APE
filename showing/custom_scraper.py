from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.options import Options

def chrome_scrape():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    # Set up Selenium WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=chrome_options)

    # Open a webpage
    driver.get("https://stocktwits.com/markets/news/crypto")

    # Define words to check for in the second line
    words_to_check = ['minutes', 'minute', 'hours', 'hour', ]

    # Define keywords to track and initialize their counts
    keywords_to_track = [
        {'keywords': ['btc', 'bitcoin','Bitcoin','BTC'], 'count': 0,'name':"Bitcoin"},
        {'keywords': ['ethereum', 'eth','ETH','Ethereum'], 'count': 0,'name':"Ethereum"}
        # Add more keywords with their variations as needed
    ]

    # XPath to target the news feed container
    xpath = '//*[@id="panel:R2kjcim:3"]/div/div[1]/div/div'

    # Wait for the page to load completely (adjust as necessary)
    time.sleep(8)

    # Find elements matching the XPath query after scrolling
    matching_elements = driver.find_elements(By.XPATH, xpath)

    # Initialize founds counter for words_to_check
    founds = 0

    # Iterate through matching elements
    for index, element in enumerate(matching_elements):
        # Find all divs within the current element
        divs = element.find_elements(By.TAG_NAME, 'div')
        print(f"Element {index + 1} has {len(divs)} div(s)")

        # Iterate through divs
        for div_index, div in enumerate(divs):
            try:
                # Split text into lines
                text_lines = div.text.split('\n')
                
                # Check second line for words_to_check
                second_line = text_lines[1]
                if any(word in second_line for word in words_to_check):
                    founds += 1
                    
                    # Check first line for keywords to track
                    first_line = text_lines[0]
                    for keyword_obj in keywords_to_track:
                        for keyword in keyword_obj['keywords']:
                            if keyword in first_line:
                                keyword_obj['count'] += 1
                                
                                # Break out of the inner loop since we found a match
                                break
            
            except Exception as e:
                continue

   

    # Close the WebDriver
    driver.quit()

    return keywords_to_track
