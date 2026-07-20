import streamlit as st
import time
from text_summarizer import TextSum
import main

keyword_hist = ""
key_temp = ""
keyword_list = ""

st.set_page_config(page_title="Real-Time Speech Transcription", layout="centered")

# Start audio threads (if not already started)
if "started" not in st.session_state:
    main.start_background_threads()
    st.session_state.started = True

st.title("Real-Time Transcription Viewer")

# Display transcription live
transcript_box = st.empty()
keyword_box = st.empty()

with st.sidebar:
    st.markdown("Options")
    if st.button("Summarize Speech"):
        summarizer = TextSum(speech=main.shared_state["speech"])
        summary = summarizer.text_summarization()
        st.markdown("Summarized Text")
        st.success(summary)

# Refresh loop
while True:
    text = main.shared_state["speech"]
    key_phrases = main.shared_state["keywords"]
    transcript_box.markdown(f"### Transcription\n{text}")
    key_phrases = [word[0]+': '+str(word[1]) for word in key_phrases if word[1] >= 0.4 and word[0] not in keyword_hist]
    key_temp = ' '.join(key_phrases)
    keyword_hist += key_temp
    key_phrases = " ".join(key_phrases)
    keyword_list += key_phrases
    keyword_box.markdown(f"### Keywords: `{keyword_list}`")
    time.sleep(2)
