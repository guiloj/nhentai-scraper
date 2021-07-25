import time
import re
from selenium import webdriver
import os
import sys
os.chdir(r'C:/Users/guilo/Documents/Atom_Projects/Python/reddit')
os.system('cls' if os.name == 'nt' else 'clear')

print('''
░██████╗███████╗██╗░░░░░███████╗███╗░░██╗██╗██╗░░░██╗███╗░░░███╗
██╔════╝██╔════╝██║░░░░░██╔════╝████╗░██║██║██║░░░██║████╗░████║
╚█████╗░█████╗░░██║░░░░░█████╗░░██╔██╗██║██║██║░░░██║██╔████╔██║
░╚═══██╗██╔══╝░░██║░░░░░██╔══╝░░██║╚████║██║██║░░░██║██║╚██╔╝██║
██████╔╝███████╗███████╗███████╗██║░╚███║██║╚██████╔╝██║░╚═╝░██║
╚═════╝░╚══════╝╚══════╝╚══════╝╚═╝░░╚══╝╚═╝░╚═════╝░╚═╝░░░░░╚═╝

              █   █▀█ ▄▀█ █▀▄ █ █▄ █ █▀▀ 
              █▄▄ █▄█ █▀█ █▄▀ █ █ ▀█ █▄█ ▄ ▄ ▄''')

