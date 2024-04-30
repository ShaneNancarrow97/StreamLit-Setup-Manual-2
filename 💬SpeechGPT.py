import ollama
import streamlit as st
from utilities.icon import page_icon
import time

# Define Stream Data
def stream_data(text,delay:float=0.02):
    for word in text.split():
        yield word + " "
        time.sleep(delay)

# Set Page Config
st.set_page_config(
    page_title="SpeechGPT",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded", 
)

def extract_model_names(models_info: list) -> tuple:
    return tuple(model["name"] for model in models_info["models"])

st.image("https://asset.brandfetch.io/idW9qdsCe9/idplAtYV0V.png")
col1, col2 = st.columns(2)
with col1:
    st.header("SpeechGPT", divider="orange", anchor=False)

    #models_info = ollama.list()
    #available_models = extract_model_names(models_info)
    #if available_models:
        selected_model = "llama3"
       #selected_model = st.selectbox(
            #"Select LLM Model", available_models)
    #else:
        #st.warning("You have not pulled any model from Ollama yet!", icon="⚠️")
        #if st.button("Go to settings to download a model"):
            #st.page_switch("pages/03_⚙️_Settings.py")
    #st.subheader(selected_model)
with col2:
    st.markdown("## What is SpeechGPT?\n"
            "SpeechGPT is a Large Language Model (LLM) custom instructed on-top of Llama3 8B. With this UI you can:\n"
            "* Prompt the SpeechGPT to return context.\n"
            "```python\n"
            "E.G. SpeechGPT Prompt = 'How do I build a category around Fraud?'\n"
            "```\n"
            "##### Link to [CallMiner Analyze](https://vanquisbank.callminer.net) | [CallMiner API](https://gwapiuk.callminer.net)")


message_container = st.container(height=350, border=True)

if "messages" not in st.session_state:
        st.session_state.messages = []

for message in st.session_state.messages:
        avatar = "🤖" if message["role"] == "assistant" else "😎"
        with message_container.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

if user_prompt := st.chat_input("Enter your prompt here..."):
        try:
            st.session_state.messages.append(
                {"role": "user", "content": user_prompt})

            message_container.chat_message("user", avatar="😎").markdown(user_prompt)

            with message_container.chat_message("assistant", avatar="🤖"):
                with st.spinner("SpeechGPT working..."):
                    stream = ollama.chat(model=selected_model,messages=[{
            "role":"user",
            "content":user_prompt,
        }])
                    
                # stream response
                response = stream["message"]["content"]
                st.write_stream(stream_data(response))
            st.session_state.messages.append(
                {"role": "assistant", "content": response})

        except Exception as e:
            st.error(e, icon="⛔️")

            # streamlit run 💬SpeechGPT.py
