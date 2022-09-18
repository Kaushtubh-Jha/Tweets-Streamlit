import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.title("Sentiment Analysis of Tweets about US Airlines")
st.sidebar.title("Sentiment Analysis of Tweets about US Airlines")

st.markdown(" This application is a Streamlit dashboard to analyze the sentiment of Tweets 🐦")
st.sidebar.markdown(" This application is a Streamlit dashboard to analyze the sentiment of Tweets 🐦")

DATA_URL = ("/home/rhyme/Desktop/Project/Tweets.csv")

@st.cache(persist=True)
def load_data():
    data = pd.read_csv(DATA_URL)
    data['tweet_created'] = pd.to_datetime(data['tweet_created'])
    return data

data = load_data()

# To Display Table
# st.write(data)

# Work with radio button and fetch single tweet for negative, positive and newtral
st.sidebar.subheader("Show random tweet")
random_tweet = st.sidebar.radio("Sentiment", ("positive", "neutral", "negative"))
st.sidebar.markdown(data.query("airline_sentiment == @random_tweet")[["text"]].sample(n=1).iat[0,0])

# Dropdown options
st.sidebar.markdown("### Number of tweets by sentiment")
select = st.sidebar.selectbox("Visualization type", ["Histogram", "Pie Chart"], key="1")

# Find total number of Tweets
sentiment_count = data["airline_sentiment"].value_counts()
# st.write(sentiment_count)
sentiment_count = pd.DataFrame({"Sentiment":sentiment_count.index, "Tweets":sentiment_count.values})

# Check box to hide the plot
if not st.sidebar.checkbox("Hide", True):
    st.markdown("### Number of tweets by sentiment")
    # User to select plotting as Histogram or Pie Chart
    if select == "Histogram":
        fig = px.bar(sentiment_count, x="Sentiment", y="Tweets", color="Tweets", height=500)
        st.plotly_chart(fig)
    else:
        fig = px.pie(sentiment_count, values="Tweets", names="Sentiment")
        st.plotly_chart(fig)

# Display Tweets Location
# st.map(data)

# Widget for hour updates
st.sidebar.subheader("When and where are users tweeting from?")
hour = st.sidebar.slider("Hour of day", 0, 23)
# hour = st.sidebar.number_input("Hour of day", min_value=1, max_value=24)
modified_data = data[data["tweet_created"].dt.hour == hour]
if not st.sidebar.checkbox("Close", True, key="1"):
    st.markdown("## Tweet locations based on the time and day")
    st.markdown("%i tweets between %i:00 and %i:00" % (len(modified_data), hour, (hour+1)%24))
    st.map(modified_data)
    if st.sidebar.checkbox("Show raw data", False):
        st.write(modified_data)
