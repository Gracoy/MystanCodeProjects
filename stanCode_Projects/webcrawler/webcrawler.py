"""
File: webcrawler.py
Name: 姜佳成
--------------------------
This file collects more data from
https://www.ssa.gov/oact/babynames/decades/names2010s.html
https://www.ssa.gov/oact/babynames/decades/names2000s.html
https://www.ssa.gov/oact/babynames/decades/names1990s.html
Please print the number of top200 male and female on Console
You should see:
---------------------------
2010s
Male number: 10895302
Female number: 7942376
---------------------------
2000s
Male number: 12976700
Female number: 9208284
---------------------------
1990s
Male number: 14145953
Female number: 10644323
"""

import requests
from bs4 import BeautifulSoup


def main():
    for year in ['2010s', '2000s', '1990s']:
        url = f'https://www.ssa.gov/oact/babynames/decades/names{year}.html'
        response = requests.get(url)
        html = response.text
        soup = BeautifulSoup(html)
        # ----- Write your code below this line ----- #
        tags = soup.find_all('tr')  # Each 'tr' tag has several 'td' within it
        male_number = 0
        female_number = 0
        tds = list(tag('td') for tag in tags)  # tds = [[td1], [td2], [td3] ...]
        for td in tds:  # td = [Rank, Male_name, Male_number, Female_name, Female_number]
            if len(td) == 5:  # Some td tags are for web style, but the list length for storing data are all 5
                # The ',' in data must be removed before transfer str into int
                male_number += int(td[2].text.replace(',', ''))
                female_number += int(td[4].text.replace(',', ''))
        print('---------------------------')
        print(year)
        print(f'Male Number: {male_number}')
        print(f'Female Number: {female_number}')


if __name__ == '__main__':
    main()
