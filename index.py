import requests
import pandas as pd
from bs4 import BeautifulSoup
import bs4

url = 'https://xadrezverbal.com/category/audio/podcast-do-xadrez-verbal://xadrezverbal.com/category/audio/podcast-do-xadrez-verbal/page/2'

req = requests.get(url)
if req.status_code == 200:
    print('Requisição bem sucedida')
    content = req.content

soup = BeautifulSoup(content, 'html.parser')
episodes = [episode.a for episode in soup.findAll('h2', {'class': 'post-title'})]
    #link = episode.findAll('a')
    #episode_link = link[0].get('href')
    #episode_name = link[0].text

    # print(episode_link)
    # print(episode_name)
    
episodes_name = [episode_name.text for episode_name in episodes]
episodes_link = [episode_link.get('href') for episode_link in episodes]
#print(episodes_name)
#print(episodes_link)

df_setimoselo = pd.DataFrame(columns=['nome','link', 'dicas', 'dica-link'])
for edicao in episodes_link:
    # print(edicao)
    ed_content = BeautifulSoup(requests.get(edicao).content, 'html.parser')
    #tem = ed_content.find({'h4':'Dicas do Sétimo Selo e links'}) 
    #print(tem.findAllNext('p', limit=5))
    ep_nomes = ed_content.find('h2', {'class':'post-title'}).text
    tag = ed_content.find({'h4':'Dicas do Sétimo Selo e links'}).findNext('p')

    ond = 0
    while True:
        if isinstance(tag, bs4.element.Tag):
            if tag.text == 'Canal do Xadrez Verbal no Telegram':
                print('foi')
                break
            else:
                print(tag.text)
                ond+=1
                print(ond)
                tag = tag.nextSibling
        else:
            tag = tag.nextSibling
            
    print(ond)
    # ind = 0 
    # while True:
    #     if isinstance(tag, bs4.element.Tag): 
    #         if tag.name == 'ul':
    #             break
    #         else: 
    #             #print('entrou')
    #             ind+=1
    #             tag = tag.nextSibling
    #     else:
    #         tag = tag.nextSibling        
    # print(edicao + ' [' + str(ind) + ']')
    ep_link = [edicao]*(ond-1)
    ep_nome = [ep_nomes]*(ond-1)

    setimo_selo_ep = [i.text for i in ed_content.find({'h4':'Dicas do Sétimo Selo e links'}).findAllNext({'p','ul'},limit=ond-1)]
    dica_link = [j['href'] for j in ed_content.find({'h4':'Dicas do Sétimo Selo e links'}).findAllNext({'a'},limit=ond-1)]

    # print(dica_link)
    # print(setimo_selo_ep)

    df = pd.DataFrame({'nome':ep_nome,'link':ep_link, 'dicas':setimo_selo_ep,'dica-link': dica_link})
    df_setimoselo = pd.concat([df_setimoselo,df])


#print(len(episodes_link))
print(df_setimoselo)
#print(setimo_selo)
df_setimoselo.to_csv('setimo_selo.csv')
