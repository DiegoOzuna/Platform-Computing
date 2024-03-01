import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import csv

# Initialize browser
driver = webdriver.Chrome()

# Navigate to your website 
driver.get("http://localhost:3000/")

metrics = []
num_clicks = 0
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
        "presence_time": presence_time,
        "scroll_position": current_scroll,
        "button_clicks": num_clicks,
        "title_page": title,
        f"paragraph_{paragraph_number}": paragraph.text
    })

# Specify the name of the csv file
csv_file = "metrics.csv"

# Open the file in write mode
with open(csv_file, 'w', newline='') as csvfile:
    # Create a csv writer object
    fieldnames = ["presence_time", "scroll_position", "button_clicks", "title_page", "paragraph_1", "paragraph_2", "paragraph_3"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # Write the header to the csv file
    writer.writeheader()

    # Write the metrics to the csv file
    for metric in metrics:
        writer.writerow(metric)

print("Metrics have been written to 'metrics.csv'")
        
driver.quit()
