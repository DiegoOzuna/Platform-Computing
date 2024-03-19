import time
import json

from selenium import webdriver
from selenium.webdriver.common.by import By

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# Initialize browser
driver = webdriver.Chrome()

# Navigate to your website 
driver.get("http://localhost:3000/")

metrics = []
num_clicks = 0

# Initialize a list of user_ids. Keep it simple for now. 1 and 2 
user_ids = [1, 2]


for user_id in user_ids:
    # Track presence time 
    start_time = time.time()
    presence_time = start_time
    while True:
        current_time = time.time()
        presence_time = current_time - start_time
        print(f"Presence time: {presence_time:.2f} seconds")
        
        if presence_time >= 30:  #only measure for 30 seconds
            break

        # Track scrolling
        scroll_height = driver.execute_script("return document.body.scrollHeight")  
        current_scroll = driver.execute_script("return window.pageYOffset")
        print(f"Scrolled {current_scroll}/{scroll_height} pixels")
        
        time.sleep(2) 

        # Track clicks   
        button = driver.find_element(by=By.CSS_SELECTOR, value="button")

        # for button in buttons:
        button.click()
        num_clicks += 1
        print(f"Button was clicked: {num_clicks} times")

        # Get title page
        title = driver.title
        print(f"Title page: {title}")

        # Get contents of three paragraphs based on the while loop
        paragraph_number = num_clicks % 3 + 1
        paragraph = driver.find_element(by=By.CSS_SELECTOR, value=f"p:nth-child({paragraph_number})")
        print(f"Contents of paragraph {paragraph_number}: {paragraph.text}")

        # Append metrics to the array
        metrics.append({
            "user_id": user_id,
            "presence_time": presence_time,
            "scroll_position": current_scroll,
            "button_clicks": num_clicks,
            "title_page": title,
            "paragraph": f"paragraph {paragraph_number} :"+paragraph.text
        })


#grab key from hidden json file...
with open('key.json', 'r') as f:
    password = json.load(f)

#URI Password is hidden 
uri = f"mongodb+srv://007157781:{password}@cluster0.hy4vdxy.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

db = client['metrics']

for metric in metrics:
        for key, value in metric.items():
            if key != "user_id":
                collection = db[key]  # Get the collection for this key
                # Insert the value as a new document with the user_id
                collection.insert_one({"user_id": metric["user_id"], "value": value})

driver.quit()
