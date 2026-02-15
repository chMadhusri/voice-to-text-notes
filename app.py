import streamlit as st
import whisper
import tempfile

st.title("🎙️ Voice-to-Text Notes Generator (Free Version)")

uploaded_file = st.file_uploader(
    "Upload your meeting audio",
    type=["mp3", "wav", "m4a"]
)

if uploaded_file is not None:
    st.audio(uploaded_file)

    if st.button("Generate Notes"):

        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(uploaded_file.read())
            temp_audio_path = tmp.name

        st.write("Transcribing audio...")

        model = whisper.load_model("base")
        result = model.transcribe(temp_audio_path)

        transcript = result["text"]

        # Show Full Transcript
        st.subheader("📄 Full Transcript")
        st.write(transcript)

        # Structured Notes Section
        st.subheader("📝 Structured Meeting Notes")

        sentences = [s.strip() for s in transcript.split(".") if s.strip() != ""]

        # Agenda (First sentence as topic)
        st.markdown("### 📌 Agenda")
        if len(sentences) > 0:
            st.write(sentences[0])

        # Key Points
        st.markdown("### 📝 Key Points")
        for s in sentences[:5]:
            st.write("- " + s)

        # Action Items (basic rule-based detection)
        st.markdown("### ✅ Action Items")
        for s in sentences:
            if "will" in s.lower() or "should" in s.lower():
                st.write("- " + s)

        # Download Button
        st.download_button(
            label="📥 Download Notes",
            data=transcript,
            file_name="meeting_notes.txt",
            mime="text/plain"
        )