from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def countElem(driver, tag_name)->int:
    #get count of this element (in this case, images)
    return len(driver.find_elements(By.TAG_NAME, tag_name))

def main():
    #initialize browser
    driver = webdriver.Chrome()

    #Navigate to your website
    driver.get("http://localhost:3000")
    reward_time = 10
    total_reward_time = 0
    tags = ["img"] #we will keep it as a list in case we want to check for more tags

    for tag in tags:
        num_elem = countElem(driver, tag)
        total_reward_time += reward_time * num_elem
        time.sleep(reward_time)
    
    driver.quit()
    print("Presence Time:", total_reward_time)
    print("Image count was: ", num_elem)

if __name__ == "__main__":
    main()
