import requests
import pandas as pd
from bs4 import BeautifulSoup
import bs4

df_setimoselo = pd.DataFrame(columns=['nome','link', 'dicas', 'dica-link'])
url = 'https://xadrezverbal.com/category/audio/podcast-do-xadrez-verbal/page/'

text_stop = ['Canal do Xadrez Verbal no Telegram', 
             'Minutagem dos blocos, cortesia dos financiadores do Xadrez Verbal', 
             'Playlist das músicas de encerramento do Xadrez Verbal no Spotify',
             'Ouça o podcast aqui ou baixe o programa.']
tag_stop = ['h2', 'h3', 'h4']
ep_stop = ['https://xadrezverbal.com/2017/04/23/podcast-prorrogacao-01-nova-lei-de-imigracao-e-leitura-comentada/',
           'https://xadrezverbal.com/2016/10/28/xadrez-verbal-podcast-70-oriente-medio-filipinas-e-venezuela/',
           'https://xadrezverbal.com/2018/07/20/xadrez-verbal-podcast-150-israel-america-latina-e-cupula-trump-putin/']
def scrp(u):
    d = pd.DataFrame(columns=['nome','link', 'dicas', 'dica-link'])
    req = requests.get(u)
    if req.status_code == 200:
        print('Requisição bem sucedida')
        content = req.content

    soup = BeautifulSoup(content, 'html.parser')
    episodes = [episode.a for episode in soup.findAll('h2', {'class': 'post-title'})]
        
    # episodes_name = [episode_name.text for episode_name in episodes]
    # print(episodes_name)
    episodes_link = [episode_link.get('href') for episode_link in episodes]
    for edicao in episodes_link:
        #tem = ed_content.find({'h4':'Dicas do Sétimo Selo e links'}) 
        #print(tem.findAllNext('p', limit=5))
        print(edicao)

        if edicao in ep_stop: 
            break
        else:
            ond = 1
            ed_content = BeautifulSoup(requests.get(edicao).content, 'html.parser')
            try:
                tag = ed_content.find({'h4':'Dicas do Sétimo Selo e links'}).findNext('p')
                print('entrou h4')
            except:
                try: 
                    tag = ed_content.find({'p':'Dicas do Sétimo Selo e links'}).findNext('p')
                    print('entrou p')
                except:
                    try:
                        tag = ed_content.find({'strong':'Dicas do Sétimo Selo e links'}).findNext('p')
                        print('entrou strong')
                    except:
                        try:
                            tag = ed_content.find({'strong':'Dicas do Sétimo Selo'}).findNext('p')
                            print('entrou dicas')
                        except:
                            tag = ed_content.find({'strong':'Textos e links'}).findNext('p')
                            print('entrou p textos')
            print(tag.text.encode('utf-8'))
            if tag.text.upper() == 'EM BREVE':
                break
            else:
                while True:
                    if isinstance(tag, bs4.element.Tag):
                        if tag.name in tag_stop or tag.text in text_stop:
                            # print('foi')
                            break
                        else:
                            print(tag.text.encode('utf-8'))
                            ond+=1
                            # print(ond)
                            tag = tag.nextSibling
                    else:
                        tag = tag.nextSibling
                        
                ep_link = [edicao]*(ond-1)
                ep_nome = [ed_content.find('h2', {'class':'post-title'}).text]*(ond-1)
                print(len(ep_nome))
                try:
                    setimo_selo_ep = [i.text for i in ed_content.find({'h4':'Dicas do Sétimo Selo e links'}).findAllNext({'p','ul'},limit=ond-1)]
                    # dica_link = []
                    # for j in setimo_selo_ep:
                    #     dica_url = j.findNext('a')
                    #     print(dica_url)
                    #     dica_link.append(dica_url['href'])
                    dica_link = [j['href'] for j in ed_content.find({'h4':'Dicas do Sétimo Selo e links'}).findAllNext({'a'},limit=ond-1)]
                    # dica_link = []
                    # for j in ed_content.find({'strong':'Dicas do Sétimo Selo e link'}).findAllNext(limit=ond-1):
                    #     if j.text == 'Textos e links' or j.text == 'Textos':
                    #         dica_link.append('')
                    #     else: 
                    #         if hasattr(j.find('a'),'href'):
                    #             dica_link.append(j.find('a')['href'])
                    #         else:
                    #             dica_link.append(j.text)
                    print(len(dica_link))
                    print(dica_link)
                except:
                    try:
                        print("Não achou h4")
                        setimo_selo_ep = [i.text for i in ed_content.find({'strong':'Dicas do Sétimo Selo e links'}).findAllNext({'p','ul'},limit=ond-1)]
                        dica_link = [j['href'] for j in ed_content.find({'strong':'Dicas do Sétimo Selo e links'}).findAllNext({'a'},limit=ond-1)]
                    except:
                        try:
                            setimo_selo_ep = [i.text for i in ed_content.find({'strong':'Dicas do Sétimo Selo'}).findAllNext({'p','ul'},limit=ond-1)]
                            # dica_link = []
                            # for j in ed_content.find({'strong':'Dicas do Sétimo Selo'}).findAllNext(limit=ond-1):
                            #     print(j)
                            #     if hasattr(j.find('a'),'href'):
                            #         dica_link.append(j['href'][0])
                            #     else:
                            #         dica_link.append(j.text)
                            dica_link = [j['href'][0] for j in ed_content.find({'strong':'Dicas do Sétimo Selo'}).findAllNext({'a'},limit=ond-1)]
                        except: 
                            setimo_selo_ep = [i.text for i in ed_content.find({'strong':'Textos e links'}).findAllNext({'p','ul'},limit=ond-1)]
                            dica_link = [j['href'] for j in ed_content.find({'strong':'Textos e links'}).findAllNext({'a'},limit=ond-1)]

                df = pd.DataFrame({'nome':ep_nome,'link':ep_link, 'dicas':setimo_selo_ep,'dica-link': dica_link})
                d = pd.concat([d,df])
    print(d)
    return d
        # df.to_csv('page-' + str(u), index=False)

i = 1
while i < 19:
    url_p = url + str(i)
    print(url_p)
    df_setimoselo = pd.concat([df_setimoselo,scrp(url_p)])
    i+=1
# print(scrp(url,df_setimoselo))
#print(len(episodes_link))
#print(setimo_selo)
df_setimoselo.to_csv('setimo_selo.csv')
