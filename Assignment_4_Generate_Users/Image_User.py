from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def findImages(driver, ImageTag)->int:
    count = 0
    images = driver.find_elements(By.TAG_NAME, ImageTag)
    
    for image in images:
        count += 1
    return count

def main():
    #initialize browser
    driver = webdriver.Chrome()

    #Navigate to your website
    driver.get("http://localhost:3000")
    reward_time = 10
    total_reward_time = 0
    ImageTag = "img"

    images_found = findImages(driver, ImageTag)
    print(images_found)

    if images_found > 0:
        total_reward_time += reward_time * images_found
        time.sleep(reward_time)
    
    driver.quit()
    print("Presence Time:", total_reward_time)
    print("Image count was: ", images_found)

if __name__ == "__main__":
    main()
