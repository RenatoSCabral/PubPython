import csv
import time

import requests
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

servico = Service(ChromeDriverManager().install())
navegador = webdriver.Chrome(service=servico)


#
# def save_to_csv(jobs) ##############################################################
#
def save_to_csv(jobs):
    #   file = open('C:\Users\Administrador\Desktop\Privado\Cursos WEB (852Gb)\Folder Python\VsCode\jobsRC.csv', 'w')
    file = open('jobsRC.csv', 'w')
    write = csv.writer(file)
    write.writerow(['title', 'company', 'location', 'how_old', 'link'])

    regsalve = 1
    for job in jobs:
        print('      registro número : ', regsalve)
        regsalve = regsalve + 1
        write.writerow(list(job.values()))

#
# def search_indeed(keyword) ##########################################################
#


def search_indeed(keyword):

    print('\n#################################')
    print('# iniciando o def search_indeed #')
    print('#################################\n')

    # cria urls (usando o range)
    urls = []
    pagina1 = "sim"
    url_base = 'https://br.indeed.com/jobs?'
    for n_page in range(3):
        if pagina1 == "sim":
            #           print("\n### PÁGINA SIM ####")
            pagina1 = "não"
            url = f"{url_base}q={keyword}"
            # https://br.indeed.com/jobs?q=python&l=&vjk=c1bff9b1b6a00771
        else:
            #           print("\n### PÁGINA NÃO ####")
            url = f"{url_base}q={keyword}&start={n_page * 10}"

        urls.append(url)
        print("   n_page :", n_page, "  url : ", url)
        # envia as urls para scrapping
    return scrapping_indeed(urls)

#
# def scrapping_indeed(urls) ################################################################
#


def scrapping_indeed(urls):

    print('\n####################################')
    print('# iniciando o def scrapping_indeed #')
    print('####################################')

    #servico = Service(ChromeDriverManager().install())
    #navegador = webdriver.Chrome(service=servico)

    all_jobs = []
    sequrl = "s"
    numexec = 1
    # para cada url recebina faça:
    print(' \n   >>>> len(urls) : ', len(urls))

    for url in urls:
        print("\n### começando uma url : ", url)

        print("    execução número : ", numexec)
        numexec = numexec + 1

        navegador.get(url)

        time.sleep(10)

#        Cards = navegador.find_elements(By.CLASS_NAME, 'resultContent')

        Cards = navegador.find_elements(By.CLASS_NAME, 'result')

        print("    número de Cards : ", len(Cards))
        print(Cards)

        seqcards = 1

        for Card in Cards:

            print(" \n    xxx - title número ", seqcards)

            try:
                CardTitle = Card.find_element(
                    By.TAG_NAME, 'span').get_attribute("title")
            except:
                CardTitle = "== Erro : sem Título"
            print("    Titulo    : ", CardTitle)

            try:
                CardCompanyName = Card.find_element(
                    By.CLASS_NAME, 'companyName').text
            except:
                CardCompanyName = "== Erro : sem Company Name"
            print("    Company   : ", CardCompanyName)

            try:
                CardCompanyLocation = Card.find_element(
                    By.CLASS_NAME, 'companyLocation').text
            except:
                CardCompanyLocation = "== Erro : sem Company Location"
            print("    Location  : ", CardCompanyLocation)

            try:
                CardCompanyHowOld = Card.find_element(
                    By.CLASS_NAME, 'date').text.lstrip()
            except:
                CardCompanyHowOld = "== Erro : sem How Old"
            print("    How Old   : ", CardCompanyHowOld)
            print("    Len HowOld: ", len(CardCompanyHowOld))

            try:
                CardCompanyLink = Card.find_element(
                    By.TAG_NAME, 'a').get_attribute("href")
            except:
                CardCompanyLink = "== Erro : sem Link"
            print("    Link      : ", CardCompanyLink)

            seqcards = seqcards + 1

            job = {
                'title': CardTitle,
                'company': CardCompanyName,
                'location': CardCompanyLocation,
                'how_old': CardCompanyHowOld,
                'link': CardCompanyLink
            }

            all_jobs.append(job)

    return all_jobs


######## main #######################


search = 'python'
#url_base = 'https://br.indeed.com/empregos?'

print("### antes no search_indeed")
result_indeed = search_indeed(search)
print("### depois do search_indeed")

print(result_indeed)

print("### antes no save_to_csv(")
save_to_csv(result_indeed)
print("### depois do save_to_csv(")
