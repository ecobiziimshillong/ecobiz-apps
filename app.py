import streamlit as st
from supportFun import loginServer,getQuantity
from PIL import Image

image = Image.open('EcoBiz New Logo 2_paint (1).jpg')
st.title('Swiggy Orders Environmental Cost Estimator')
imap_host = 'imap.gmail.com'
st.image(image)
imap_user = st.text_input('Enter the Email ID')
imap_pass = st.text_input('Enter the password', type = "password")


if st.button('Enter to get analytics'):
  quantity_table = loginServer(imap_user,imap_pass,imap_host)
  st.table(quantity_table)







