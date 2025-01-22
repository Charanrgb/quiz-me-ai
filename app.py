import openai
import streamlit as st
import os
import homepage

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Function to generate questions
if 'page' not in st.session_state:
    st.session_state.page = "landing"

def generate_questions(topic, difficulty, num_questions):
    prompt = f"Generate exactly {num_questions} multiple-choice questions about {topic} at a {difficulty} level. Provide each question in this exact format: Question;Choice1;Choice2;Choice3;Choice4;CorrectAnswer"
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
    st.session_state.page = "landing"
    
# Load CSS
load_css("style.css")

if(st.session_state.page == "landing"):
    homepage.landing_page()

# Render the app based on the current page state
elif st.session_state.page == "home":
    # Home Page: Input Form
    if(st.button("About")):
        st.session_state.page = "landing"
        st.experimental_rerun()
    st.title("🎓Quiz Me AI")
    # User input
    topic = st.text_input("Enter the topic:")
    difficulty = st.selectbox("Select difficulty level:", ["easy", "medium", "hard"])
    num_questions = st.slider(
        label="How many questions would you like in your quiz?",
        min_value=1,
        max_value=20,
        value=5,
        step=1
    )
    if st.button("Generate Questions"):
        if topic:
            with st.spinner("Generating questions..."):
                raw_questions = generate_questions(topic, difficulty, num_questions)
                st.session_state.questions.clear()
                st.session_state.choices.clear()
                st.session_state.correct_answers.clear()
                st.session_state.user_answers.clear()
                st.session_state.submitted = False

                questions_generated = False  # Track if valid questions are generated

                for question in raw_questions:
                    question_parts = question.split(";")
                    if len(question_parts) == 6:
                        st.session_state.questions.append(question_parts[0])
                        st.session_state.choices.append(question_parts[1:5])
                        st.session_state.correct_answers.append(question_parts[5])
                        st.session_state.user_answers.append(None)
                        questions_generated = True
                    else:
                        st.error("Invalid question format. Please try again.")
                        break
            
            # Navigate to questions page only if questions were generated
            if questions_generated:
                st.session_state.page = "questions"
                st.experimental_rerun()
            else:
                st.error("Failed to generate questions. Please try again with valid inputs.")
    else:
        st.error("Please enter a topic to generate questions.")


# Questions Page
elif st.session_state.page == "questions":
    st.title("Quiz Questions")
    wrong = []

    for idx, question_text in enumerate(st.session_state.questions):
        choices = st.session_state.choices[idx]

    # Display the question
    st.write(f"Q{idx + 1}: {question_text}")

    # Check if submitted to disable further input
    if st.session_state.submitted:
        st.radio(
            label="",
            options=choices,
            index=choices.index(st.session_state.user_answers[idx]) if st.session_state.user_answers[idx] else 0,
            key=f"question_{idx}_choice",
            disabled=True
        )
    else:
        st.session_state.user_answers[idx] = st.radio(
            label="",
            options=choices,
            index=0,
            key=f"question_{idx}_choice",
            disabled=False
        )

    # Submit button to calculate and display results
    if not st.session_state.submitted and st.button("Submit"):
        st.session_state.submitted = True
        score = 0
        for idx in range(len(st.session_state.questions)):
            if (
                st.session_state.user_answers[idx] 
                and st.session_state.user_answers[idx].strip().lower() == st.session_state.correct_answers[idx].strip().lower()
            ):
                score += 1
            else:
                wrong.append(f"Q{idx + 1}")  # Store the question number (1-based index)
        st.success(f"Your score: {score}/{len(st.session_state.questions)}")
        if len(wrong) != 0:
            st.write("You got the following questions wrong: ", ", ".join(wrong))
        else:
            st.write("Congratulations! You got all the questions right!")

    # Return to Home Button
    if st.session_state.submitted and st.button("Return to Home"):
        # Reset the session state when going back to the home page
        st.session_state.questions = []
        st.session_state.choices = []
        st.session_state.correct_answers = []
        st.session_state.user_answers = []
        st.session_state.submitted = False
        st.session_state.page = "home"
        st.experimental_rerun()  # Reload to "home"



st.markdown("""
    <div class="footer">
        Created by Sai Charan
    </div>
""", unsafe_allow_html=True)
