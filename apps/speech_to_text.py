import streamlit as st


def app():
    st.title("Speech to text")

    st.markdown(
        """
        The aim of this part is to obtain some text after a recording
    After recording an audio, we need to transcript the text so that we can later
    analyze with NLP whether the elder has an important issue. We used a pretrained
    Speech recognition model
    """
    )

    st.code('''
from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC

processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-base-960h")
model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-960h")
''')

    st.markdown('We load the recorded audio from the file input.wav')

    st.code('''
import librosa

speech, rate = librosa.load("input.wav", sr=16_000)
input_audio = processor(speech, return_tensors = 'pt', sampling_rate=16_000).input_values
''')

    st.markdown('And then the translation is as easy as:')

    st.code('''
logits = model(input_audio).logits
predicted_ids = torch.argmax(logits, dim =-1)
transcriptions = processor.decode(predicted_ids[0]).lower()
print(transcriptions)
''')

    st.markdown('An example that this code produces will be a string like:')
    st.code('''

print("Result", transcriptions)
''')
    st.markdown('*Result*: hello i need help need a doctor')

