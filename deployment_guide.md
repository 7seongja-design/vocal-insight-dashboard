# Vocal Insight Dashboard - 배포 및 공유 가이드

이 가이드는 완성된 **Vocal Insight Dashboard (PRO Version)**를 GitHub에 업로드하고, Streamlit Cloud를 통해 전 세계 어디서나 접속할 수 있는 웹 앱으로 배포하는 과정을 안내합니다.

---

## 🚀 1단계: GitHub 저장소 업로드 (필수)
Streamlit Cloud는 GitHub 저장소의 코드를 읽어와서 실행합니다. 따라서 코드를 먼저 GitHub에 올려야 합니다.

**사용자의 PC에서 진행할 작업:**
1. **GitHub 로그인:** [GitHub](https://github.com/)에 로그인합니다.
2. **새 저장소 생성:** 우측 상단의 `+` 버튼 -> `New repository` 클릭.
   - Repository name: `vocal-insight-dashboard` (또는 원하는 이름)
   - Public 선택 -> `Create repository` 클릭.
3. **코드 업로드 (터미널 명령어):**
   `d:/개발/my vocal` 폴더에서 터미널(VS Code 터미널 등)을 열고 아래 명령어를 순서대로 입력하세요.

   ```bash
   # git 초기화
   git init

   # 모든 파일 추가 (app.py, requirements.txt, .streamlit/config.toml 등)
   git add .

   # 커밋 (저장)
   git commit -m "feat: Add advanced vocal metrics and insights"

   # 원격 저장소 연결 (Github에서 생성한 주소로 변경하세요!)
   # 예: git remote add origin https://github.com/사용자아이디/vocal-insight-dashboard.git
   git remote add origin https://github.com/<YOUR_GITHUB_USERNAME>/vocal-insight-dashboard.git

   # 브랜치 이름 변경 및 업로드
   git branch -M main
   git push -u origin main
   ```

---

## ☁️ 2단계: Streamlit Cloud 배포
코드가 GitHub에 올라갔다면, 이제 서버를 띄울 차례입니다.

1. [Streamlit Cloud](https://streamlit.io/cloud)에 접속 및 로그인 (GitHub 계정 연동).
2. **"New app"** 클릭.
3. **Deploy an app** 화면에서:
   - **Repository:** 방금 업로드한 `vocal-insight-dashboard` 선택.
   - **Branch:** `main`
   - **Main file path:** `app.py`
4. **"Deploy!"** 클릭.

### ☕ 잠시 기다리기
Streamlit이 자동으로 필요한 라이브러리(`requirements.txt`에 명시된 librosa 등)를 설치하고 앱을 실행합니다. 약 1~3분 정도 소요됩니다.

---

## 🔑 3단계: Secrets 관리 (선택 사항)
만약 API 키(예: OpenAI API 등)를 사용한다면 Streamlit Cloud 대시보드에서 설정해야 합니다. (이 프로젝트는 현재 API 키가 필요 없습니다.)

- **설정 위치:** App Settings (앱 우측 상단 점 3개) -> `Secrets`.
- **형식:** TOML 형식을 따릅니다.
  ```toml
  # .streamlit/secrets.toml 예시
  # [api]
  # key = "sk-..."
  ```

---

## 🎉 4단계: 공유하기
배포가 완료되면 화면 상단에 URL이 표시됩니다.
- 예: `https://vocal-insight-dashboard-xyz.streamlit.app`
- 이 링크를 복사해서 동료나 가족에게 카카오톡, 이메일로 보내면 바로 접속해서 보컬 분석을 체험해볼 수 있습니다!

---

## 🛠️ 문제 해결 (FAQ)
- **Q: "ModuleNotFoundError: No module named 'librosa'" 에러가 나요.**
  - A: `requirements.txt` 파일이 GitHub 최상위 폴더에 있는지 확인하세요. 오타가 없는지도 체크하세요.
- **Q: 앱이 너무 느려요.**
  - A: Streamlit Cloud(무료 티어)는 리소스를 공유합니다. Librosa 분석은 CPU를 많이 쓰므로 큰 파일(10MB 이상)은 분석에 시간이 걸릴 수 있습니다.
