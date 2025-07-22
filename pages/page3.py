import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os

# ✅ 사용자 지정 한글 폰트 경로 설정
font_path = '/workspaces/blankapp20250721/fonts/나눔 글꼴/나눔고딕/NanumFontSetup_TTF_GOTHIC/NanumGothic.ttf'

# ✅ 폰트 등록 및 설정
if os.path.exists(font_path):
    font_prop = fm.FontProperties(fname=font_path)
    plt.rcParams['font.family'] = font_prop.get_name()
    plt.rcParams['axes.unicode_minus'] = False  # 마이너스 깨짐 방지
else:
    print("❌ 한글 폰트 파일을 찾을 수 없습니다.")






st.title("🔄 일차변환 시각화")

st.markdown("도형의 꼭짓점 좌표와 변환 행렬을 입력해 보세요.")



# 1. 도형 입력 (삼각형)
st.subheader("도형 입력")
A = np.array(st.text_input("점 A 좌표 (예: 1,1)", "1,1").split(','), dtype=float)
B = np.array(st.text_input("점 B 좌표 (예: 1,2)", "1,2").split(','), dtype=float)
C = np.array(st.text_input("점 C 좌표 (예: 2,1)", "2,1").split(','), dtype=float)
shape = np.array([A, B, C, A])  # 삼각형 폐곡선




# 2. 행렬 입력
st.subheader("2×2 변환 행렬 입력")

a11 = st.number_input("a11", value=1, step=1, format="%d")  # 🔹 default = 1
a12 = st.number_input("a12", value=2, step=1, format="%d")  # 🔹 default = 2
a21 = st.number_input("a21", value=3, step=1, format="%d")  # 🔹 default = 3
a22 = st.number_input("a22", value=4, step=1, format="%d")  # 🔹 default = 4

matrix = np.array([[a11, a12], [a21, a22]])




# 3. 변환 적용
transformed = np.dot(shape, matrix.T)




# 4. 시각화
fig, ax = plt.subplots(figsize=(2.5, 2.5))  # 적당한 크기 유지

# 도형 그리기
ax.plot(shape[:,0], shape[:,1], 'b-', label='원래 도형')
ax.plot(transformed[:,0], transformed[:,1], 'r--', label='변환된 도형')

# 자동 축 범위
all_x = np.concatenate([
    shape[:,0], transformed[:,0], [-1, 1]  # x 기준점 추가
])
all_y = np.concatenate([
    shape[:,1], transformed[:,1], [-1, 1]  # y 기준점 추가
])

margin = 0.5
ax.set_xlim(np.min(all_x) - margin, np.max(all_x) + margin)
ax.set_ylim(np.min(all_y) - margin, np.max(all_y) + margin)



# 그래프 스타일
ax.set_aspect('equal')
ax.grid(True)

# 좌표축 추가
ax.axhline(0, color='gray', linewidth=1)  # x축
ax.axvline(0, color='gray', linewidth=1)  # y축

# 원점 표시
ax.plot(0, 0, 'ko')  # 원점 점으로 찍기
ax.text(0.1, 0.1, '원점', fontsize=8, fontproperties=font_prop)  # 원점 라벨


# ✅ 범례 (폰트 적용 여부 확인 후 처리)
if font_prop:
    ax.legend(
        loc='upper left',
        bbox_to_anchor=(1.05, 1.0),
        fontsize='small',
        frameon=True,
        prop=font_prop
    )
else:
    ax.legend(
        loc='upper left',
        bbox_to_anchor=(1.05, 1.0),
        fontsize='small',
        frameon=True
    )

plt.tight_layout(pad=0.3)
st.pyplot(fig, use_container_width=False)





# 5. 수식 출력
st.latex(rf"""
\text{{입력된 행렬}} = 
\begin{{bmatrix}}
{a11} & {a12} \\
{a21} & {a22}
\end{{bmatrix}}
""")
