import streamlit as st
from openai import OpenAI

# -----------------------------------
# 페이지 설정
# -----------------------------------
st.set_page_config(
    page_title="MBTI 성격 챗봇",
    page_icon="🧠",
    layout="centered"
)

# -----------------------------------
# 제목
# -----------------------------------
st.title("🧠 MBTI 성격 챗봇")

st.write(
    """
MBTI 성격 유형에 대해 알려주는 AI 챗봇입니다 😊

✔ MBTI 특징  
✔ 연애 스타일  
✔ 직업 추천  
✔ 인간관계 성향  
✔ 장점과 단점  

등을 쉽게 알려드립니다.
"""
)

# -----------------------------------
# OpenAI API Key 입력
# -----------------------------------
openai_api_key = st.text_input(
    "OpenAI API Key",
    type="password"
)

if not openai_api_key:
    st.info("OpenAI API Key를 입력해주세요.", icon="🗝️")
    st.stop()

# -----------------------------------
# OpenAI Client
# -----------------------------------
client = OpenAI(api_key=openai_api_key)

# -----------------------------------
# 시스템 프롬프트
# -----------------------------------
SYSTEM_PROMPT = """
당신은 친절한 MBTI 성격 분석 전문가입니다.

역할:
- MBTI 유형 설명
- 성격 특징 안내
- 연애 스타일 설명
- 인간관계 특징 설명
- 직업 추천
- 장점/단점 분석

규칙:
- 쉽고 친절하게 설명
- 긍정적인 말투 사용
- 리스트 형태 적극 활용
- 너무 딱딱하지 않게 작성
- 이모지 사용 가능

답변 스타일:
- 핵심 먼저 설명
- 짧고 보기 쉽게 작성
"""

# -----------------------------------
# 추천 질문
# -----------------------------------
st.subheader("🌱 추천 질문")

col1, col2 = st.columns(2)

with col1:

    if st.button("💙 INFP 특징 알려줘"):
        st.session_state.example = "INFP 특징 알려줘"

    if st.button("🔥 ENTJ 직업 추천"):
        st.session_state.example = "ENTJ에게 잘 맞는 직업 추천해줘"

with col2:

    if st.button("💕 ENFP 연애 스타일"):
        st.session_state.example = "ENFP 연애 스타일 알려줘"

    if st.button("👫 ISTJ와 궁합 좋은 MBTI"):
        st.session_state.example = "ISTJ와 궁합 좋은 MBTI 알려줘"

# -----------------------------------
# 세션 상태 초기화
# -----------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------------------
# 이전 메시지 출력
# -----------------------------------
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -----------------------------------
# 입력창
# -----------------------------------
default_prompt = st.session_state.get("example", "")

prompt = st.chat_input(
    "MBTI 관련 질문을 입력하세요"
)

if default_prompt and not prompt:
    prompt = default_prompt
    st.session_state.example = ""

# -----------------------------------
# 사용자 입력 처리
# -----------------------------------
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

    # 시스템 메시지 포함
    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ] + st.session_state.messages

    # Assistant 응답
    with st.chat_message("assistant"):

        placeholder = st.empty()
        full_response = ""

        stream = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=messages,
            stream=True,
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

# -----------------------------------
# 사이드바
# -----------------------------------
with st.sidebar:

    st.header("🧩 MBTI 유형")

    st.markdown("""
    ### 분석 가능 유형

    - INTJ
    - INTP
    - ENTJ
    - ENTP
    - INFJ
    - INFP
    - ENFJ
    - ENFP
    - ISTJ
    - ISFJ
    - ESTJ
    - ESFJ
    - ISTP
    - ISFP
    - ESTP
    - ESFP
    """)

    st.divider()

    st.markdown("""
    💡 예시 질문

    - ENFP 성격 특징 알려줘
    - ISTJ 장단점 알려줘
    - INFJ 연애 스타일은?
    - ENTP 직업 추천해줘
    """)

    st.divider()

    if st.button("🗑️ 대화 초기화"):
        st.session_state.messages = []
        st.rerun()
