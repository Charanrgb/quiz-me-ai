import streamlit as st

def landing_page():
    # Hero Section
    st.markdown("""
        <div class="hero-section">
            <h1 class="main-title">🎓 Quiz Me AI</h1>
            <div class="hero-content">
                <p class="hero-subtitle">Elevate Your Learning Journey</p>
                <p class="hero-description">Transform your study experience with AI-powered interactive quizzes</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # AI-Powered Feature
    st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🤖</div>
            <h3>AI-Powered</h3>
            <p>Enter topic and Answer questions!</p>
        </div>
    """, unsafe_allow_html=True)

    # Track Progress Feature
    st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📊</div>
            <h3>Random questions everytime!</h3>
            <p>No 2 Quizzes are the same!</p>
        </div>
    """, unsafe_allow_html=True)

    # Unlimited Practice Feature
    st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🔄</div>
            <h3>Unlimited Practice</h3>
            <p>Generate new quizzes anytime you want</p>
        </div>
    """, unsafe_allow_html=True)

    # CTA Section
    st.markdown("""
        <div class="cta-section">
            <h2>Ready to Start Learning?</h2>
        </div>
    """, unsafe_allow_html=True)

    # Center the button using columns
    col1, col2, col3 = st.columns([1,1,1])
    with col2:
        if st.button("Start Quiz Now"):
            st.session_state.page = "home"
            st.experimental_rerun()

    # Footer
    st.markdown("""
        <div class="footer">
            Created by Sai Charan
        </div>
    """, unsafe_allow_html=True)
