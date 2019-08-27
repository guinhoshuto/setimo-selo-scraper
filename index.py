import requests
import pandas as pd
from bs4 import BeautifulSoup
import bs4
import re

df_setimoselo = pd.DataFrame(columns=['nome','link', 'dicas', 'dica-link'])
url = 'https://xadrezverbal.com/category/audio/podcast-do-xadrez-verbal/page/'

text_stop = ['Canal do Xadrez Verbal no Telegram', 
             'Minutagem dos blocos, cortesia dos financiadores do Xadrez Verbal', 
             'Playlist das músicas de encerramento do Xadrez Verbal no Spotify',
             'Ouça o podcast aqui ou baixe o programa.']
tag_stop = ['h2', 'h3', 'h4']
ep_stop = ['https://xadrezverbal.com/2017/04/23/podcast-prorrogacao-01-nova-lei-de-imigracao-e-leitura-comentada/',
           'https://xadrezverbal.com/2017/05/18/podcast-prorrogacao-02-brasil-na-revisao-periodica-universal/',
           'https://xadrezverbal.com/2017/12/01/xadrez-verbal-podcast-121-iugoslavia-america-latina-e-coreia-do-norte/',
           'https://xadrezverbal.com/2016/02/22/recados-especiais-menino-neymar-e-peoes-do-podcast-do-apagao/', 
           'https://xadrezverbal.com/2015/08/06/musica-e-o-xadrez-verbal-respondendo-perguntas/',
           'https://xadrezverbal.com/2016/10/28/xadrez-verbal-podcast-70-oriente-medio-filipinas-e-venezuela/',
           'https://xadrezverbal.com/2015/07/17/xadrez-verbal-podcast-8-ira-nuclear-brics-e-grecia/', 
           'https://xadrezverbal.com/2015/07/03/xadrez-verbal-podcast-7-grecia-lgbt-e-mocambique/',
           'https://xadrezverbal.com/2015/06/26/xadrez-verbal-podcast-6-dilma-terrorismo-e-intolerancia/',
           'https://xadrezverbal.com/2015/05/29/xadrez-verbal-podcast-4-a-semana-na-politica-internacional/',
           'https://xadrezverbal.com/2015/05/22/xadrez-verbal-podcast-3-a-semana-na-politica-internacional/',
           'https://xadrezverbal.com/2015/05/15/xadrez-verbal-podcast-2-a-semana-na-politica-internacional/',
           'https://xadrezverbal.com/2015/05/08/xadrez-verbal-podcast-1-a-semana-na-politica-internacional/',
           'https://xadrezverbal.com/2015/06/12/xadrez-verbal-podcast-5-jerusalem-armenia-e-g7/',
           'https://xadrezverbal.com/2015/07/24/xadrez-verbal-podcast-9-africa-cuba-eua-e-euro/', 
           'https://xadrezverbal.com/2018/07/20/xadrez-verbal-podcast-150-israel-america-latina-e-cupula-trump-putin/']
ep_tres = ['https://xadrezverbal.com/2015/08/07/xadrez-verbal-podcast-11-eleicoes-na-venezuela-onu-e-egito/', 
           'https://xadrezverbal.com/2015/08/14/xadrez-verbal-podcast-12-arqueologia-diplomatas-turquia-e-curdos/',
           'https://xadrezverbal.com/2015/08/21/xadrez-verbal-podcast-13-renuncia-grega-dilma-e-merkel-e-imigracao/',
           'https://xadrezverbal.com/2015/08/28/xadrez-verbal-podcast-14-definicao-de-refugiado-libano-e-japao/',
           'https://xadrezverbal.com/2015/09/04/xadrez-verbal-podcast-15-colombia-venezuela-china-e-guatemala/']
ep_quatro = ['https://xadrezverbal.com/2015/09/04/xadrez-verbal-podcast-15-colombia-venezuela-china-e-guatemala/', 
             'https://xadrezverbal.com/2018/01/19/xadrez-verbal-podcast-125-inicio-de-2018/',   
             'https://xadrezverbal.com/2015/07/31/xadrez-verbal-podcast-10-leao-cecil-israel-africa-e-curdos/']
