import streamlit as st
import pandas as pd
import sounddevice as sd
import scipy.io.wavfile as wf
import plotly.express as px
import os
import cohere
from cohere.classify import Example



def app():
    if not os.path.exists('dades.csv'):
        df = pd.DataFrame(data=[{"Name": "Rogelia", "Recorded Text": "Help, I am dying", "lat": 41.39, "lon": 2.16}],
            columns=["Name", "Recorded Text", "lat", "lon"])
        df.to_csv('dades.csv')
    df = pd.read_csv('dades.csv')


    st.title("Demo - Granny's Watch")

    st.header("Short Description")
    st.markdown(
        """
    This site is a prototype of the product *Granny's Watch*. This product has the aim to 
    alert near people when an old person is in need. To make this demo more interactive, let's start
    by entering your name:
    """
    )
    name = st.text_input('Enter your name')


    st.header("Speech to text")

    st.markdown(
    """
    Let's start testing this app: To start the simulation we frst neeed to record an audio. 
    Remember that the audio you record must be in the use case of an elderly person having 
    (or not) an emergency. Some examples that we propose that you can say are: 
    - **Example One:** *"Help! I'm bleeding Help!"*
    - **Example Two:** *"Why is this stupid device on again if I'm fine"*
    - **Example Three:** *"I think I need a doctor please"*
    """
    )

    if st.button("Record"):

        # -- Record and save audio --
        sampling_rate = 16000  # Sample rate
        seconds = 5  # Duration of recording
        myrecording = sd.rec(int(seconds * sampling_rate), samplerate=sampling_rate, channels=2)
        sd.wait()  # Wait until recording is finished
        wf.write('recording.wav', sampling_rate, myrecording)  # Save as WAV file
        st.markdown('<p style="color:Green;">Succesfully Recorded Audio</p>', unsafe_allow_html=True)

        st.markdown('Now that we have the audio let\'s see the result of the speech to text recogntion:')
                # -- Load and transcript audio --
        with st.spinner('Loading speech recognition models'):
            from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC
            processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-base-960h") # load model and tokenizer
            model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-960h")
        
        with st.spinner('Transcipting audio'):
            import librosa
            import torch
            speech, rate = librosa.load("recording.wav", sr=sampling_rate)
            input_audio = processor(speech, return_tensors='pt', sampling_rate=sampling_rate).input_values
            logits = model(input_audio).logits
            predicted_ids = torch.argmax(logits, dim =-1)
            transcriptions = processor.decode(predicted_ids[0]).lower()
        st.markdown(f"""**Transcipted text:** {transcriptions}""")
                
        
        # -- Analyze if it's an emergency --
        st.header("Sentiment Analysis")
        st.markdown(f"""The next step is to make a sentiment analysis. We need to know if is an *Emergency* or is a *False Alarm*
        We have train a model with some sentences that an old person could say when is in a health danger and when is a 
        false alarms.
        """)

        co = cohere.Client('qhHPck58e98i1UFzeNHJigqcU3KhDOdokly1dN3G') # -> Main instance of coherence
        voice_samples = [
            Example("I need an ambulance", "Emergency"),
            Example("I need an help", "Emergency"),
            Example("Please hurry, I am in pain", "Emergency"),
            Example("I think I’ve broken a bone", "Emergency"),
            Example("I’m bleeding, need some help", "Emergency"),
            Example("Someone hit me and I think I hurt my nose", "Emergency"),
            Example("Call for an ambulance", "Emergency"),
            Example("I can't breathe", "Emergency"),
            Example("I falling son", "Emergency"),
            Example("I’m having trouble breathing", "Emergency"),
            Example("I am in pain", "Emergency"),
            Example("I think I’m having a heart attack", "Emergency"),
            Example("I'm getting very dizzy", "Emergency"),
            Example("I fell and my body hurts a lot", "Emergency"),
            Example("Can anyone help me?", "Emergency"),
            Example("My stomach hurts too much", "Emergency"),
            Example("My chest hurts", "Emergency"),
            Example("My head hurts", "Emergency"),
            Example("My leg hurts", "Emergency"),
            Example("I can’t see anything, I am afraid", "Emergency"),
            Example("My eyes are stinging for a few hours", "Emergency"),
            Example("My tooth has come out", "Emergency"),
            Example("I’ve dislocated my shoulder", "Emergency"),
            Example("I’ve put my back out", "Emergency"),
            Example("Please come quick, I am in such a pain", "Emergency"),
            Example("I fell off a ladder and I am bleeding", "Emergency"),
            Example("My heart is in such pain...", "Emergency"),
            Example("I am having a heart attack", "Emergency"),
            Example("I passed out and have been unconscious", "Emergency"),
            Example("Can you bring an ambulance?", "Emergency"),
            Example("Help Help I need medical assistance", "Emergency"),
            Example("Please hurry! There’s been an accident", "Emergency"),
            Example("Sorry, was a mistake", "False Alarm"),
            Example("I was scared but I'm fine", "False Alarm"),
            Example("False alarm, I don't need help", "False Alarm"),
            Example("No help needed around here", "False Alarm"),
            Example("Why does the device keep ringing if I'm fine?", "False Alarm"),
            Example("I'm fine, I'm fine, it was just a scare", "False Alarm"),
            Example("I don't need a doctor", "False Alarm"),
            Example("My heart is fine, I only have hippo", "False Alarm"),
            Example("I fell to the ground and despite having some pain, it's just a scratch", "False Alarm"),
            Example("You don't need to come", "False Alarm"),
            Example("I can breathe perfectly fine", "False Alarm"),
            Example("I do not need to go to a hospital", "False Alarm"),
            Example("Don't call an ambulance", "False Alarm"),
            Example("Sorry, I have touched something that is not...", "False Alarm"),
            Example("Oops I touched something I shouldn't", "False Alarm"),
            Example("Alarm of what? let me sleep in peace", "False Alarm"),
            Example("Help me turn off this device, I'm fine", "False Alarm"),
            Example("No need to send help", "False Alarm"),
            Example("Oops", "False Alarm"),
            Example("Why is the device on now? Nothing happens to me", "False Alarm"),
        ]

        response = co.classify(
        model='large',
        inputs=[transcriptions],
        examples=voice_samples,
        )            

        if response.classifications[0].prediction == 'False Alarm':
            st.markdown(f'Prediction: <p style="color:Green;">{response.classifications[0].prediction}</p>', unsafe_allow_html=True)
            st.markdown(f'Confidence: **{response.classifications[0].confidence}**', unsafe_allow_html=True)

            st.balloons()

        else:
            st.markdown(f'Prediction: <p style="color:Red;">{response.classifications[0].prediction}</p>', unsafe_allow_html=True)
            st.markdown(f'Confidence: **{response.classifications[0].confidence}**', unsafe_allow_html=True)

            st.markdown(f'Prediction: <p style="color:Red;">Emergency added!</p>', unsafe_allow_html=True)

            # Add point to the map if emergency
            import geocoder
            g = geocoder.ip('me')
            lat, lng = g.latlng
            df = df.append([{'Name': name, 'Recorded Text': transcriptions, 'lat': lat, 'lon': lng}])
            df.to_csv('dades.csv', index=False)

            # Enviar el missatge
            #import requests as r
            #r.post('http://127.0.0.1:5000/emergency',
            #    json={'name': name, 'lat': lat, 'lng': lng, 'message': transcriptions})

        
    st.header("Map Plot")
    # Map Part
    fig = px.scatter_mapbox(
        df,
        lat="lat",
        lon="lon",
        hover_name="Name",
        hover_data=["Recorded Text"],
        color_discrete_sequence=["red"],
        zoom=12,
        height=500
    )
    fig.update_traces(marker={'size': 15})
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    st.plotly_chart(fig)

