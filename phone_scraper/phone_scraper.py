import requests, sys, webbrowser, time, openpyxl, urllib, re
from bs4 import BeautifulSoup as BeautifulSoup4
from BeautifulSoup import BeautifulSoup
from openpyxl import Workbook

def solve_capcha(website): #Allows the user to manually bypass the capcha code
    time.sleep(3)
    webbrowser.open(website)
    raw_input("Press Enter when the Capcha has been bypassed...")
    return urllib.urlopen(website)

ite = 2

res = urllib.urlopen('https://www.ahd.com/state_statistics.html')
noStarchSoup = BeautifulSoup(res)
noStarchSoup.prettify()

if noStarchSoup.find(id = 'popupbody') != None: #Checks if the webpage is a Capcha Page
    res = solve_capcha('https://www.ahd.com/state_statistics.html')
    noStarchSoup = BeautifulSoup(res)

table = noStarchSoup.findAll('a')

workbook = Workbook()
worksheet = workbook.active
worksheet['A1'] = 'Phone Number'
worksheet['B1'] = 'Website Address'

print('Entering first for loop')
for i in range(8,64):
    state = requests.get('https://www.ahd.com/' + table[i].get('href'))
    soup = BeautifulSoup(urllib.urlopen('https://www.ahd.com/' + table[i].get('href')).read())
    if soup.find(id = 'popupbody') != None: #Checks if the webpage is a Capcha Page
        solve_capcha('https://www.ahd.com/' + table[i].get('href'))
        i -= 1
        continue #Resets the for loop in case the user made a mistake in the capcha page

    hospital_table = soup.findAll('a')
    if len(hospital_table) == 1: #Program does not handle single length tables
        continue
    iter = 1
    for element in soup.findAll('td'):
        print(str(iter) + ' ' + str(element))
        iter += 1

    raw_input('...')
    td = 4 #Pages have 4 td tags before the table

    print('Entering second for loop')
    for j in range(8, len(hospital_table)):
        if td == 82:
            print(soup.findAll('td'))
        try:
            num_of_beds = str(soup.findAll('td')[td]).replace('<td align="right">', '').replace('</td>','').replace(',','')
        except:
            break
        print(num_of_beds)
        if int(num_of_beds) <= 150:
            hospital = requests.get('https://www.ahd.com' + hospital_table[j].get('href'))
            soup = BeautifulSoup4(hospital.text, 'html5lib')

            if soup.find(id = 'popupbody') != None: #Checks if the webpage is a Capcha Page
                soup = BeautifulSoup4(solve_capcha('https://www.ahd.com' + hospital_table[j].get('href')))
    
            all_tables = soup.find_all('td') #Gets the text of all td tags

            worksheet['A' + str(ite)] = str(all_tables[19]).replace('<td align="left">', '').replace('</td>','').replace(',','') 
            website = re.search('(http|ftp|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?', str(all_tables[21])) #Gets a website out of the table
            worksheet['B' + str(ite)] = website.group(0)
            ite += 1

            workbook.save('Small Hospital Contact Info.xlsx')

            soup = BeautifulSoup(urllib.urlopen('https://www.ahd.com/' + table[i].get('href')).read())
            if soup.find(id = 'popupbody') != None: #Checks if the webpage is a Capcha Page
                res = solve_capcha('https://www.ahd.com/' + table[i].get('href'))
                soup = BeautifulSoup(res)
        td += 6

workbook.save('Small Hospital Contact Info.xlsx')
            
