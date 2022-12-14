import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from wordcloud import wordcloud, STOPWORDS, WordCloud
import matplotlib.pyplot as plt

st.title("Sentiment Analysis of Tweets about US Airlines")
st.sidebar.title("Sentiment Analysis of Tweets about US Airlines")
st.set_option('deprecation.showPyplotGlobalUse', False)

st.markdown(" This application is a Streamlit dashboard to analyze the sentiment of Tweets 🐦")
st.sidebar.markdown(" This application is a Streamlit dashboard to analyze the sentiment of Tweets 🐦")

DATA_URL = ("./Tweets.csv")

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
if not st.sidebar.checkbox("Hide", True, key="2"):
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
if not st.sidebar.checkbox("Close", True, key="4"):
    st.markdown("## Tweet locations based on the time and day")
    st.markdown("%i tweets between %i:00 and %i:00" % (len(modified_data), hour, (hour+1)%24))
    st.map(modified_data)
    if st.sidebar.checkbox("Show raw data", False):
        st.write(modified_data)

# Plot number of tweets by sentiment for each Airline
st.sidebar.subheader("Breakdown airline tweets by sentiment")
# Multi select widget
choice = st.sidebar.multiselect("Pick airlines", ("US Airways", "United", "American", "Southwest", "Delta", "Virgin America"), key="0")

# Show the histo only when user need and no error
if len(choice) > 0:
    choice_data = data[data.airline.isin(choice)]
    fig_choice = px.histogram(choice_data, x="airline", y="airline_sentiment", histfunc="count", color="airline_sentiment",
    facet_col="airline_sentiment", labels={"airline_sentiment":"tweets"}, height=600, width=800)
    st.plotly_chart(fig_choice)

# Word Cloud for sentiment tweets
st.sidebar.header("Word Cloud")
word_sentiment = st.sidebar.radio("Display word cloud for what sentiment?", ("positive", "neutral", "negative"))

# Define functionality
if not st.sidebar.checkbox("Hide", True, key="3"):
    st.header("Word cloud for %s sentiment" % (word_sentiment))
    df = data[data["airline_sentiment"]==word_sentiment]
    words = " ".join(df["text"])
    processed_words = " ".join([word for word in words.split() if "http" not in word and not word.startswith("@") and word != "RT"])
    wordcloud = WordCloud(stopwords=STOPWORDS, background_color="white", height=640, width=800).generate(processed_words)
    plt.imshow(wordcloud)
    plt.xticks([])
    plt.yticks([])
    st.pyplot()
