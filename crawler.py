from bs4 import BeautifulSoup
import requests
import datetime
import os.path
os.system('clear');

class bcolors:
    OK = '\033[92m' #GREEN
    WARNING = '\033[93m' #YELLOW
    FAIL = '\033[91m' #RED
    RESET = '\033[0m' #RESET COLOR
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'

# Bearbeiten:
zuSuchendeBeruf="Fliesenverlegungen"
staedteDatei="cities.csv"
CrawlOutputDatei="Output.csv"

print(bcolors.OK+"""

  ____                          ____
 / ___| _ __   __ _  ___ ___   / ___|_____      __
 \___ \| '_ \ / _` |/ __/ _ \ | |   / _ \ \ /\ / /
  ___) | |_) | (_| | (_|  __/ | |__| (_) \ V  V /
 |____/| .__/ \__,_|\___\___|  \____\___/ \_/\_/
       |_|

"""+bcolors.RESET)
print(bcolors.OKCYAN+"""\|/          (__)
     `\------(oo)
       ||    (__)
       ||w--||     \|/
   \|/"""+bcolors.RESET)
print()

print("Öffne "+CrawlOutputDatei+" Datei...")
citiesFile = open(staedteDatei, 'r')
nameList = []
tempVar=0
for element in citiesFile:
    element=element.strip('\n')
    nameList.append(element)
    tempVar+=1

print("[+] Daten eingelesen")
print("[i] "+str(tempVar)+" Städte wurden gefunden")
print("[i] Der zu suchende Beruf: "+zuSuchendeBeruf)
print("[i] Ausgabe wird geschrieben in: "+CrawlOutputDatei)
userInput=input(bcolors.WARNING+"[?] weiter? y/n :"+bcolors.RESET)
if userInput != "y":
    print("beende..")
    exit()
if os.path.exists(CrawlOutputDatei):
    print()
    print(bcolors.FAIL+"[!] ACHTUNG!"+bcolors.RESET)
    print("[i] Die Datei: "+CrawlOutputDatei+" Existiert bereits")
    print("[i] Alle inhalte werden überschrieben")
    userInput=input(bcolors.WARNING+"[?] weiter? y/n :"+bcolors.RESET)
    if userInput != "y":
        print("beende..")
        exit()

