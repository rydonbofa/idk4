#!venv/bin/python3.9

import subprocess
import bs4


def get_running_services():
    command = """systemctl list-units |grep hide\.me |grep -v "system-hide" |awk '{ print $1" " $4}'"""
    return list(filter(None,subprocess.check_output(command, shell=True).decode("UTF-8").split("\n")))



with open("temp.html", "r") as f:
    temp = f.read()


soup = bs4.BeautifulSoup(temp, features="html.parser")


data = []
table = soup.find('table')
table_body = table.find('tbody')

rows = table_body.find_all('tr')
for row in rows:
    cols = row.find_all('td')
    cols = [ele.text.strip() for ele in cols]
    for col in cols:
        if "Linux" in col or "Details" in col or col == "":
            cols.remove(col)
    img = row.find('img')
    if img:
        cols.append(img['src'])
    if len(cols) > 1:
        data.append([ele for ele in cols if ele]) # Get rid of empty values


print(data)
#print(result)