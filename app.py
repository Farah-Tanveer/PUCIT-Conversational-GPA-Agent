import streamlit as st
from langchain.messages import HumanMessage, AIMessage

from agent import agent


st.set_page_config(
    page_title="PUCIT GPA Assistant",
    page_icon="🎓"
)

st.title("🎓 PUCIT GPA & CGPA Assistant")
st.write("Ask me about GPA, CGPA, grades, or your semester courses.")


# Start empty conversation
if "messages" not in st.session_state:
    st.session_state.messages = []


# Clear chat button
if st.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()


# Display previous conversation
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.write(message["content"])


# Get new user message
user_input = st.chat_input("Type your question here...")


if user_input:

    # Save user's message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    # Display user's message
    with st.chat_message("user"):
        st.write(user_input)


    # Convert Streamlit history into LangChain messages
    agent_messages = []

    for message in st.session_state.messages:

        if message["role"] == "user":
            agent_messages.append(
                HumanMessage(content=message["content"])
            )

        elif message["role"] == "assistant":
            agent_messages.append(
                AIMessage(content=message["content"])
            )


    # Send conversation to agent
    result = agent.invoke({
        "messages": agent_messages
    })


    # Get final assistant response
    assistant_response = result["messages"][-1].content


    # Save assistant response
    st.session_state.messages.append({
        "role": "assistant",
        "content": assistant_response
    })


    # Display assistant response
    with st.chat_message("assistant"):
        st.write(assistant_response)