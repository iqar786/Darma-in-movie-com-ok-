import streamlit as st
from pytube import YouTube
from googletrans import Translator
from gtts import gTTS
import os

st.title("🎬 YouTube Video Dubbing App")
st.write("Paste a YouTube link, choose language, and get dubbed audio!")

# YouTube Link
url = st.text_input("🔗 Enter YouTube Video URL:")

# Language input
lang = st.text_input("🌍 Enter target language (e.g. 'ur' for Urdu, 'hi' for Hindi, 'en' for English):", "ur")

if st.button("Start Dubbing"):
    if url:
        try:
            yt = YouTube(url)
            st.write(f"🎥 Video Title: **{yt.title}**")

            # Subtitle simulation (we assume English captions exist)
            captions = yt.captions.get_by_language_code("en")
            if captions is None:
                st.error("❌ No English subtitles found for this video.")
            else:
                text = captions.generate_srt_captions()
                st.success("✅ Subtitles downloaded.")

                # Translate
                translator = Translator()
                translated = translator.translate(text, dest=lang)
                st.success(f"✅ Translated to {lang}")

                # Convert to speech
                tts = gTTS(translated.text, lang=lang)
                audio_file = "dubbed_audio.mp3"
                tts.save(audio_file)

                # Play + Download
                st.audio(audio_file)
                with open(audio_file, "rb") as f:
                    st.download_button("⬇️ Download Dubbed Audio", f, file_name="dubbed_audio.mp3")

        except Exception as e:
            st.error(f"⚠️ Error: {e}")
    else:
        st.warning("Please enter a YouTube link.")
