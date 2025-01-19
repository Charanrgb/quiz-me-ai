import openai
import streamlit as st

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Function to generate questions
def generate_questions(topic, difficulty, num_questions):
    prompt = f"Generate {num_questions} multiple-choice questions about {topic} at a {difficulty} level. Provide each question in the format: Question;Choice1;Choice2;Choice3;Choice4;CorrectAnswer"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "You are a helpful quiz generator."},
                  {"role": "user", "content": prompt}],
        max_tokens=1000,
        temperature=0.7
    )
    response_text = response['choices'][0]['message']['content'].strip()
    questions = response_text.split("\n")
    return questions

# Load custom CSS
def load_css(css_file):
    with open(css_file) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Initialize session state
if 'questions' not in st.session_state:
    st.session_state.questions = []
    st.session_state.choices = []
    st.session_state.correct_answers = []
    st.session_state.user_answers = []
    st.session_state.submitted = False
    st.session_state.page = "home"  # Add a page state

# Load CSS
load_css("style.css")

# Render the app based on the current page state
if st.session_state.page == "home":
    # Home Page: Input Form
    st.title("Quiz Me AI")
    # User input
    topic = st.text_input("Enter the topic:")
    difficulty = st.selectbox("Select difficulty level:", ["easy", "medium", "hard"])
    num_questions = st.number_input("Number of questions:", min_value=1, max_value=20, value=5)

    if st.button("Generate Questions"):
        if topic:
            with st.spinner("Generating questions..."):
                raw_questions = generate_questions(topic, difficulty, num_questions)
                st.session_state.questions.clear()
                st.session_state.choices.clear()
                st.session_state.correct_answers.clear()
                st.session_state.user_answers.clear()
                st.session_state.submitted = False

                for question in raw_questions:
                    question_parts = question.split(";")
                    if len(question_parts) == 6:
                        st.session_state.questions.append(question_parts[0])
                        st.session_state.choices.append(question_parts[1:5])
                        st.session_state.correct_answers.append(question_parts[5])
                        st.session_state.user_answers.append(None)

                # Navigate to questions page
                st.session_state.page = "questions"
                st.experimental_rerun()
        else:
            st.error("Please enter a topic to generate questions.")

elif st.session_state.page == "questions":
    # Questions Page
    st.title("Quiz Questions")
    for idx, question_text in enumerate(st.session_state.questions):
        choices = st.session_state.choices[idx]
        st.session_state.user_answers[idx] = st.radio(
            f"Q{idx + 1}: {question_text}",
            choices,
            key=f"question_{idx}"
        )

    # Submit button to calculate and display results
    if st.button("Submit"):
        st.session_state.submitted = True
        score = 0
        for idx in range(len(st.session_state.questions)):
            if st.session_state.user_answers[idx] == st.session_state.correct_answers[idx]:
                score += 1
        st.success(f"Your score: {score}/{len(st.session_state.questions)}")

    # Now, show the "Return to Home" button only after submission
    if st.session_state.submitted:
        if st.button("Return to Home"):
            # Reset the session state when going back to the home page
            st.session_state.questions = []
            st.session_state.choices = []
            st.session_state.correct_answers = []
            st.session_state.user_answers = []
            st.session_state.submitted = False
            st.session_state.page = "home"
            st.experimental_rerun()  # This ensures the page reloads to "home"

st.markdown("""
    <div class="footer">
        Created by Sai Charan
    </div>
""", unsafe_allow_html=True)
