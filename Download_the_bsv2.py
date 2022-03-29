#Selenium

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

PATH = "C:\Program Files (x86)\chromedriver.exe" #Cesta k webdriveru
driver = webdriver.Chrome(PATH) #jmeno

compare = ["výroční zpráva [2020]","výroční zpráva [2019]","výroční zpráva [2018]","výroční zpráva [2017]"]
ucetni = ["účetní závěrka [2020]","účetní závěrka [2019]","účetní závěrka [2018]","účetní závěrka [2017]"]
# Je mozne ze download speed bude too fucking slow a nechci to checkovat pomoci download adresare kam se normalne veci stahuji
# Takze kdytak upravit sleep timer dole na vice sekund (pokud by jste to opravdu chteli tak se obetuji)
driver.get("https://aobp.cz/clenove/?fbclid=IwAR3ynXwAPAawMk5jmxG-uGajW9aTU_kBXEmjpiIMhgDPNhwAJzyO4xUTkcA")
listveci = driver.find_elements_by_class_name("upme-name")
listfirem = []
for vec in listveci:
	listfirem.append(vec.text)

for link in listfirem: #Loop pro spolecnosti
	driver.get("https://or.justice.cz/ias/ui/rejstrik")
	driver.find_element(By.CLASS_NAME,"text").send_keys(link)
	driver.find_element(By.ID,"quick-search-button").click()

	try:
		element = WebDriverWait(driver, 2).until(
		EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "Sbírka"))
		)
		driver.find_element(By.PARTIAL_LINK_TEXT,"Sbírka").click()
	except:
		continue
	i = -1
	for zprava in compare: #Loop pro vyrocni zpravy.
		col = 0
		i += 1
		main = driver.find_element_by_class_name("list") #Lokace tablky
		tbody = main.find_element(By.TAG_NAME, "tbody") #preskoceni nadpisu
		rows = tbody.find_elements(By.TAG_NAME, "tr") #radky
		for row in rows:
			col = row.find_elements(By.TAG_NAME,"td")[1].text

			if zprava in col:
				cell = row.find_elements(By.TAG_NAME,"td")[0].text 
				driver.find_element(By.PARTIAL_LINK_TEXT,cell).click() #Nalez radku -> clickni na odkaz na presmerovani 
				break
			elif ucetni[i] in col:
				cell = row.find_elements(By.TAG_NAME,"td")[0].text 
				driver.find_element(By.PARTIAL_LINK_TEXT,cell).click() #Nalez radku -> clickni na odkaz na presmerovani 
				break

		try:
		   	element = WebDriverWait(driver, 2).until(
	        	EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "kB"))
	    	)
		   	driver.find_element(By.PARTIAL_LINK_TEXT,'kB').click()
		   	driver.execute_script("window.history.go(-1)")
		   	time.sleep(1)
		except:
		  	print("test_error") #pokud to nenalezne odkaz (neni to na dalsi strance escape z loopu)

driver.quit()