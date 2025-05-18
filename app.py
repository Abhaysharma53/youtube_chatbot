import streamlit as st
from youtube_transcript_api import TranscriptsDisabled, YouTubeTranscriptApi, NoTranscriptFound, VideoUnavailable
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda, RunnablePassthrough, RunnableParallel
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS

load_dotenv()
ytt_api = YouTubeTranscriptApi()
parser = StrOutputParser()
splitter = RecursiveCharacterTextSplitter(chunk_size = 1000, chunk_overlap = 150)
embedding_model= OpenAIEmbeddings(model= 'text-embedding-3-small')
llm = ChatOpenAI(temperature= 0.25)
def format_documents(retrieved_docs):
    context_text = "\n\n".join(docs.page_content for docs in retrieved_docs)
    return context_text

prompt = PromptTemplate(template = """You are a helpful assistant, who helps to give the answer about youtube video based upon the context received under your best capacity
                        if you think the question asked by the user has not any relation with the youtube video, just say you dont have enough context to answer this question
                        
                        {context}
                        Question: {query}""",
                        input_variables= ['context', 'query'])

st.set_page_config(page_title= 'YouTube Chatbot')
st.title('Youtube Chatbot App')
st.sidebar.header("YouTube Video")
video_id = st.sidebar.text_input("Enter the youtube video id to get started")
with st.chat_message("assistant"):
    st.write("Hello Aliens!")
    st.write("I am your assistant who will help you chat with your youtube video")



if video_id:
    #active_state = True
    try:
        raw_transcript = ytt_api.get_transcript(video_id, languages= ['en', 'hi'])
    except TranscriptsDisabled:
        st.exception('❌ Transcripts are disabled for this video.')
    except NoTranscriptFound:
        st.exception('❌ No transcript found in the requested languages.')
    except VideoUnavailable:
        st.exception("❌ The video is unavailable.")
    except Exception as e:
        st.exception('Some Unexpected error occured. please try again!')
    transcript = " ".join(chunk['text'] for chunk in raw_transcript)
    chunks = splitter.create_documents([transcript])
    vector_store = FAISS.from_documents(chunks, embedding_model)

query = st.chat_input("Ask your question", disabled= not bool(video_id))
if query:
    #st.write(f'User has sent the following query {query}')
    # with st.chat_message("assistant"):
    #     st.write(transcript)
        #st.write(len(chunks))   #chunks are getting created
    with st.chat_message("user"):
        st.write(query)
    retriever = vector_store.as_retriever(search_type = 'similarity', search_kwargs = {"k": 5})
    retrieved_docs = retriever.invoke(query)
    #st.write(retrieved_docs)
    parallel_chain = RunnableParallel({
        'context': retriever | RunnableLambda(format_documents),
        'query': RunnablePassthrough()
    }
    )
    main_chain = parallel_chain | prompt | llm | parser
    with st.chat_message("assistant"):
        st.write(main_chain.invoke(query))

else:
# Disable chat input
    st.info("Please enter a YouTube video ID in the sidebar to start chatting.", icon = "🚨")

