from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import pandas as pd
import time

# Make sure to replace 'your/path/to/chromedriver' with the actual path to the ChromeDriver
service = Service('your/path/to/chromedriver')
driver = webdriver.Chrome(service=service)

# Navigate to the website
driver.get('https://hprera.nic.in/PublicDashboard')


time.sleep(5)  # Adjust the sleep time as necessary

# Get the first 6 project links under "Registered Projects"
project_links = driver.find_elements(By.XPATH, '//table[@id="tblProjects"]//tbody/tr/td[1]/a')[:6]

project_details = []

for link in project_links:
    project_data = {}
    rera_no = link.text
    link.click()
    time.sleep(3)  # Wait for the details page to load
    
    # Get the page source and parse it with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    # Extract details
    project_data['RERA No'] = rera_no
    project_data['GSTIN No'] = soup.find('span', id='ContentPlaceHolder1_lblGSTIN').text.strip()
    project_data['PAN No'] = soup.find('span', id='ContentPlaceHolder1_lblPAN').text.strip()
    project_data['Name'] = soup.find('span', id='ContentPlaceHolder1_lblPromoterName').text.strip()
    project_data['Permanent Address'] = soup.find('span', id='ContentPlaceHolder1_lblAddress').text.strip()
    
    project_details.append(project_data)
    
    # Go back to the previous page
    driver.back()
    time.sleep(3)  # Wait for the page to load again

driver.quit()


df = pd.DataFrame(project_details)
print(df)
df.to_csv('registered_projects.csv', index=False)
