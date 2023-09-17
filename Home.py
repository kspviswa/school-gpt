import streamlit as st
import time
from prompt import LLM_Hander

st.set_page_config(page_title='School GPT',
                   page_icon='🚸',
                   #layout='wide',
                   #initial_sidebar_state="expanded",
                )

if 'trainingCompleted' not in st.session_state:
    st.session_state.trainingCompleted = False

if 'botHandler' not in st.session_state:
    st.session_state.botHandler = None

if 'messages' not in st.session_state:
    st.session_state.messages = []

st.markdown('# :rainbow[School GPT] 🚸', unsafe_allow_html=True)
st.markdown('### :rainbow[A personalized chatbot for teachers] 👩🏻‍🏫 :rainbow[& students] 👨🏻‍🎓')

st.subheader('Build a knowledge base')
flist = st.file_uploader(label='Upload a PDF file to act as a knowledge base',
                 accept_multiple_files=True,
                 type=['pdf'],
                 )

st.markdown("""
    <style>
    .stRadio [role=radiogroup]{
        align-items: center;
        justify-content: center;
        font-size: 32px;
    }
    </style>
""",unsafe_allow_html=True)

if st.session_state.botHandler == None:
    st.session_state.botHandler = LLM_Hander()

if len(flist) > 0:
    st.markdown('## If you are done adding files, click below to train')
    b = st.button('Train 🚀 the school bot 🤖', use_container_width=True, type='primary')
    if b:
        with st.status(label='Crunching the data 🏋🏻‍♀️🏋🏻‍♀️🏋🏻‍♀️🏋🏻‍♀️🏋🏻‍♀️🏋🏻‍♀️', expanded=True):
            st.session_state.botHandler.loadData(flist)
            st.write('📑 Loaded the docs ✅')
            st.write('📇 Created indexes ✅')
            st.write('👩🏻‍🏫 Created teacher bot ✅')            
            st.write('👨🏻‍🎓 Created student bot ✅')
            st.session_state.trainingCompleted = True

if st.session_state.trainingCompleted:
    BotOption = st.radio(
        "Select the Bot",
        ["Teacher Bot", "Student Bot"],
        captions=["Chat bot for teacher assistant tasks",
                  "Q&A bot for answering questions"],
    )
    if BotOption == "Teacher Bot":
        st.markdown('Hi 👋🏻 I am a Teacher bot 🤖')

        for message in st.session_state.messages:
            with st.chat_message(name=message["role"]):
                st.markdown(message["content"])
        
        if prompt := st.chat_input("How may I help you?"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            with st.chat_message(name='assistant'):
                message_placeholder = st.empty()
                full_response = ""
                with st.spinner(text="Thinking... 💭💭💭"):
                    if st.session_state.botHandler != None:
                        raw = st.session_state.botHandler.firePrompt('teacher', st.session_state.messages[-1]['content'])
                        response = str(raw)
                        # Simulate stream of response with milliseconds delay
                        for chunk in response.split():
                            full_response += chunk + " "
                            time.sleep(0.05)
                            # Add a blinking cursor to simulate typing
                            message_placeholder.markdown(full_response + "▌", unsafe_allow_html=True)
                        message_placeholder.markdown(full_response, unsafe_allow_html=True)
                        st.session_state.messages.append({"role": "assistant", "content": full_response})
                    else:
                        message_placeholder.error('Bot not initialized')
    if BotOption == "Student Bot":
        st.markdown('Hi 👋🏻 I am a Student bot 🤖')
        with st.chat_message(name="assistant"):
            st.markdown('Ask a question')
        if prompt := st.chat_input('ask....'):
            m = {"role" : "user", "content" : prompt}
            with st.chat_message("user"):
                st.markdown(prompt)
            with st.chat_message(name='assistant'):
                with st.spinner('Thinking'):
                    if st.session_state.botHandler != None:
                        r = st.session_state.botHandler.firePrompt('student', prompt)
                        st.markdown(str(r))
                    else:
                        st.error('Bot not initialized')


