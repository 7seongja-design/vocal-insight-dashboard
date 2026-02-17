# Vocal Insight Dashboard - 배포 및 공유 가이드

이 가이드는 완성된 **Vocal Insight Dashboard (PRO Version)**를 GitHub에 업로드하고, Streamlit Cloud를 통해 전 세계 어디서나 접속할 수 있는 웹 앱으로 배포하는 과정을 안내합니다.

---

## 🚀 1단계: GitHub 저장소 업로드 (완료됨)
이미 자동화 스크립트를 통해 GitHub에 코드가 업로드되었습니다. 아래 링크에서 확인하실 수 있습니다.

👉 **GitHub 저장소 바로가기:** [https://github.com/7seongja-design/vocal-insight-dashboard](https://github.com/7seongja-design/vocal-insight-dashboard)

---

## ☁️ 2단계: Streamlit Cloud 배포
코드가 GitHub에 올라갔다면, 이제 서버를 띄울 차례입니다.

1. [Streamlit Cloud](https://streamlit.io/cloud)에 접속 및 로그인 (GitHub 계정 연동).
2. **"New app"** 클릭.
3. **Deploy an app** 화면에서:
   - **Repository:** `7seongja-design/vocal-insight-dashboard` 선택 (자동 검색되거나 직접 입력).
   - **Branch:** `main`
   - **Main file path:** `app.py`
4. **"Deploy!"** 클릭.

### ☕ 잠시 기다리기
Streamlit이 자동으로 필요한 라이브러리(`requirements.txt`에 명시된 librosa 등)를 설치하고 앱을 실행합니다. 약 1~3분 정도 소요됩니다.

---

## 🔑 3단계: Secrets 관리 (선택 사항)
이 프로젝트는 현재 별도의 API 키가 필요 없습니다. 바로 배포하여 사용하시면 됩니다.

---

## 🎉 4단계: 공유하기
배포가 완료되면 화면 상단에 URL이 표시됩니다.
- 예: `https://vocal-insight-dashboard-xyz.streamlit.app`
- 이 링크를 복사해서 동료나 가족에게 카카오톡, 이메일로 보내면 바로 접속해서 보컬 분석을 체험해볼 수 있습니다!

---

## 🛠️ 문제 해결 (FAQ)
- **Q: 앱이 배포 중에 멈춰요.**
  - A: 가끔 Streamlit Cloud 서버 상태에 따라 지연될 수 있습니다. "Reboot app"을 눌러보세요.
- **Q: 앱이 너무 느려요.**
  - A: Streamlit Cloud(무료 티어)는 리소스를 공유합니다. Librosa 분석은 CPU를 많이 쓰므로 큰 파일(10MB 이상)은 분석에 시간이 걸릴 수 있습니다.
