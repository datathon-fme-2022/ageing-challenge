import streamlit as st
from multiapp import MultiApp
from apps import speech_to_text, sentiment_analysis, demo

st.set_page_config(layout="wide")


apps = MultiApp()

# Add all your application here

apps.add_app("Speech to text", speech_to_text.app)
apps.add_app("Sentiment Analysis", sentiment_analysis.app)
apps.add_app("Demo", demo.app)


# The main app
apps.run()