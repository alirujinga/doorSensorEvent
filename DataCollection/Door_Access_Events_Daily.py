from selenium import webdriver
from getpass import getpass
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import os
import csv
import time
from datetime import date

"""
Classes
login button = 'btn-atrium'
Date & time = 'time'
Event Block = 'details'
Next Page = 'page-link' (find one that includes '»') typically the last item

Name
username_name = 'username'
password_name = 'password'

"""

## Links
events_link = 'http://door.arxtron.local/#/events'
login_link = 'http://door.arxtron.local/#/'
login_button = 'btn-atrium'
next_page = 'page-link'
event_block = 'details'
date_block = 'time'
## Constants
filename = 'C:\\Users\\administrator.ARXTRON\\Documents\\Door Controller\\events.csv'
## Names
username_name = 'username'
password_name = 'password'
## Website IDs

def weblogin(username: str, password: str) -> webdriver.Firefox:

  driver = webdriver.Firefox()
  
  ## Disable HTTPS only on Firefox
  driver.get("about:preferences#privacy")
  driver.find_element(By.ID, "httpsOnlyRadioDisabled").click()

  ## Login
  driver.get(login_link)
  time.sleep(2)
  driver.find_element(By.NAME, username_name).send_keys(username)
  driver.find_element(By.NAME, password_name).send_keys(password)
  driver.find_element(By.CLASS_NAME, login_button).click()

  return driver

def get_lists(driver: webdriver.Firefox):
  time.sleep(1)
  driver.get(events_link)
  time.sleep(5)
  current_day_check = True
  
  with open(filename, 'a', newline='') as events_file:
    writer = csv.writer(events_file)
    
    while (current_day_check & driver.find_elements(By.CLASS_NAME, next_page)[-1].text.__contains__("Next")):
      time.sleep(10)
      dates = driver.find_elements(By.CLASS_NAME, date_block)
      events = driver.find_elements(By.CLASS_NAME, event_block)
      
      for i in range (len(dates)):
        date_line = dates[i].text.split(' ')
        event_line = events[i].text.split(' ')
        
        if (len(date_line) == 1): ## if date line is empty, skip line
          continue
        
        date_day = date_line[0]
        today = date.today().day
        if (date_day[-2:] == str(today)):
          continue
        
        if (date_day[-2:] < str(today - 1)): ## Makes sure the code stops after the previous day's data end
          current_day_check = False
          break
        
        date_time = date_line[1]
        first_name = event_line[0]
        last_name = event_line[1]
        event_details = events[i].text[len(first_name + last_name) + 2:]
        data = [date_day, date_time, first_name, last_name, event_details]
        writer.writerow(data)
      driver.find_elements(By.CLASS_NAME, next_page)[-1].click()
  

def main():

  user_login = input("\nEnter username:  ")
  user_password = getpass("\nEnter Password:  ")
  
  ## use these instead for quiet running
  ## user_login = ''
  ## user_password = ''

  driver = weblogin(user_login, user_password)
  
  get_lists(driver)
  
  driver.close()

if __name__ == "__main__":
  main()