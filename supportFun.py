import imaplib

import pandas as pd
from bs4 import BeautifulSoup
import email

def loginServer(imap_user,imap_pass,imap_host):
  # connect to host using SSL
  imap = imaplib.IMAP4_SSL(imap_host)
  ## login to server
  imap.login(imap_user, imap_pass)

  imap.select('Inbox')

  tmp, data = imap.search(None, 'SUBJECT', '"Your Swiggy order summary"')
  count = 0
  table = pd.DataFrame(columns=['Year','Month','Date','Quantity'])
  for num in data[0].split():
    tmp, data = imap.fetch(num, '(RFC822)')
    doc = {
      'mail': data[0][1].decode('UTF-8')
    }
    email_message = email.message_from_string(doc['mail'])
    date = email.utils.parsedate_tz(email_message['Date'])
    soup = BeautifulSoup(doc['mail'], 'html.parser')
    count = count + 1
    table = table.append(pd.DataFrame([[int(date[0]),int(date[1]),int(date[2]),getQuantity(soup)]],
                         columns=['Year','Month','Date','Quantity']),
                         ignore_index=True )

  imap.close()
  return  table

def getQuantity(soup):
  count_table = 0
  quantity = []
  for table in soup.find_all('table'):
    count_table += 1
    td_ele = table.find_all('td')
    if len([1 for td_ele in table.find_all('td') if "Quantity" in td_ele.getText().strip()]) > 0:
      break
  rows = table.find_all('tr')
  for row in rows:
    cols = row.find_all('td')
    for col in cols:
      try:
        quantity.append(int(col.getText().strip()))
      except:
        continue
  num_items = int(len(quantity) / 4)
  return num_items
