import streamlit as st


def app():
    st.title("Sentiment Analysis")

    st.markdown(
        """
    After transcripting the text, we analyze it in order to predict whether the text is a real Emergency or just a False Alarm.
    """
    )

    st.markdown("We used cohere's Client to train a model")

    st.code("""
# Imports of the document
import cohere
from cohere.classify import Example

co = cohere.Client('xxxxxxxxxxxxxxxxxxxx') # -> Main instance of coherence
    """)

    st.markdown('With only a few examples (about 50), the model is pretty accurate')

    st.code('''
voice_samples = [
    Example("I need an ambulance", "Emergency"),
    Example("Please hurry, I am in pain", "Emergency"),
    Example("Sorry, I have touched something that is not...", "False Alarm")
    # ...
]
''')

    st.markdown("And simply uring the cohere model with this few examples, we can try on new data")

    st.code("""
inputs=["It's hurting so much, I can't even breath",
        "Please hurry, I fell down",
        "Oops I pressed the wrong button"]

response = co.classify(
  model='large',
  inputs=inputs,
  examples=voice_samples,
)
""")
    st.markdown("We get the following predictions:")

    st.code("""
//Classification<prediction: "Emergency", confidence: 0.9993907>
//Classification<prediction: "Emergency", confidence: 0.9980647>
//Classification<prediction: "False Alarm", confidence: 0.9678431>""")

