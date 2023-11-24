# created the main python file
import streamlit as st
import pandas as pd
import requests
import snowflake.connector
from urllib.error import URLError

st.title('My Parents New Healthy Diner')
st.header('Breakfast Menu')
st.text('🥣 Omega 3 & Blueberry Oatmeal')
st.text('🥗 Kale, Spinach & Rocket Smoothie')
st.text('🐔 Hard-Boiled Free-Range Eggs')
st.text('🥑🍞 Avocado Toast')

st.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = st.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Banana'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page
st.dataframe(fruits_to_show)

# New section to display fruityvice api response
# First simple version
# st.header("Fruityvice Fruit Advice!")
# fruit_choice = st.text_input('What fruit would you like information about?','Kiwi')
# st.write('The user entered ', fruit_choice)
# fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
# normalize the json response 
# fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
# display the normalize table on the screen
# st.dataframe(fruityvice_normalized)

# Better production version using functions
# function definition
def get_fruityvice_data(this_fruit_choice):
   fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
   fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
   return fruityvice_normalized

# display fruityvice api response
st.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = st.text_input('What fruit would you like information about?')
  if not fruit_choice:
    st.error('Please select a fruit to get information.')
  else:
    back_from_function = get_fruityvice_data(fruit_choice)
    st.dataframe(back_from_function)

except URLError as e:
  st.error()
# end of new version

# st.stop()

# add snowflake query: first simple version - run every time
# my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
# my_cur = my_cnx.cursor()
# my_cur.execute("SELECT * from fruit_load_list")
# my_data_rows = my_cur.fetchall()
# st.header("The fruit load list contains:")
# st.dataframe(my_data_rows)

# snowflake query new version: run when clicking on a button
st.header("The fruit load list contains:")
#snoflake-related functions
def get_fruit_load_list():
   with my_cnx.cursor() as my_cur:
      my_cur.execute("SELECT * from fruit_load_list")
      return my_cur.fetchall()

# add a button to load the fruit
if st.button('Get Fruit Load List'):
   my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
   my_data_rows = get_fruit_load_list()
   st.dataframe(my_data_rows)

# st.stop()

# New section to add selected fruit: first simple version with no Control of Flow
# add_my_fruit = st.text_input('What fruit would you like to add?','starfruit')
# st.write('Thanks for adding ', add_my_fruit)
# my_cur.execute("insert into fruit_load_list values ('from streamlit')")

# select a fruit new version
def insert_row_snowflake(new_fruit):
   with my_cnx.cursor() as my_cur:
      my_cur.execute("insert into fruit_load_list values ('" + add_my_fruit +"')")
      return 'Thanks for adding ' + add_my_fruit

add_my_fruit = st.text_input('What fruit would you like to add?')
if st.button('Add a Fruit to the List'):
   my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
   back_from_function = insert_row_snowflake(add_my_fruit)
   st.text(back_from_function)




