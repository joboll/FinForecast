

from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

TICKER = input('Entrer le ticker du titre (NYSE seulement):')
URL = 'https://www.stocktargetadvisor.com/stock/USA/NYE/{}#analyst-rating-tab'.format(TICKER)


def soup4test(URL):

    with requests.Session() as sesh:
        response = sesh.get(URL)
        html = response.text
    soup = BeautifulSoup(html, features="lxml")
    return soup

def get_headers(soup):
    """
    Extract header cell text from table
    Parameters: Soup (bs4)
    Returns: List of all table headers
    """
    headers = []
    for t in soup.find_all('th', class_="sorting"):
        headers.append(t.text)

    return headers

 def get_rows(soup, rows):
    """
    Extract row cell text from table
    Parameters: Soup (bs4)
    Returns: List of cells within a list of rows
    """    
    row = []
    for i in soup.find('div', class_="datatable-scroll viewed").find('tbody').find_all('tr'):
        rows.append(row) if row  else rows # Append une ligne si var row a un contenu
        row = []
        for j in i.find_all('td'): 
            row.append(j.text)
    
    return rows

"""
Extraction du 'code' de Ajax Code Editor (partie seulement possible en Selenium)
"""

driver = webdriver.Chrome(ChromeDriverManager().install()) 
driver.get(URL)

html = driver.page_source
soup = BeautifulSoup(html, features="lxml") 

#code = driver.find_elements_by_id("analyst_rate").text
#code = driver.find_element(By.ID, "analyst_rate").text
#print(str(code))
#table = soup.find('table', id_="analyst_rate")
#print(str(table))

headers = get_headers(soup)
previous_rows = rows if rows else []
rows = get_rows(soup, previous_rows)






driver.find_element(By.ID, "analyst_rate_next").click()


"""driver.find_element(By.LINK_TEXT, "Sign in").click()
driver.find_element(By.ID, "user_email").click()
driver.find_element(By.ID, "user_email").send_keys("job@zenetik.org")
driver.find_element(By.CSS_SELECTOR, ".dc-account-modal__next-btn").click()
driver.implicitly_wait(5)
driver.find_element(By.ID, "user_password").click()
driver.find_element(By.ID, "user_password").send_keys("JO21bo12")
driver.find_element(By.ID, "user_password").send_keys(Keys.ENTER)"""

# Time out pour que les credentials se load. Peut aussi appliquer la stratégie expliqué en 5.1 de https://selenium-python.readthedocs.io/waits.html
"""time.sleep(10)

driver.get(INTERNAL_URL)
driver.implicitly_wait(10)

# Scrape le code
code = driver.find_element(By.CSS_SELECTOR, ".ace_content").text
print(str(code))

time.sleep(7)
# Scrape le completed message
driver.find_element(By.XPATH, '//*[@id="gl-editorTabs-files/script.py"]/div/div[2]/div[2]/div[3]/button').click()
driver.implicitly_wait(10)
completed_message = driver.find_element(By.CSS_SELECTOR, ".dc-completed__message").text
print(str(completed_message))"""

# teardown_method(self, method):
driver.quit()




#ToDo next: Click next with selenium