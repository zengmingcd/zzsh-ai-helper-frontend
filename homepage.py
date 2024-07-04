import streamlit as st
from resources import enum_list as el, i18n
from utils import request4answer as r4a

st.set_page_config(page_title="AI-Assistant")

language = st.sidebar.selectbox(
    "Language",
    el.LANGUAGE_LIST
)

st.title(i18n.TITLE.get(language))
st.info(i18n.INFO.get("0").get(language))
st.info(i18n.INFO.get("1").get(language))

# init
if "session" not in st.session_state:
    st.session_state.session = r4a.initSession(st.secrets.authorize_key.key)
    st.session_state.session_count = 0

# construct sidebar
st.sidebar.markdown(i18n.SIDEBAR_TITLE.get(language))
country = st.sidebar.selectbox(
    i18n.COUNTRY.get(language),
    el.COUNTRY_LIST
)
region = st.sidebar.selectbox(
    i18n.REGION.get(language),
    el.REGION_LIST.get(country) if el.REGION_LIST.get(country) else (i18n.COMING_SOON.get(language),)
)

source = st.sidebar.selectbox(
    i18n.ACT_RESOURCES_LIST.get(language),
    el.ACT_SOURCES_LIST.get(region) if el.ACT_SOURCES_LIST.get(region) else (i18n.COMING_SOON.get(language),)
)


# construct main
greeting = i18n.GREETING.get(language)
with st.chat_message("assistant"):
    st.markdown(greeting)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if st.session_state.session_count < el.MAX_CONVERSATION_COUNT:
    if prompt := st.chat_input(i18n.INPUT_PROMPT.get(language)):
        st.session_state.messages.append({"role":"user", "content":prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            response = r4a.requestAIHelper(prompt, st.session_state.session)
            st.markdown(response)

        st.session_state.messages.append({"role":"assistant", "content":response}) 
        st.session_state.session_count = st.session_state.session_count + 1
else:
    with st.chat_message("ai"):
        st.markdown(i18n.SESSION_LIMIT.get(language))