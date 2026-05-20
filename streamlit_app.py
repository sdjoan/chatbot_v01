import streamlit as st
from openai import OpenAI

# -----------------------------
# 페이지 설정
# -----------------------------
st.set_page_config(
    page_title="AI 건강 코치",
    page_icon="💪",
    layout="centered"
)

# -----------------------------
# 제목
# -----------------------------
st.title("💪 AI 건강 코치")
st.caption("생활 습관 · 운동 · 식습관 · 건강 관리 도우미")

# -----------------------------
# API Key 입력
# -----------------------------
api_key = st.text_input(
    "OpenAI API Key",
    type="password"
)

if not api_key:
    st.info("OpenAI API Key를 입력해주세요.")
    st.stop()

# -----------------------------
# OpenAI Client
# -----------------------------
client = OpenAI(api_key=api_key)

# -----------------------------
# 시스템 프롬프트
# -----------------------------
SYSTEM_PROMPT = """
당신은 친절한 AI 건강 코치입니다.

역할:
- 생활 습관 개선 안내
- 쉬운 운동 추천
- 건강한 식습관 조언
- 수면 및 스트레스 관리 도움
- 초보자도 이해하기 쉽게 설명

규칙:
- 의료 진단 금지
- 약 처방 금지
- 위험 증상은 병원 상담 권고
- 긍정적이고 따뜻한 말투 사용
- 실천 가능한 작은 습관 위주로 안내
- 답변은 짧고 이해하기 쉽게 작성

답변 스타일:
- 핵심 먼저 설명
- 리스트 형태 적극 사용
- 하루 실천 팁 제공
"""

# -----------------------------
# 세션 상태 초기화
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------------
# 추천 질문 버튼
# -----------------------------
st.subheader("추천 질문")

col1, col2 = st.columns(2)

with col1:
    if st.button("🥗 건강한 식단 추천"):
        st.session_state.example = "건강한 식단 추천해줘"

    if st.button("😴 숙면 습관 알려줘"):
        st.session_state.example = "잠 잘 자는 습관 알려줘"

with col2:
    if st.button("🏃 초보 운동 추천"):
        st.session_state.example = "운동 초보가 시작하기 좋은 운동 추천해줘"

    if st.button("💧 물 얼마나 마셔야 해?"):
        st.session_state.example = "하루 물 섭취량 알려줘"

# -----------------------------
# 이전 채팅 출력
# -----------------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -----------------------------
# 사용자 입력
# -----------------------------
default_prompt = st.session_state.get("example", "")

prompt = st.chat_input(
    "건강 관련 질문을 입력하세요"
)

if default_prompt and not prompt:
    prompt = default_prompt
    st.session_state.example = ""

# -----------------------------
# 응급 키워드 감지
# -----------------------------
EMERGENCY_KEYWORDS = [
    "가슴 통증",
    "호흡곤란",
    "실신",
    "심한 출혈",
    "의식 잃음"
]

if prompt and any(word in prompt for word in EMERGENCY_KEYWORDS):
    st.error(
        "응급 가능성이 있습니다. 가까운 응급실 또는 119에 연락하세요."
    )

# -----------------------------
# 채팅 처리
# -----------------------------
if prompt:

    # 사용자 메시지 저장
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    # 사용자 메시지 출력
    with st.chat_message("user"):
        st.markdown(prompt)

    # 시스템 프롬프트 포함
    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ] + st.session_state.messages

    # AI 응답
    with st.chat_message("assistant"):

        placeholder = st.empty()
        full_response = ""

        stream = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=messages,
            stream=True
        )

        for chunk in stream:
            delta = chunk.choices[0].delta.content

            if delta:
                full_response += delta
                placeholder.markdown(full_response + "▌")

        placeholder.markdown(full_response)

    # 응답 저장
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": full_response
        }
    )

# -----------------------------
# 사이드바
# -----------------------------
with st.sidebar:

    st.header("📌 건강 습관 TIP")

    st.markdown("""
    - 하루 30분 걷기
    - 물 충분히 마시기
    - 늦은 야식 줄이기
    - 규칙적인 수면
    - 스트레칭 자주 하기
    """)

    if st.button("대화 초기화"):
        st.session_state.messages = []
        st.rerun()
