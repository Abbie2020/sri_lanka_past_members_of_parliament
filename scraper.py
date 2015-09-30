from lxml import html
import requests
import re
import scraperwiki
import time
import string

def do_the_scraping():
    index_url = "http://www.parliament.lk/members-of-parliament/index2.php?option=com_members&task=past&letter="    

    for letter in string.ascii_uppercase:
        data = requests.get(index_url + letter).json()
        for item in data:
            url = "http://www.parliament.lk/en/members-of-parliament/directory-of-members/viewMember/" + str(item['mem_intranet_id'])
            scrape_mp(url)
            time.sleep(0.5)

def scrape_mp(url):
    page = requests.get(url)
    tree = html.fromstring(page.text)
    id = url.rsplit('/',1)[1]
    find_mp_name = tree.xpath('//div[@class="components-wrapper"]/h2/text()') 
    if find_mp_name:
        name = find_mp_name[0].split(',',1)[0]
    else:
        name = ""
    find_party = tree.xpath('//td[div="Last elected Party"]/a[1]/text()')
    if find_party:
        party_list = find_party[0].split('(',1)
        party = party_list[0]
        party_id = party_list[1].split(')',1)[0]
    else:
        party = ""  
        party_id = ""                              
    find_district = tree.xpath('//td[div="Electoral District / National List"]/text()') 
    if find_district:
        area = find_district[0].strip()
    else:
        area = ""
    find_email = tree.xpath('//a[@onclick="getContactUs();"]/text()') 
    if find_email:
        email = find_email[0]
    else:
        email = ""
    find_image = tree.xpath('//div[@class="left-pic"]/img/@src') 
    if find_image:
        image = find_image[0]
    else:
        image = ""
    find_birth_date = tree.xpath('//td[span="Date of Birth"]/text()') 
    if find_birth_date:
        birth_date = find_birth_date[0].strip()
        birth_date = re.search(r'\d{1,2}-\d{1,2}-\d{2,4}', birth_date).group()
        birth_date = time.strptime(birth_date,'%d-%m-%Y')
        try:
            birth_date = time.strftime('%Y-%m-%d',birth_date)
        except:
            birth_date = ""
    else:
        birth_date = ""

    data = {
        'id': id,
        'name': name,
        'area': area,
        'party': party,
        'party_id': party_id,
        'email': email,
        'image': image,
        'birth_date': birth_date,
        'source': url,
        }
    print data
    scraperwiki.sqlite.save(unique_keys = ['id'], data = data)
        
do_the_scraping()
