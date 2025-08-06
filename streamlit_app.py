# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests
import pandas as pd

# Write directly to the app
st.title(f":cup_with_straw: Example Streamlit App :cup_with_straw:")
st.write(
  """Choose the fruits you want in your custom Smoothie!
  """
)


cnx = st.connection("snowflake")
session = cnx.session()

#option = st.selectbox(
#    "How would you like to be contacted?",
#    ("Banana", "Strawberries", "Peaches"),
#)

#st.write("Your favorite fruit is:", option)


name_on_order = st.text_input('Name on Smoothie: ')
st.write('The name on your Smoothie will be:', name_on_order)


#session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()
#my_dataframe_Id = session.table("smoothies.public.fruit_options").select(col('FRUIT_ID'))
#st.dataframe(data=my_dataframe_Id, use_container_width=True)

pd_df = my_dataframe.to_pandas()
#st.dataframe(pd_df)
#st.stop()


ingredients_list = st.multiselect('Choose up to 5 ingredients:', my_dataframe, max_selections = 5)

if ingredients_list:
    #st.write(ingredients_list)
    #st.text(ingredients_list)

    ingredients_string = ''

    for fruit_choose in ingredients_list:
        ingredients_string += fruit_choose + ' '
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_choose, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_choose,' is ', search_on, '.')
        st.subheader(fruit_choose + ' Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + fruit_choose)
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

    #st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""

    #st.write(my_insert_stmt)
    #st.stop()

    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")


#smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
#sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
