# main.py

import streamlit as st
import pandas as pd
from deta import Deta
from streamlit_elements import elements, mui, html
from streamlit_elements import nivo

st.write("""
# Gas Log
""")

# Connect to Deta Base with your Project Key
# deta = Deta(st.secrets['deta_key'])

# Create a new database "wwlog-db"
# db = deta.Base("wwlog-db")

# db_content is a list of dictionaries. You can do everything you want with it.
# db_content = db.fetch().items

