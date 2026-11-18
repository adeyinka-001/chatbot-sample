
import os
import streamlit as st
from openai import OpenAI

st.set_page_config(
    page_title="ABC Store AI Assistant",
    page_icon="🤖",
    layout="centered"
)

# Connect to OpenAI using the environment variable
api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    st.error("OPENAI_API_KEY is missing. Configure it in Colab before launching the app.")
    st.stop()

client = OpenAI(api_key=api_key)

# ABC Store workshop knowledge
policy = """
You work for ABC Store.
Returns are accepted within 30 days.
Shipping takes 3-5 business days.
Customer support is available Monday-Friday.
"""

orders = {
    "1234": "Shipped",
    "5678": "Processing",
    "9999": "Delivered"
}

instructions = f"""
You are a professional customer support agent working for ABC Store.

BUSINESS POLICY:
{policy}

ORDER DATABASE:
{orders}

Rules:
1. Answer using only the supplied business policy and order database.
2. Check order numbers against the supplied database.
3. If an order number does not exist, say you cannot find it.
4. If information is unavailable, say you do not know based on the available information.
5. Never invent policies, delivery dates, order statuses, or other information.
6. Be friendly, professional, and concise.
"""

st.title("🤖 ABC Store AI Assistant")
st.write("Welcome to ABC Store! How can I help you today?")

with st.sidebar:
    st.title("ABC Store")
    st.write("Customer Support Assistant")
    st.divider()
    st.subheader("Available Services")
    st.write("📦 Order Tracking")
    st.write("🚚 Shipping Information")
    st.write("🔄 Returns Policy")
    st.write("☎️ Customer Support")
    st.divider()
    st.info("Customer support is available Monday-Friday.")
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display existing conversation
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

question = st.chat_input("Ask ABC Store a question...")

if question:
    st.session_state.messages.append(
        {"role": "user", "content": question}
    )

    with st.chat_message("user"):
        st.markdown(question)

    # Send the conversation so the model can use chat context
    conversation = [
        {"role": item["role"], "content": item["content"]}
        for item in st.session_state.messages
    ]

    with st.chat_message("assistant"):
        with st.spinner("ABC Store AI is thinking..."):
            try:
                response = client.responses.create(
                    model="gpt-4.1-mini",
                    instructions=instructions,
                    input=conversation
                )
                answer = response.output_text
            except Exception as error:
                answer = f"Sorry, an API error occurred: {error}"

        st.markdown(answer)

    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )
