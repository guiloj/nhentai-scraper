# was going to use urllib but nhentai was super rude and gave me a 403
# from urllib import request
# import chromedriver_binary
import time
import re
from selenium import webdriver
import os
# web webdriver/selenium stuff
options = webdriver.ChromeOptions()
# # was pissing me off with errors because i had my tablet plugged in
options.add_experimental_option('excludeSwitches', ['enable-logging'])
browser = webdriver.Chrome(options=options)

# gets all the links from this file and puts them in a list
with open('links.txt', 'r', encoding='utf-8') as f:
    links = f.readlines()

# gets all the numbers ever used by the bot to see if one was already used automatically
with open('dupli.txt', 'r', encoding='utf-8') as f:
    dupli = []
    f = f.readlines()
    for x in f:
        dupli.append(x.replace('\n',''))


for link in links:
    # checks if the list element is a number or a link than gets the link and number of each one
    if len(link) < 6:
        url = 'https://nhentai.net/g/'+link+'/'
        number = link
    else:
        url = link
        number = re.search("([0-9]+)", link).group(0)
    # checks if the number is in dupli.txt or not, if so warn the user and go back to the start of the for with the next elemnt
    if number in dupli:
        print(number, 'duplicated')
        continue
    # opens url (takes ages the first time)
    browser.get(url)
    # finds the element we are interested in
    search = browser.find_element_by_id('tags')
    # hippity hoppity that html is now my property
    html = search.get_attribute('innerHTML')
    # ladies and gentleman, I present to you, the worse code I have ever written in my whole life
    elem = html.split('\n')
    parodies = []; characters = []; tags = []; artists = []; groups = []; languages = []
    par = "class=\"name\"\>([- A-Za-z0-9_|]+)\<" # this took me way more time than it should
    for x in range(len(elem)):
        if 'Parodies:' in elem[x]:
            parodies = re.findall(par, elem[x+1])
        elif 'Characters:' in elem[x]:
            characters = re.findall(par, elem[x+1])
        elif 'Tags:' in elem[x]:
            tags = re.findall(par, elem[x+1])
        elif 'Artists:' in elem[x]:
            artists = re.findall(par, elem[x+1])
        elif 'Groups:' in elem[x]:
            groups = re.findall(par, elem[x+1])
        elif 'Languages:' in elem[x]:
            languages = re.findall(par, elem[x+1])

    # what? never heard of a dict
    p = ''; c = ''; t = ''; a = ''; g = ''; l = ''
    for x in parodies[:6]:
        p += ' <{}>'.format(x)
    for x in characters[:6]:
        c += ' <{}>'.format(x)
    for x in tags[:6]:
        t += ' <{}>'.format(x.replace('multi-work ', ''))
    for x in artists[:6]:
        a += ' <{}>'.format(x)
    for x in groups[:6]:
        g += ' <{}>'.format(x)
    for x in languages[:6]:
        l += ' <{}>'.format(x)
    # get the image link to make my life easier
    search = browser.find_element_by_id('cover')
    html = search.get_attribute('innerHTML')
    # im telling you man, im afraid of beautiful soup
    img = re.search("(?P<url>https?://[^\s]+)", html).group(0).replace('"', '')
    # add the thing to dupli
    with open('dupli.txt', 'a', encoding='utf-8') as f:
        f.write(number + '\n')
    # append output
    with open('output.txt', 'a', encoding='utf-8') as f:
        f.write("Tags:{}\nParodies:{}\nCharacters:{}\nArtists:{}\nGroups:{}\nLanguages:{}\n\n#{}\n{}\n{}\n\n\n".format(t, p, c, a, g, l, number, url, img))
    # looks like this:
    #
    # Tags: <tag1> <tag2> <tag3> <tag4> <tag5> <tag6> ...
    # Parodies: <parodie> ...
    # Characters: <character> ...
    # Artists: <artist> ...
    # Groups: <group> ...
    # Languages: <language> ...
    #
    # #000000
    # https://nhentai.net/g/000000/
    #
    # https://t.nhentai.net/galleries/0000000/cover.png
# my processor finally gets sweet relif
browser.quit()
