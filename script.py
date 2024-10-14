# 1.	Use BeautifulSoup and requests to scrape data from https://realpython.github.io/fake-jobs/. This page contains fake job postings.
# 2.	Extract the job titles, company names, and locations, and store them in a structured format like a CSV file use pandas module with orientation records.
# 3.	Write a function using Selenium that opens this webpage, searches for a specific job title (passed as an argument to the function), and returns the number of job postings found for that title.
# 4.	Write a scrip
# 4.	Write a script to test the function with different job titles.

import requests
from bs4 import BeautifulSoup
import pandas as pd


# get html
url = "https://realpython.github.io/fake-jobs/"
response = requests.get(url)

# parse with bs4
soup = BeautifulSoup(response.text, 'html.parser')
# print(soup)


# extract job data
jobs = []

for job in soup.find_all('div', class_="card-content"):
    job_title = job.find('h2', class_="title").text.strip()
    company_name = job.find('h3', class_="company").text.strip()
    location = job.find('p', class_="location").text.strip()
    jobs.append({'job_title': job_title, 'company': company_name, 'location': location})


# store data in a structured format
df = pd.DataFrame(jobs)
df.to_csv('job_lis.csv', index=False)

print(df)

# Selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service

import time


def search_job_title(job_title):
    # Create a Service object with the path to chromedriver
    service = Service("/workspaces/python_test/chromedriver")

    # Use the service object to start the WebDriver
    driver = webdriver.Chrome(service=service)

    # Open the fake jobs website
    driver.get("https://realpython.github.io/fake-jobs/")

    # Locate the search input box
    search_box = driver.find_element(By.ID, "search-input")

    # Enter the job title and search
    search_box.send_keys(job_title)
    search_box.send_keys(Keys.RETURN)

    # Wait for results to load
    time.sleep(2)

    # Count the number of job postings displayed
    results = driver.find_elements(By.CLASS_NAME, "card-content")
    count = len(results)

    # Close the browser
    driver.quit()

    return count

for job in jobs:

    job_title = job['job_title']
    print(job_title)
    count = search_job_title(job_title)

    print("Number of '{job_title}, Postings: {count}")