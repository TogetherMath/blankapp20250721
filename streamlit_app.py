import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 한글 폰트 설정 (matplotlib용)
plt.rcParams['font.family'] = 'Malgun Gothic'
 
# 데이터 정의
data = {
    "이름": ["홍길동", "김영희", "이철수", "박민수", "최지은"],
    "수학": [85, 90, 70, 95, 60],
    "영어": [78, 88, 65, 92, 72],
    "과학": [92, 84, 75, 89, 68]
}

df = pd.DataFrame(data)

# 제목
st.title("학생 성적 시각화")

# 표 보여주기
st.subheader("📋 성적 데이터")
st.dataframe(df)

# 과목별 평균 점수 막대그래프
st.subheader("📊 과목별 평균 점수")

mean_scores = df[["수학", "영어", "과학"]].mean()
fig, ax = plt.subplots()
ax.bar(mean_scores.index, mean_scores.values, color=["skyblue", "lightgreen", "salmon"])
ax.set_ylabel("점수")
ax.set_title("과목별 평균 점수")

st.pyplot(fig)