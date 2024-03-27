from selenium import webdriver
import time

def findKeyword(driver, keyword)->bool:
    return keyword.lower() in driver.page_source.lower()

def main():
    #initialize browser
    driver = webdriver.Chrome()

    #Navigate to your website
    driver.get("http://localhost:3000")
    reward_time = 10
    total_reward_time = 0
    keywords = ["student", "senior"]

    for keyword in keywords:
        if findKeyword(driver, keyword):
            total_reward_time += reward_time
            time.sleep(reward_time)
        
        print("Presence Time:", total_reward_time)
        print("Keyword was: ", keyword)
    
    driver.quit()

if __name__ == "__main__":
    main()
