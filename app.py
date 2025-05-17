import streamlit as st

st.set_page_config(page_title= 'YouTube Chatbot')
st.title('Youtube Chatbot App')
st.sidebar.header("YouTube Video")
video_id = st.sidebar.text_input("Enter the youtube video id to get started")
with st.chat_message("assistant"):
    st.write("Hello Aliens!")
    st.write("I am your assistant who will help you chat with your youtube video")



# if video_id:
#     active_state = True

query = st.chat_input("Ask your question", disabled= not bool(video_id))
if query:
    st.write(f'User has sent the following query {query}')
else:
# Disable chat input
    st.info("Please enter a YouTube video ID in the sidebar to start chatting.", icon = "🚨")

