from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time

#################################################
# Rewards via keyword or image based on action
# action: KEYOWRD, IMAGE, LINK
# driver: web driver
# req_list: list of either keyword or element tag
##################################################

def userAction(action, driver, reward_time, req_list)->float:
    total_reward_time = 0
    if action.upper() == "KEYWORD":
        for keyword in req_list:
            if findKeyword(driver, keyword):
                print("found", keyword)
                time.sleep(reward_time)
                total_reward_time += reward_time
            else:
                print(keyword, "not found")
    elif action.upper() == "IMAGE":
        item = countElem(driver, req_list)
        num_images = item[0]
        reward_time_X = reward_time*num_images
        total_reward_time = reward_time_X
        print("# of Images: ", num_images)
        time.sleep(reward_time_X)
    elif action.upper() == "LINK":
        item = countElem(driver, req_list)
        num_links = item[0]
        
        clickLinks(driver, item[1])

        reward_time_X = reward_time*num_links
        total_reward_time = reward_time_X
        print("# of Links: ", num_links)
        time.sleep(reward_time_X)
    
    return total_reward_time


def findKeyword(driver, keyword)->bool:
    return keyword.lower() in driver.page_source.lower()

def countElem(driver, tag_name)->int:
    #get count of this element (in this case, images)
    length = 0
    elements = driver.find_elements(By.TAG_NAME, tag_name)
    
    length += len(elements)
    return length, elements

def clickLinks(driver, links):
    #find link or links and click on them....
    for link in links:
        ActionChains(driver) \
            .key_down(Keys.SHIFT) \
            .click(link) \
            .key_up(Keys.SHIFT) \
            .perform()

def main():
    #initialize browser
    driver = webdriver.Chrome()

    #Navigate to your website
    driver.get("http://localhost:3000")
    reward_time = 10
    total_reward_time = userAction("KEYWORD", driver, reward_time, ["senior", "student"])
    total_reward_time += userAction("IMAGE", driver, reward_time, "img")
    total_reward_time += userAction("LINK", driver, reward_time, "a")
    

    
    driver.quit()
    print("Presence Time:", total_reward_time)

if __name__ == "__main__":
    main()
