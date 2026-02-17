import streamlit as st
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import io

# Page Configuration
st.set_page_config(
    page_title="Vocal Insight Dashboard PRO",
    page_icon="🎤",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    h1 {
        text-align: center;
        color: #1DB954; 
    }
    .stAudio {
        width: 100%;
    }
    .metric-card {
        background-color: #282828;
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
    }
    /* Highlight the insight box */
    .insight-box {
        border: 1px solid #1DB954;
        padding: 15px;
        border-radius: 10px;
        background-color: #121212;
        color: #FFFFFF;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("By Jaemin Lee")
    st.image("https://img.icons8.com/fluency/96/microphone.png", width=80) 
    st.markdown("---")
    st.header("Upload Audio")
    st.info("Supported formats: WAV, MP3")

# Main Content
st.title("🎤 Vocal Insight Dashboard PRO")
st.markdown("### Advanced Audio Analytics for Vocal Performance")

# File Uploader
uploaded_file = st.sidebar.file_uploader("Choose a vocal file", type=["mp3", "wav"])

if uploaded_file is not None:
    # Loading State
    with st.spinner('Analyzing audio file... performing deep feature extraction.'):
        try:
            # Load Audio
            y, sr = librosa.load(uploaded_file, sr=None)
            duration = librosa.get_duration(y=y, sr=sr)
            
            # --- 1. Basic Info Row ---
            st.markdown("#### 🎧 Basic Information")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Sample Rate", f"{sr} Hz")
            with col2:
                st.metric("Duration", f"{duration:.2f} s")
            with col3:
                st.metric("Channels", "Mono" if y.ndim == 1 else "Stereo") 
            
            st.audio(uploaded_file)
            st.divider()

            # --- 2. Advanced Metrics Calculation ---
            
            # A. Dynamic Range: Difference between Peak dB and Mean RMS dB
            rms = librosa.feature.rms(y=y)
            db_rms = librosa.amplitude_to_db(rms, ref=np.max)
            peak_db = np.max(db_rms)
            mean_db = np.mean(db_rms)
            dynamic_range = peak_db - mean_db # Approximate dynamic range
            
            # B. Spectral Centroid (Brightness)
            centroids = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
            avg_centroid = np.mean(centroids)
            max_centroid = np.max(centroids) # Peak brightness
            
            # C. Pitch Stability (Chroma Confidence)
            # Use chroma_stft. Calculate the max value per frame (how "certain" are we about the note?). 
            # Mean of these max values = Stability Score.
            chroma = librosa.feature.chroma_stft(y=y, sr=sr)
            pitch_confidence_per_frame = np.max(chroma, axis=0)
            avg_pitch_stability = np.mean(pitch_confidence_per_frame) * 100 # Convert to 0-100 scale
            
            # D. Spectral Flatness (Noise/Breathiness)
            flatness = librosa.feature.spectral_flatness(y=y)[0]
            avg_flatness = np.mean(flatness)
            
            # --- 3. Vocal Data Insight Section ---
            st.subheader("📊 Vocal Data Insight")
            
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Dynamic Range", f"{abs(dynamic_range):.1f} dB", help="Expression range (Peak - Average Volume)")
            m2.metric("Brightness (Centroid)", f"{int(avg_centroid)} Hz", help="Average frequency center. Higher = Brighter")
            m3.metric("Pitch Stability", f"{avg_pitch_stability:.1f}/100", help="Tonal clarity score (0-100)")
            m4.metric("Noise Factor", f"{avg_flatness:.4f}", help="Spectral Flatness (0=Tone, 1=Noise)")

            # Data-Driven Text Feedback
            insight_text = ""
            
            # Dynamic Range Logic
            if abs(dynamic_range) > 15:
                insight_text += f"<li><b>Dynamic Representation</b>: Excellent. The dynamic range is <b>{abs(dynamic_range):.1f} dB</b>, showing a wide emotional spectrum from soft whispers to powerful belts.</li>"
            else:
                insight_text += f"<li><b>Dynamic Representation</b>: Consistent. The dynamic range is <b>{abs(dynamic_range):.1f} dB</b>, suggesting a steady and controlled vocal performance.</li>"

            # Brightness Logic
            if max_centroid > 3000:
                insight_text += f"<li><b>Timbre Analysis</b>: The spectral centroid peaks at <b>{int(max_centroid)} Hz</b> in climax sections, indicating a <b>very bright and open vocal texture</b> capable of cutting through a mix.</li>"
            elif avg_centroid < 1500:
                insight_text += f"<li><b>Timbre Analysis</b>: The average centroid is <b>{int(avg_centroid)} Hz</b>, suggesting a <b>warm, grounded, and rich</b> vocal tone.</li>"
            else:
                insight_text += f"<li><b>Timbre Analysis</b>: Balanced brightness with an average centroid of <b>{int(avg_centroid)} Hz</b>.</li>"

            # Stability Logic
            if avg_pitch_stability > 80:
                insight_text += f"<li><b>Pitch Control</b>: Outstanding stability (<b>{avg_pitch_stability:.1f}/100</b>). The chroma features show distinct and unwavering pitch centers.</li>"
            elif avg_pitch_stability < 60:
                insight_text += f"<li><b>Pitch Control</b>: Variable (<b>{avg_pitch_stability:.1f}/100</b>). Detected fluctuations suggesting a breathy style or frequent pitch glides/vibrato.</li>"
            else:
                insight_text += f"<li><b>Pitch Control</b>: Good stability (<b>{avg_pitch_stability:.1f}/100</b>), characteristic of a trained vocalist.</li>"

            st.markdown(f"""
            <div class="insight-box">
                <h4>🎙️ Assistant Analysis</h4>
                <ul>
                {insight_text}
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            st.divider()
            
            # --- 4. Visualizations ---
            st.subheader("📈 Detailed Visualizations")
            
            # Waveform
            st.markdown("#### Waveform (Amplitude vs Time)")
            fig_wave, ax_wave = plt.subplots(figsize=(10, 2))
            ax_wave.set_facecolor('#191414')
            fig_wave.patch.set_facecolor('#191414')
            librosa.display.waveshow(y, sr=sr, ax=ax_wave, color='#1DB954', alpha=0.8)
            ax_wave.axis('off') # Cleaner look
            st.pyplot(fig_wave)
            
            col_spec, col_chroma = st.columns(2)
            
            with col_spec:
                st.markdown("#### Spectrogram")
                D = librosa.stft(y)
                S_db = librosa.amplitude_to_db(np.abs(D), ref=np.max)
                fig, ax = plt.subplots()
                ax.set_facecolor('#191414')
                fig.patch.set_facecolor('#191414')
                img = librosa.display.specshow(S_db, x_axis='time', y_axis='log', ax=ax, sr=sr, cmap='inferno')
                fig.colorbar(img, ax=ax, format="%+2.f dB")
                ax.set_xlabel("Time", color='white')
                ax.set_ylabel("Hz", color='white')
                ax.tick_params(colors='white')
                st.pyplot(fig)
                
            with col_chroma:
                st.markdown("#### Pitch/Chroma")
                fig, ax = plt.subplots()
                ax.set_facecolor('#191414')
                fig.patch.set_facecolor('#191414')
                img = librosa.display.specshow(chroma, y_axis='chroma', x_axis='time', ax=ax, cmap='coolwarm')
                fig.colorbar(img, ax=ax)
                ax.set_xlabel("Time", color='white')
                ax.set_ylabel("Pitch", color='white')
                ax.tick_params(colors='white')
                st.pyplot(fig)

        except Exception as e:
            st.error(f"Error processing audio file: {e}")

else:
    # Empty State
    st.container()
    st.markdown("""
    <div style='text-align: center; padding: 50px; background-color: #282828; border-radius: 10px; margin-top: 20px;'>
        <h3>👋 Welcome to Vocal Insight Dashboard PRO</h3>
        <p>Upload an audio file to receive a <b>Data-Driven Precision Report</b>.</p>
        <p style='color: #888;'>Data Insight Team</p>
    </div>
    """, unsafe_allow_html=True)
