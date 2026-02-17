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
                insight_text += f"<li><b>다이내믹 표현력 (Dynamic Representation)</b>: 우수합니다. 다이내믹 레인지가 <b>{abs(dynamic_range):.1f} dB</b>로 측정되었으며, 부드러운 속삭임부터 파워풀한 성량까지 넓은 감정의 스펙트럼을 보여줍니다.</li>"
            else:
                insight_text += f"<li><b>다이내믹 표현력 (Dynamic Representation)</b>: 일정합니다. 다이내믹 레인지가 <b>{abs(dynamic_range):.1f} dB</b>로 측정되었으며, 흔들림 없이 꾸준하고 안정적인 볼륨 컨트롤을 보여줍니다.</li>"

            # Brightness Logic
            if max_centroid > 3000:
                insight_text += f"<li><b>음색 분석 (Timbre Analysis)</b>: 클라이맥스 구간에서 주파수 중심값(Spectral Centroid)이 <b>{int(max_centroid)} Hz</b>에 달합니다. 이는 <b>매우 밝고 시원한 음색</b>을 나타내며, 반주를 뚫고 나오는 명료한 보컬 질감을 증명합니다.</li>"
            elif avg_centroid < 1500:
                insight_text += f"<li><b>음색 분석 (Timbre Analysis)</b>: 따뜻합니다. 평균 주파수 중심값이 <b>{int(avg_centroid)} Hz</b>로, 중후하고 풍성한 저음역대의 매력이 돋보이는 음색입니다.</li>"
            else:
                insight_text += f"<li><b>음색 분석 (Timbre Analysis)</b>: 균형 잡혀 있습니다. 평균 주파수 중심값이 <b>{int(avg_centroid)} Hz</b>로, 과하게 밝거나 어둡지 않은 편안하고 자연스러운 톤을 가지고 있습니다.</li>"

            # Stability Logic
            if avg_pitch_stability > 80:
                insight_text += f"<li><b>음정 제어력 (Pitch Control)</b>: 매우 뛰어난 안정성(<b>{avg_pitch_stability:.1f}/100</b>)을 보여줍니다. 크로마 분석 결과, 음정이 흔들림 없이 목표 피치에 정확하게 고정되어 있습니다.</li>"
            elif avg_pitch_stability < 60:
                insight_text += f"<li><b>음정 제어력 (Pitch Control)</b>: 다소 불안정(<b>{avg_pitch_stability:.1f}/100</b>)합니다. 호흡이 불안정하거나 바이브레이션의 폭이 넓어 피치가 흔들리는 구간이 감지됩니다.</li>"
            else:
                insight_text += f"<li><b>음정 제어력 (Pitch Control)</b>: 준수합니다(<b>{avg_pitch_stability:.1f}/100</b>). 훈련된 보컬리스트의 특징인 안정적인 피치 유지가 관찰됩니다.</li>"

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

    # Technical Guide Section
    st.divider()
    with st.expander("💡 분석 지표 알아보기 (Technical Guide)"):
        st.markdown("""
        - **Waveform (Amplitude vs Time)**: 소리의 크기 변화를 나타냅니다. 파형의 폭이 넓을수록 성량이 풍부하며, 곡의 감정선에 따른 다이내믹(강약 조절)을 확인할 수 있습니다.
        - **Spectrogram (Frequency vs Time)**: 소리의 성질(음색)을 보여줍니다. 세로축의 주파수 에너지가 높고 밝을수록 '시원하고 쨍한' 고음(배음)이 잘 형성된 것입니다.
        - **Pitch/Chroma (Note vs Time)**: 어떤 음정을 냈는지 분석합니다. 특정 음계 라인에 빨간색 블록이 흔들림 없이 길게 유지될수록 음정이 정확하고 안정적임을 의미합니다.
        """)

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
