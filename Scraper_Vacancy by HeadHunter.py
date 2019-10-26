# -*- coding: UTF-8 -*-
import requests
from bs4 import BeautifulSoup as bs
import smtplib

def mail_send(body):
    HOST = "192.168.0.5"
    SUBJECT = "Vacancy by HeadHunter"
    TO = "119_6@hosp13"
    FROM = "HeadHunter"
    
    text = body
     
    BODY = "\r\n".join((
        "From: %s" % FROM,
        "To: %s" % TO,
        "Subject: %s" % SUBJECT ,
        "",
        text
    ))
    
    server = smtplib.SMTP(HOST)
    #server.sendmail(FROM, [TO], BODY.encode('cp1251'))
    #server.sendmail(FROM, [TO], BODY.encode('ascii'))
    server.sendmail(FROM, [TO], BODY.encode('utf-8'))
    server.quit()    

def hh_parse(base_url, headers):
    body=''
    #out = 'output.txt'
    session = requests.session()
    request = session.get(base_url, headers=headers)
    if request.status_code == 200:
        soup = bs(request.content, 'html.parser')
        divs = soup.find_all('div', attrs={'data-qa': 'vacancy-serp__vacancy'})
        #output_file = open(out, 'a')
        for div in divs:
            title = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'}).text
            compensation = div.find('div', attrs={'data-qa': 'vacancy-serp__vacancy-compensation'})
            if compensation == None:
                compensation = 'Не указанно'
            else:
                compensation = div.find('div', attrs={'data-qa': 'vacancy-serp__vacancy-compensation'}).text
            href = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'})['href']
            company = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-employer'}).text.strip()
            text1 = div.find('div', attrs={'data-qa': 'vacancy-serp__vacancy_snippet_responsibility'}).text
            text2 = div.find('div', attrs={'data-qa': 'vacancy-serp__vacancy_snippet_requirement'}).text
            content = 'Условия:\n' + text1 + '\nТребования к кандидату:\n' + text2
            all = title + '\t' + compensation  + '\n' + 'Company: ' + company + '\n' + content + '\n' + href + ('\n\n'+'-------------------------------'+'\n')
            #output_file.write(all)
            body+= all
         
        #output_file.close()
    else:
        print('ERROR')
    mail_send(body)
 
def main():
    headers = {'accept': '*/*', 'user-agent': 'Mozilla/5.0(X11;Linux x86_64...)Geco/20100101 Firefox/60.0'}
    #base_url = 'https://nn.hh.ru/search/vacancy?order_by=publication_time&clusters=true&area=1679&text=devops&enable_snippets=true&search_period=3'
    base_url = 'https://nn.hh.ru/search/vacancy?search_period=1&clusters=true&area=1679&text=devops&order_by=publication_time&enable_snippets=true'
    hh_parse(base_url, headers)
    
    base_url ='https://nn.hh.ru/search/vacancy?area=1679&clusters=true&enable_snippets=true&order_by=publication_time&search_period=1&text=junior&specialization=1&from=cluster_professionalArea&showClusters=true'
    hh_parse(base_url, headers)
    
    base_url = 'https://nn.hh.ru/search/vacancy?area=1679&clusters=true&enable_snippets=true&order_by=publication_time&search_period=1&text=Python&specialization=1.82&from=cluster_specialization&showClusters=true'
    hh_parse(base_url, headers)
    
    base_url = 'https://nn.hh.ru/search/vacancy?area=66&clusters=true&enable_snippets=true&search_period=1&text=%D0%A1%D1%82%D0%B0%D0%B6%D0%B5%D1%80&showClusters=true'
    hh_parse(base_url, headers)

if __name__ == '__main__':
    main()
 