ep_cinco = ['https://xadrezverbal.com/2015/12/19/xadrez-verbal-especial-de-fim-de-ano-jerusalem-e-as-tres-religioes/']
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

        ond = 1
        if edicao in ep_stop: 
            print('episódio ignorado')
        elif edicao in ep_tres:
            ed_content = BeautifulSoup(requests.get(edicao).content, 'html.parser')
            tag = ed_content.find('h3', string='Ouça o podcast aqui ou baixe o programa.')
            ep_link = [edicao]*3
            ep_nome = [ed_content.find('h2', {'class':'post-title'}).text]*3
            setimo_selo_ep = [i.text for i in ed_content.findAll('h3')[1].findAllPrevious('p',limit=3)]
            dica_link = [j['href'] for j in ed_content.findAll('h3')[1].findAllPrevious('a',limit=3)]
            df = pd.DataFrame({'nome':ep_nome,'link':ep_link, 'dicas':setimo_selo_ep,'dica-link': dica_link})
            d = pd.concat([d,df])
        elif edicao in ep_quatro:
            ed_content = BeautifulSoup(requests.get(edicao).content, 'html.parser')
            ep_link = [edicao]*4
            ep_nome = [ed_content.find('h2', {'class':'post-title'}).text]*4
            try:
                setimo_selo_ep = [i.text for i in ed_content.findAll('h3')[1].findAllPrevious('p',limit=4)]
                dica_link = [j['href'] for j in ed_content.findAll('h3')[1].findAllPrevious('a',limit=4)]
            except:
                setimo_selo_ep = [i.text for i in ed_content.findAll('h2')[3].findAllPrevious('p',limit=4)]
                dica_link = [j['href'] for j in ed_content.findAll('h2')[3].findAllPrevious('a',limit=4)]
            df = pd.DataFrame({'nome':ep_nome,'link':ep_link, 'dicas':setimo_selo_ep,'dica-link': dica_link})
            d = pd.concat([d,df])
        elif edicao in ep_cinco:
            ed_content = BeautifulSoup(requests.get(edicao).content, 'html.parser')
            tag = ed_content.find('p', string='Links para baixar')
            ep_link = [edicao]*5
            ep_nome = [ed_content.find('h2', {'class':'post-title'}).text]*5
            setimo_selo_ep = [i.text for i in ed_content.find('p', string='Links para baixar').findAllPrevious('p',limit=5)]
            dica_link = [j['href'] for j in ed_content.find('p', string='Links para baixar').findAllPrevious('a',limit=5)]
            df = pd.DataFrame({'nome':ep_nome,'link':ep_link, 'dicas':setimo_selo_ep,'dica-link': dica_link})
            d = pd.concat([d,df])
        else:
            ed_content = BeautifulSoup(requests.get(edicao).content, 'html.parser')
            try:
                tag = ed_content.find('h4', string='Dicas do Sétimo Selo e links').findNext('p')
                print('entrou h4')
            except:
                try: 
                    tag = ed_content.find('p', string='Dicas do Sétimo Selo e links').findNext('p')
                    print('entrou p')
                except:
                    try:
                        tag = ed_content.find('strong', string='Dicas do Sétimo Selo e links').findNext('p')
                        print('entrou strong')
                    except:
                        try:
                            tag = ed_content.find('strong', string='Dicas do Sétimo Selo').findNext('p')
                            print('entrou dicas')
                        except:
                            try:
                                tag = ed_content.find('h4', string='Dicas e links').findNext('p')
                                print('entrou h4')
                            except:
                                try:
                                    tag = ed_content.find('strong', text=re.compile('no final do programa')).findNext('p')
                                    print('entrou p indicacoes')
                                except:
                                    tag = ed_content.find('strong', string='Textos e links').findNext('p')
                                    print('entrou p textos')
            print(tag.text.encode('utf-8'))
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
                setimo_selo_ep = [i.text for i in ed_content.find('h4', string='Dicas do Sétimo Selo e links').findAllNext({'p','ul'},limit=ond-1)]
                setimo_selo_ep = [i for i in setimo_selo_ep if i != 'Textos e links' or i != 'Textos']
                dica_link = [j['href'] for j in ed_content.find('h4',string='Dicas do Sétimo Selo e links').findAllNext({'a'},limit=ond-1)]
                print(len(dica_link))
                print(dica_link)
            except:
                try:
                    print("Não achou h4")
                    setimo_selo_ep = [i.text for i in ed_content.find('strong', string='Dicas do Sétimo Selo e links').findAllNext({'p','ul'},limit=ond-1)]
                    setimo_selo_ep = [i for i in setimo_selo_ep if i != 'Textos e links' or i != 'Textos']
                    dica_link = [j['href'] for j in ed_content.find('strong', string='Dicas do Sétimo Selo e links').findAllNext({'a'},limit=ond-1)]
                except:
                    try:
                        setimo_selo_ep = [i.text for i in ed_content.find('strong', string='Dicas do Sétimo Selo').findAllNext({'p','ul'},limit=ond-1)]
                        setimo_selo_ep = [i for i in setimo_selo_ep if i != 'Textos e links' or i != 'Textos']
                        dica_link = [j['href'] for j in ed_content.find('strong', string='Dicas do Sétimo Selo').findAllNext({'a'},limit=ond-1)]
                    except: 
                        setimo_selo_ep = [i.text for i in ed_content.find({'strong':'Textos e links'}).findAllNext({'p','ul'},limit=ond-1)]
                        setimo_selo_ep = [i for i in setimo_selo_ep if i != 'Textos e links' or i != 'Textos']
                        dica_link = [j['href'] for j in ed_content.find({'strong':'Textos e links'}).findAllNext({'a'},limit=ond-1)]

            df = pd.DataFrame({'nome':ep_nome,'link':ep_link, 'dicas':setimo_selo_ep,'dica-link': dica_link})
            d = pd.concat([d,df])
    print(d)
    return d
        # df.to_csv('page-' + str(u), index=False)

i = 1
while i < 28:
    url_p = url + str(i)
    print(url_p)
    df_setimoselo = pd.concat([df_setimoselo,scrp(url_p)])
    i+=1
# print(scrp(url,df_setimoselo))
#print(len(episodes_link))
#print(setimo_selo)
df_setimoselo.to_csv('setimo_selo.csv')
