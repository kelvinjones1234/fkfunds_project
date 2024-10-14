import streamlit as st
import os
from chat import load_environment_variables, query_and_respond

# Load environment variables
load_environment_variables()

# Set up paths
current_dir = os.path.dirname(os.path.abspath(__file__))
persist_dir = os.path.join(current_dir, 'chroma_db')

# Custom CSS for styling (unchanged)
st.markdown("""
<style>
    .question {
        background-color: #3A506B;
        color: white;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 10px;
        border-left: 5px solid white;
        font-family: 'Helvetica Neue', sans-serif;
        font-size: 16px;
    }
    .answer {
        background-color: #F5F5F5;
        color: #333;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 20px;
        border-left: 5px solid #3A506B;
        font-family: 'Helvetica Neue', sans-serif;
        font-size: 16px;
    }
    .stApp {
        margin: 0 auto;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for conversation history
if 'conversation' not in st.session_state:
    st.session_state.conversation = []

# Sidebar content (unchanged)
st.sidebar.title("About the System")
justified_text = """
<div style='text-align: justify; padding-bottom: 1rem'>
This platform is designed to help students easily navigate school processes and access the information they need. Whether you're looking for guidance on course registration, need help with fee payments, or have questions about campus services, we're here to assist you every step of the way. Explore the features and get the support you need to make your academic journey smoother and more efficient.
</div>
"""
st.sidebar.markdown(justified_text, unsafe_allow_html=True)

school_map_url = "https://earth.google.com/web/search/Federal+Polytechnic+Bida,+Doko+Road,+Bida/@9.04122326,6.00630994,165.69800678a,381.85097263d,35y,0.00016688h,0t,0r/data=CigiJgokCQiipm-VGyJAEW2avhRfESJAGZJsQWdbIRhAITY8dt2v8hdAOgMKATA"
button_html = f"""
<div style="display: flex;">
    <a href="{school_map_url}" target="_blank" style="
    background-color: #4CAF50;
    color: white;
    padding: 10px 20px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    margin-bottom: .5rem;
    border-radius: 4px;
    font-size: 16px;
    margin-top: 10px;
    ">Explore the School Map</a>
</div>
"""
st.sidebar.markdown(button_html, unsafe_allow_html=True)
st.sidebar.write("We can also help you with detailed descriptions to enhance your map experience.")

# Main Section
st.title("Welcome to the Federal Polytechnic Consultation and Navigation System")

st.subheader("Frequently Asked Questions:")
faqs = [
    "What is the cut-off mark for admission?",
    "How do I apply for admission?",
    "What documents are required for admission?"
]

# Create clickable buttons for FAQs
for faq in faqs:
    if st.button(faq):
        # Use query_and_respond function from chat.py
        response = query_and_respond(persist_dir, faq)
        
        # Add to conversation history
        st.session_state.conversation.append({
            "question": faq,
            "answer": response
        })
        
        # Force a rerun to update the conversation display
        st.rerun()

# Input field for custom questions
question = st.chat_input("Type your question here")

# Handling the submit action for custom questions
if question:
    response = query_and_respond(persist_dir, question)
    
    # Add to conversation history
    st.session_state.conversation.append({
        "question": question,
        "answer": response
    })
    
    # Clear the input field by rerunning the app
    st.rerun()

# Display conversation history
for item in st.session_state.conversation:
    st.markdown(f'<div class="question"><strong>Q:</strong> {item["question"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="answer"><strong>A:</strong> {item["answer"]}</div>', unsafe_allow_html=True)

# Adding space at the bottom
st.markdown("<br>", unsafe_allow_html=True)