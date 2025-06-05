import streamlit as st
import altair as alt
import pandas as pd

df = pd.read_csv("listings.csv")

st.title("Austin AirBnB Dashboard")
st.markdown("Explore Austin, TX AirBnB listings interactively!")

df['price'] = df['price'].replace('[\$,]', '', regex=True).astype(float)
df = df[df['price'] < 1000] 

room_types = df['room_type'].dropna().unique().tolist()
neighborhood_names = df['neighbourhood_cleansed'].dropna().unique().tolist()
price_min, price_max = int(df['price'].min()), int(df['price'].max())

left_col, right_col = st.columns([2, 3])

# Filters in the wider left column
with left_col:
    st.header("Filters")
    selected_room_types = st.multiselect("Select Room Types", room_types, default=room_types)
    selected_neighborhoods = st.multiselect("Select Neighborhood Names", neighborhood_names, default=neighborhood_names)
    selected_price = st.slider("Select Price Range", min_value=price_min, max_value=price_max, value=(price_min, price_max))

df_filtered = df[
    (df['room_type'].isin(selected_room_types)) &
    (df['neighbourhood_cleansed'].isin(selected_neighborhoods)) &
    (df['price'].between(selected_price[0], selected_price[1]))
]

with right_col:
    st.subheader("1. Average Price by Room Type")
    chart1 = alt.Chart(df_filtered).mark_bar().encode(
        x=alt.X("room_type:N", title="Room Type"),
        y=alt.Y("mean(price):Q", title="Average Price"),
        color="room_type:N"
    ).properties(width=600, height=400)
    st.altair_chart(chart1, use_container_width=True)

    st.subheader("2. Number of Listings by Neighborhood Zip Code")
    chart2 = alt.Chart(df_filtered).mark_bar().encode(
        x=alt.X("count():Q", title="Number of Listings"),
        y=alt.Y("neighbourhood_cleansed:N", sort='-x', title="Neighborhood Name"),
        color="neighbourhood_cleansed:N"
    ).properties(width=600, height=600)
    st.altair_chart(chart2, use_container_width=True)

    st.subheader("3. Price vs Review Scores")
    chart3 = alt.Chart(df_filtered).mark_circle(size=60, opacity=0.6).encode(
        x=alt.X("review_scores_rating:Q", title="Review Score"),
        y=alt.Y("price:Q", title="Price"),
        color="room_type:N",
        tooltip=["name", "price", "review_scores_rating"]
    ).interactive().properties(width=700, height=400)
    st.altair_chart(chart3, use_container_width=True)
