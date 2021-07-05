import json
import requests

from parser import get_new_jobs, is_programming

URL = 'https://api.telegram.org/bot1769543182:AAFP7NE728CXkpxuMk7CB4zXLBpoDNWYRYg/sendMessage?parse_mode=HTML'
with open('data.json') as file:
    data = json.load(file)
    TOKEN = data['token']
    CHAT_ID = data['chat_id']


def create_msg(title, description, category, link, payment=''):
    msg = {
        'text': f"<b>🔥 {title} 🔥</b>\n{ category}\n{payment if payment else 'Цена не указана'}\n\n{description}\n\n{link}\n",
        'chat_id': '@notiffer',
    }
    
    text = f"<b>🔥 {title} 🔥</b>\n <i>{category}</i> \n💸 {payment if payment else 'Цена не указана'}💸\n\n\n\n{link}\n"
    return text

while True:
  try:
    jobs = get_new_jobs()
    if jobs:
        for job in jobs:
            title = job.select('a.text-bold.show_visited')[0].text
            description = job.find('div', 'text_field')
            category = job.select('div.col-sm-8.text-muted.dot_divided a.text-muted')[0].text
            link = 'https://www.weblancer.net' + job.select('a.text-bold.click_target')[0]['href']
            
            if job.select('div.float-right.float-sm-none.title.amount.indent-xs-b0'):
                temp = job.find('div', 'float-right float-sm-none title amount indent-xs-b0').find('span')
                if temp:
                    payment = f"{temp['title']} • {temp.text}"
                else:
                    payment = None
                    
            if is_programming(job):
                requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={create_msg(title, description, category, link, payment)}&parse_mode=HTML")
  except:
    pass
  