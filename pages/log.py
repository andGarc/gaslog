# /pages/log.py

import streamlit as st
from deta import Deta
import pandas as pd

# Connect to Deta Base with your Project Key
deta = Deta(st.secrets['deta_key'])

st.write("""
# MPG Tracker
""")

with st.expander('Log a New Entry ✏️'):
    with st.form('log_form', clear_on_submit=True):

        actual_miles = st.number_input('Miles driven since last fill up', 
                            min_value=0.0, max_value=20000.0, step=0.01)

        date = st.date_input('Date')

        gallons = st.number_input('Gallons', 
                            min_value=0.0, max_value=20000.0, step=0.01)

        expected_miles = st.number_input('Expected Miles', 
                            min_value=0, max_value=600, step=1)


        # Every form must have a submit button.
        submitted = st.form_submit_button("Submit")

        # Create a new database "wwlog-db"
        db = deta.Base("gasolinelog-db")

        # If the user clicked the submit button,
        # write the data from the form to the database.
        if submitted:
            st.markdown(f"""
                📝 **Entry**
                - Date: `{date}`
                - Gallons: `{gallons} gal`
                - Expected Miles: `{expected_miles} mi`
            """)
            # New record
            db.put({'Date':date.strftime('%Y-%m-%d'),
                    'Gallons': gallons,
                    'Expected_Miles':expected_miles
                    })

            # Update last record with actual miles
            # fetch all entries
            db = deta.Base("gasolinelog-db")
            db_content = db.fetch().items
            df_content = pd.DataFrame(db_content)

            if df_content.shape[0] > 1:
                # sort dataframe
                df_content = df_content.sort_values(by=['Date'],ascending=False)
                # get latest value into a dic
                lastest_record =  df_content.iloc[1].to_dict()
                # update
                lastest_record['Actual_Miles'] = actual_miles
                db.put(lastest_record, lastest_record['key'])
            else:
                st.write('**First record recorded!**')
    
            st.markdown('**Entry recorded.**')

"---"
st.write("""
## Entries
""")

# fetch all entries
db = deta.Base("gasolinelog-db")
db_content = db.fetch().items
df_content = pd.DataFrame(db_content).sort_values(by=['Date'], ascending=False)
st.dataframe(data=df_content[['Date','Actual_Miles','Expected_Miles','Gallons']])



# be able to edit an entry 