print()
CrawlOutput = open(CrawlOutputDatei,'w')
now = datetime.datetime.now()
startTime= now.strftime('%d.%m.%Y %H:%M Uhr')
CrawlOutput.write('Branche;Branche;Adresse;PLZ;Straße;Nummer\n')
CrawlOutput.close();
for element in nameList:
    CrawlOutput = open(CrawlOutputDatei,'a')
    searchUrls = []
    print("--------------------------------------------------------------------")
    print()
    print('#############################')
    print("# Durchgang für Stadt: "+element)
    print('#############################')

    url = f'https://www.gelbeseiten.de/Suche/'+zuSuchendeBeruf+'/'+element+'?umkreis=0'
    print(url)

    try:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        table = soup.find('div',attrs={'id':'gs_treffer'})


        for urls in table.find_all('a', href=True):
            url = str(urls["href"])
            searchUrls.append(str(urls["href"]))
    except:
        print()
        print(element+" Übersprungen")
        print()
        continue

    searchUrls = list(set(searchUrls))
    print()

    for urls in searchUrls:
        infoList=[]
        try:
            page = requests.get(urls)
            soup = BeautifulSoup(page.content, 'html.parser')
            print('[+] Verbunden -> '+urls)
        except:
            print('[-] -> '+urls)

        # Firmen Name
        try:
            infoList.append(str(soup.find('h1',attrs={'class':'mod-TeilnehmerKopf__name'}).text).strip()+";")
            print('[+] Firma -> '+str(str(soup.find('h1',attrs={'class':'mod-TeilnehmerKopf__name'}).text).strip().replace("\n", " ")))
        except:
            print('[-] Konnte Firmen Name nicht finden')
            print("[i] Überspringe Url")
            print()
            continue

        # Branche
        try:
            #if str(soup.find('ul',attrs={'class':'list-unstyled'}).text).strip()==zuSuchendeBeruf:
            infoList.append(str(soup.find('ul',attrs={'class':'list-unstyled'}).text).strip().replace("\n", " ")+";")
            print('[+] Branche -> '+str(soup.find('ul',attrs={'class':'list-unstyled'}).text).strip().replace("\n", " "))
            #else:
            #print('[-] Nicht die Gesuchte Branche')
            #print()
            #continue

        except:
            print('[-] Konnte Branche nicht finden')
            infoList.append("null")

        """
        try:
            if str(soup.find('ul',attrs={'class':'list-unstyled'}).text).strip()==zuSuchendeBeruf:
                infoList.append(str(soup.find('ul',attrs={'class':'list-unstyled'}).text).strip()+";")
                print('[+] Branche gefunden')
            else:
                print('[-] Nicht die Gesuchte Branche')
                print()
                continue

        except:
            print('[-] Konnte Branche nicht finden')
            infoList.append("null")
        """
        # Adresse
        try:
            tableTemp = soup.find('address',attrs={'class':'mod-TeilnehmerKopf__adresse'})
            infoList.append(str(tableTemp.select_one('span:nth-of-type(1)').text).strip()+";")
            print('[+] Adresse -> '+str(tableTemp.select_one('span:nth-of-type(1)').text).strip().replace("\n", " "))
        except:
            print('[-] Konnte Adresse nicht finden')
            infoList.append("null")

        # PLZ
        try:
            tableTemp = soup.find('address',attrs={'class':'mod-TeilnehmerKopf__adresse'})
            #print(str(tableTemp.select_one('span:nth-of-type(2)').text))
            infoList.append(str(tableTemp.select_one('span:nth-of-type(2)').text).strip()+";")
            print('[+] PLZ -> '+str(tableTemp.select_one('span:nth-of-type(2)').text).strip().replace("\n", " "))
        except:
            print('[-] Konnte PLZ nicht finden')
            infoList.append("null")

        # Ort
        try:
            tableTemp = soup.find('address',attrs={'class':'mod-TeilnehmerKopf__adresse'})
            #print(str(tableTemp.select_one('span:nth-of-type(2)').text))
            infoList.append(str(tableTemp.select_one('span:nth-of-type(3)').text).strip()+";")
            print('[+] Ort -> '+str(tableTemp.select_one('span:nth-of-type(3)').text).strip().replace("\n", " "))
        except:
            print('[-] Konnte Ort nicht finden')
            infoList.append("null")


        # Telefon
        try:
            tableTemp = soup.find('a',attrs={'class':'nolink-black'})
            infoList.append(str(tableTemp.find('span').text).strip())
            print('[+] Nummer -> '+str(tableTemp.find('span').text).strip().replace("\n", " "))
        except:
            print('[-] Konnte Nummer nicht finden')
            infoList.append("null")

        #print("Datas:"+str(infoList))
        CrawlOutputClear=""
        for rawInput in infoList:
            CrawlOutputClear+=rawInput

        CrawlOutput.write(CrawlOutputClear+'\n')
        print()

    CrawlOutput.close()

print()
print()
print(bcolors.OK+"""

  ___ _              __ _       _     _              _
 |_ _( )_ __ ___    / _(_)_ __ (_)___| |__   ___  __| |
  | ||/| '_ ` _ \  | |_| | '_ \| / __| '_ \ / _ \/ _` |
  | |  | | | | | | |  _| | | | | \__ \ | | |  __/ (_| |
 |___| |_| |_| |_| |_| |_|_| |_|_|___/_| |_|\___|\__,_|


"""+bcolors.RESET)
print("[i] Start time: "+bcolors.OK+startTime+bcolors.RESET)
now = datetime.datetime.now()
print("[i] End time: "+bcolors.OK+now.strftime('%d.%m.%Y %H:%M Uhr')+bcolors.RESET)
print()
print("[i] Datas saved in -> "+bcolors.WARNING+CrawlOutputDatei+bcolors.RESET)
print("[+] finished")
