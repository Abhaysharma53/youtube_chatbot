import streamlit as st
from youtube_transcript_api import TranscriptsDisabled, YouTubeTranscriptApi
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda, RunnablePassthrough, RunnableParallel
from dotenv import load_dotenv

load_dotenv()
ytt_api = YouTubeTranscriptApi()
st.set_page_config(page_title= 'YouTube Chatbot')
st.title('Youtube Chatbot App')
st.sidebar.header("YouTube Video")
video_id = st.sidebar.text_input("Enter the youtube video id to get started")
with st.chat_message("assistant"):
    st.write("Hello Aliens!")
    st.write("I am your assistant who will help you chat with your youtube video")



if video_id:
    active_state = True
    raw_transcript = ytt_api.get_transcript(video_id, languages= ['en', 'hi'])
    transcript = " ".join(chunk['text'] for chunk in raw_transcript)


query = st.chat_input("Ask your question", disabled= not bool(video_id))
if query:
    #st.write(f'User has sent the following query {query}')
    with st.chat_message("assistant"):
        st.write(transcript)
else:
# Disable chat input
    st.info("Please enter a YouTube video ID in the sidebar to start chatting.", icon = "🚨")

