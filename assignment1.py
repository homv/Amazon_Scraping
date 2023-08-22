import requests
from bs4 import BeautifulSoup
import pandas as pd
import re



pages_dataset = pd.DataFrame()
headers = {
    "authority": "www.amazon.in",
    "method": "GET",
    "path": "/s?k=bags&page=5&crid=2M096C61O4MLT&qid=1692649346&sprefix=ba%2Caps%2C283&ref=sr_pg_5",
    "scheme": "https",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9",
    "Device-Memory": "8",
    "Downlink": "10",
    "Dpr": "1",
    "Ect": "4g",
    "Rtt": "50",
    "Sec-Ch-Device-Memory": "8",
    "Sec-Ch-Dpr": "1",
    "Sec-Ch-Ua": "\"Chromium\";v=\"116\", \"Not)A;Brand\";v=\"24\", \"Google Chrome\";v=\"116\"",
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": "\"Linux\"",
    "Sec-Ch-Ua-Platform-Version": "\"6.4.11\"",
    "Sec-Ch-Viewport-Width": "827",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
    "Viewport-Width": "827"
}

count=0
for i in range(1,21):
    url = f"https://www.amazon.in/s?k=bags&page={i}&crid=2M096C61O4MLT&qid=1692627594&sprefix=ba%2Caps%2C283&ref=sr_pg_{i}"
    r = requests.get(url,headers=headers)
    soup = BeautifulSoup(r.content, 'html5lib')
    get_section = soup.find_all('div', class_="sg-col sg-col-4-of-12 sg-col-8-of-16 sg-col-12-of-20 sg-col-12-of-24 s-list-col-right")

    for i in get_section:
        url = i.find('a', class_="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal").get('href')
        if 'sspa' not in url:
            #part2
            url = 'https://www.amazon.in' + url
            rpr = requests.get(url,headers=headers)
            souppr = BeautifulSoup(rpr.content, 'html5lib')
            get_sectionpr = souppr.find('div',id="detailBullets_feature_div")
            data_dict = {}
            if get_sectionpr:
                lis = get_sectionpr.find_all('li')
                for j in lis:
                    pro_det = [re.sub(r'\s+', ' ', x.text).strip() for x in j.find('span')][1:-1]
                    if pro_det:
                        data_dict[' '.join(pro_det[0].split(':')[0].split(' ')[0:-2])] = pro_det[-1]
            else:
                table1 = souppr.find('table',id="productDetails_techSpec_section_1")
                table2 = souppr.find('table',id="productDetails_detailBullets_sections1")
                table_rows = table1.find_all('th') if table1 else None
                table_rows_data = table1.find_all('td') if table1 else None
                table_rows2 = table2.find_all('th') if table2 else None
                table_rows_data2 = table2.find_all('td') if table2 else None
                data_dict={}
                data1 = [row.text.strip() for row in table_rows]
                data_val_2 = [row.text.strip()[1:] for row in table_rows_data]
                data = [row.text.strip() for row in table_rows2]
                data_val = [row.text.strip() for row in table_rows_data2]
                excep = {'Customer Reviews','Best Sellers Rank'}
                for inde in range(len(data)):
                    if data[inde] not in excep:
                        data_dict[data[inde]] = data_val[inde]
                for inde in range(len(data1)):
                    data_dict[data1[inde]] = data_val_2[inde]
            name_element = i.find('span', class_="a-size-medium a-color-base a-text-normal")
            name = name_element.text if name_element else None
            
            rating_element = i.find('span', class_="a-icon-alt")
            rating = rating_element.text.split()[0] if rating_element else None
            
            price_element = i.find('span', class_="a-price-whole")
            price = price_element.text if price_element else None
            
            no_of_reviews_element = i.find('span', class_='a-size-base s-underline-text')
            no_of_reviews = no_of_reviews_element.parent.parent['aria-label'] if no_of_reviews_element else None
            
            pages_dataset = pages_dataset._append({
                "Product URL": url,
                "Product Name": name,
                "Product Price": price,
                "Rating": rating,
                "Number of reviews": no_of_reviews
            }|data_dict, ignore_index=True)
            print(count)
            count+=1


pages_dataset.to_csv('assignment1.csv')