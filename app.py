import streamlit as st
import pandas as pd
import sounddevice as sd
import scipy.io.wavfile as wf
import os

# Streamlit executa repetidament tot el codi escrit,
# i si detecta canvis actualitza dinàmicament la pàgina web

if not os.path.exists('dades.csv'):
    df = pd.DataFrame([[41.4, 2.17]], columns=['lat', 'lon'])
    df.to_csv('dades.csv')
df = pd.read_csv('dades.csv')

if st.button("Record"):

    # -- Record and save audio --
    sampling_rate = 16000  # Sample rate
    seconds = 5  # Duration of recording
    myrecording = sd.rec(int(seconds * sampling_rate), samplerate=sampling_rate, channels=2)
    sd.wait()  # Wait until recording is finished
    wf.write('recording.wav', sampling_rate, myrecording)  # Save as WAV file

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

    st.write('Transciprted text: ' + transcriptions)

    # -- Analyze if it's an emergency --

    import cohere
    from cohere.classify import Example
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
    st.write(response)

    if response.classifications[0].prediction == 'False Alarm':
        st.balloons()

    else:
        st.write('Emergency added!')
        # Add point to the map if emergency
        import geocoder
        g = geocoder.ip('me')
        lat, lng = g.latlng
        df = df.append([{'lat': lat, 'lon': lng}])
        df.to_csv('dades.csv', index=False)

    # Faltaria la part d'enviar el missatge


st.map(df)
