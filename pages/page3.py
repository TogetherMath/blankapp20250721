import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from datetime import date, timedelta
import os

# matplotlib 한글 폰트 설정
font_path = "./fonts/NanumGothic.ttf"
if os.path.exists(font_path):
    fm.fontManager.addfont(font_path)
    plt.rcParams['font.family'] = fm.FontProperties(fname=font_path).get_name()
else:
    st.warning("⚠️ 지정한 경로에 NanumGothic.ttf 파일이 없습니다. 한글이 깨질 수 있습니다.")
plt.rcParams['axes.unicode_minus'] = False  # 마이너스(-) 깨짐 방지


# -------------------------------
# 초기 설정
st.set_page_config(page_title="음식물 쓰레기 줄이기 실천 앱", layout="centered")
st.title("🍽️ 오늘도 음식 다 먹었나요?")
st.subheader("음식물 쓰레기 줄이기 실천 기록장")

# -------------------------------
# 사용자 입력
st.markdown("**1. 오늘 남긴 음식 종류와 양을 입력해보세요.**")

밥 = st.slider("밥", 0.0, 1.0, 0.0, 0.1, help="1.0은 한 공기 전체를 남겼다는 뜻입니다.")
국 = st.slider("국/찌개", 0.0, 1.0, 0.0, 0.1)
반찬 = st.slider("반찬", 0.0, 1.0, 0.0, 0.1)
과일 = st.slider("과일/디저트", 0.0, 1.0, 0.0, 0.1)

총_남긴_양 = 밥 + 국 + 반찬 + 과일  # 단순 합산

# -------------------------------
# 결과 출력
st.markdown("---")
st.markdown("**2. 오늘 남긴 음식 총량 요약**")

st.metric(label="🍛 오늘 남긴 총 음식량 (단위: 공기)", value=f"{총_남긴_양:.2f} 공기")

if 총_남긴_양 == 0:
    st.success("👏 훌륭해요! 오늘 음식물 쓰레기를 하나도 남기지 않았어요.")
elif 총_남긴_양 < 1:
    st.info("😊 꽤 잘했어요. 내일은 더 줄여볼까요?")
else:
    st.warning("⚠️ 음식물 쓰레기를 줄이기 위한 노력이 더 필요해요.")

# -------------------------------
# 기록 저장 (간단한 시뮬레이션용)
st.markdown("---")
st.markdown("**3. 이번 주 실천 기록 보기 (예시)**")

# 예시 데이터 생성
today = date.today()
dates = [today - timedelta(days=i) for i in range(6, -1, -1)]
values = [0.4, 0.2, 0.6, 0.1, 0.3, 0.0, 총_남긴_양]

df = pd.DataFrame({'날짜': dates, '남긴 음식량(공기)': values})

fig, ax = plt.subplots()
ax.plot(df['날짜'], df['남긴 음식량(공기)'], marker='o')
ax.set_ylabel("공기 수 (음식량)")
ax.set_title("📉 나의 음식물 쓰레기 줄이기 실천 그래프")
plt.xticks(rotation=45)

st.pyplot(fig)