def get_tags(link, current, total):
    print('\033[K', end='\r')
    print(f'>>[?][{current}/{total}] parsing link', end='\r')
    if len(link) < 6:
        url = 'https://nhentai.net/g/'+link+'/'
        number = link
    else:
        url = link.replace('\n', '')
        number = re.search("([0-9]{1,6})", link).group(0)
    if number in dupli:
        print('\033[K', end='\r')
        print(f'>>[{number}][{current}/{total}] {number} is duplicaded', end='\r')
        return
    print('\033[K', end='\r')
    print(f'>>[{current}/{total}] opening ({url})...', end='\r')
    browser.get(url)
    print('\033[K', end='\r')
    print(f'>>[{number}][{current}/{total}] {url} opened', end='\r')
    search = browser.find_element_by_id('tags')
    html = search.get_attribute('innerHTML')
    info = html.split('\n')
    tags = {
        'parodies':[],
        'characters':[],
        'tags':[],
        'artists':[],
        'groups':[],
        'languages':[]
    }    
    print('\033[K', end='\r')
    print(f'>>[{number}][{current}/{total}] finding tags', end='\r')
    par = r"class=\"name\"\>([- A-Za-z0-9_|]+)\<"
    for x in range(len(info)):
        if 'Parodies:' in info[x]:
            tags['parodies'] = re.findall(par, info[x+1])
        elif 'Characters:' in info[x]:
            tags['characters'] = re.findall(par, info[x+1])
        elif 'Tags:' in info[x]:
            tags['tags'] = re.findall(par, info[x+1])
        elif 'Artists:' in info[x]:
            tags['artists'] = re.findall(par, info[x+1])
        elif 'Groups:' in info[x]:
            tags['groups'] = re.findall(par, info[x+1])
        elif 'Languages:' in info[x]:
            tags['languages'] = re.findall(par, info[x+1])
    print('\033[K', end='\r')
    print(f'>>[{number}][{current}/{total}] tags found', end='\r')
    
    tags['parodies'] = ' '.join(['<'+x+'>' for x in tags['parodies'][:6]])
    tags['characters'] = ' '.join(['<'+x+'>' for x in tags['characters'][:6]])
    tags['tags'] = ' '.join(['<'+x+'>' if x != 'multi-work ' else x.replace('multi-work', 'series') for x in tags['tags'][:6]])
    tags['artists'] = ' '.join(['<'+x+'>' for x in tags['artists'][:6]])
    tags['groups'] = ' '.join(['<'+x+'>' for x in tags['groups'][:6]])
    tags['languages'] = ' '.join(['<'+x+'>' for x in tags['languages'][:6]])

    search = browser.find_element_by_id('cover')
    html = search.get_attribute('innerHTML')
    img = re.search(r"(?P<url>https?://[^\s\"]+)", html).group(0)
    print('\033[K', end='\r')
    print(f'>>[{number}][{current}/{total}] img found', end='\r')
    with open('dupli.txt', 'a', encoding='utf-8') as f:
        f.write(number + '\n')
    
    print('\033[K', end='\r')
    print(f'>>[{number}][{current}/{total}] number written to dupli.txt', end='\r')
    with open('output.txt', 'a', encoding='utf-8') as f:
        f.write("Tags: {}\nParodies: {}\nCharacters: {}\nArtists: {}\nGroups: {}\nLanguages: {}\n\n#{}\n{}\n{}\n\n\n".format(tags['tags'], tags['parodies'], tags['characters'], tags['artists'], tags['groups'], tags['languages'], number, url, img))
    
    print('\033[K', end='\r')
    print(f'>>[{number}][{current}/{total}] output written to output.txt', end='\r')
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
browser = webdriver.Chrome(options=options)
os.system('cls' if os.name == 'nt' else 'clear')
print('''
                        ████████╗██╗░░██╗███████╗  
                        ╚══██╔══╝██║░░██║██╔════╝  
                        ░░░██║░░░███████║█████╗░░  
                        ░░░██║░░░██╔══██║██╔══╝░░  
                        ░░░██║░░░██║░░██║███████╗  
                        ░░░╚═╝░░░╚═╝░░╚═╝╚══════╝  

███████╗██╗░░░░░░█████╗░████████╗  ░█████╗░██╗░░██╗███████╗░██████╗████████╗  
██╔════╝██║░░░░░██╔══██╗╚══██╔══╝  ██╔══██╗██║░░██║██╔════╝██╔════╝╚══██╔══╝  
█████╗░░██║░░░░░███████║░░░██║░░░  ██║░░╚═╝███████║█████╗░░╚█████╗░░░░██║░░░  
██╔══╝░░██║░░░░░██╔══██║░░░██║░░░  ██║░░██╗██╔══██║██╔══╝░░░╚═══██╗░░░██║░░░  
██║░░░░░███████╗██║░░██║░░░██║░░░  ╚█████╔╝██║░░██║███████╗██████╔╝░░░██║░░░  
╚═╝░░░░░╚══════╝╚═╝░░╚═╝░░░╚═╝░░░  ░╚════╝░╚═╝░░╚═╝╚══════╝╚═════╝░░░░╚═╝░░░  

    ███████╗███╗░░██╗░░░░░██╗░█████╗░██╗░░░██╗███████╗██████╗░██╗░██████╗  
    ██╔════╝████╗░██║░░░░░██║██╔══██╗╚██╗░██╔╝██╔════╝██╔══██╗╚█║██╔════╝  
    █████╗░░██╔██╗██║░░░░░██║██║░░██║░╚████╔╝░█████╗░░██████╔╝░╚╝╚█████╗░  
    ██╔══╝░░██║╚████║██╗░░██║██║░░██║░░╚██╔╝░░██╔══╝░░██╔══██╗░░░░╚═══██╗  
    ███████╗██║░╚███║╚█████╔╝╚█████╔╝░░░██║░░░███████╗██║░░██║░░░██████╔╝  
    ╚══════╝╚═╝░░╚══╝░╚════╝░░╚════╝░░░░╚═╝░░░╚══════╝╚═╝░░╚═╝░░░╚═════╝░  

    ██╗░░██╗░█████╗░██╗░░░░░██╗░░░██╗  ██████╗░██╗██████╗░██╗░░░░░███████╗
    ██║░░██║██╔══██╗██║░░░░░╚██╗░██╔╝  ██╔══██╗██║██╔══██╗██║░░░░░██╔════╝
    ███████║██║░░██║██║░░░░░░╚████╔╝░  ██████╦╝██║██████╦╝██║░░░░░█████╗░░
    ██╔══██║██║░░██║██║░░░░░░░╚██╔╝░░  ██╔══██╗██║██╔══██╗██║░░░░░██╔══╝░░
    ██║░░██║╚█████╔╝███████╗░░░██║░░░  ██████╦╝██║██████╦╝███████╗███████╗
    ╚═╝░░╚═╝░╚════╝░╚══════╝░░░╚═╝░░░  ╚═════╝░╚═╝╚═════╝░╚══════╝╚══════╝''')
browser.get('file:///C:/path/to/your/html/file/start.html')
print('\n\n')
print('>>opening links.txt')
with open('links.txt', 'r', encoding='utf-8') as f:
    links = f.readlines()
print('>>done\n')

print('>>opening dupli.txt')
with open('dupli.txt', 'r', encoding='utf-8') as f:
    dupli = []
    f = f.readlines()
    print('>>iteraring')
    for x in f:
        dupli.append(x.replace('\n',''))

print('>>done\n')

input('>>proceed(enter): ')

print('\n>>entering for loop\n')
print('\033[K', end='\r')
print('>>starting...', end='\r')

nums = [*range(1, len(links)+1)]
for x, y in zip(links, nums):
    get_tags(x, y, len(links))

print('\n\n>>DONE')
browser.get('file:///C:/path/to/your/html/file/end.html')
input('>>exit(enter): ')
browser.quit()
sys.exit(0) 
