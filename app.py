import streamlit as st
import requests


# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="AI CV Parser",
    page_icon="📄",
    layout="wide"
)


# ==========================================
# API URL
# ==========================================

API_URL = "https://henchman-ground-elevator.ngrok-free.dev/extract-cv"
# ==========================================
# TITLE
# ==========================================

st.title("📄 AI CV Parser")

st.write(
    "Upload a CV and let the AI extract "
    "structured candidate information."
)


# ==========================================
# FILE UPLOAD
# ==========================================

uploaded_file = st.file_uploader(
    "Upload your CV",
    type=["pdf"]
)


# ==========================================
# PROCESS
# ==========================================

if uploaded_file is not None:

    st.success(
        f"Uploaded: {uploaded_file.name}"
    )

    st.pdf(uploaded_file)

    if st.button(
        "🚀 Analyze CV",
        type="primary"
    ):

        with st.spinner(
            "AI is analyzing your CV..."
        ):

            try:

                response = requests.post(
                    API_URL,
                    files={
                        "file": (
                            uploaded_file.name,
                            uploaded_file.getvalue(),
                            "application/pdf"
                        )
                    },
                    timeout=300
                )

                if response.status_code == 200:

                    result = response.json()

                    st.success(
                        "CV analyzed successfully!"
                    )

                    data = result["data"]

                    # ==================================
                    # BASIC INFORMATION
                    # ==================================

                    st.header("👤 Candidate Information")

                    col1, col2 = st.columns(2)

                    with col1:

                        st.subheader("Full Name")

                        st.write(
                            data.get(
                                "full_name",
                                "Not found"
                            )
                        )

                    with col2:

                        st.subheader("Email")

                        st.write(
                            data.get(
                                "email",
                                "Not found"
                            )
                        )

                    # ==================================
                    # EDUCATION
                    # ==================================

                    st.header("🎓 Education")

                    education = data.get(
                        "education",
                        []
                    )

                    for edu in education:

                        with st.container():

                            st.write(
                                f"**Degree:** "
                                f"{edu.get('degree', '')}"
                            )

                            st.write(
                                f"**Institution:** "
                                f"{edu.get('institution', '')}"
                            )

                            st.write(
                                f"**Year:** "
                                f"{edu.get('year', '')}"
                            )

                            st.divider()

                    # ==================================
                    # SKILLS
                    # ==================================

                    st.header("🛠️ Skills")

                    skills = data.get(
                        "skills",
                        []
                    )

                    cols = st.columns(3)

                    for i, skill in enumerate(skills):

                        with cols[i % 3]:

                            st.success(skill)

                    # ==================================
                    # EXPERIENCE
                    # ==================================

                    st.header("💼 Experience")

                    experience = data.get(
                        "experience",
                        []
                    )

                    for exp in experience:

                        with st.container():

                            st.subheader(
                                exp.get(
                                    "role",
                                    ""
                                )
                            )

                            st.write(
                                f"**Company:** "
                                f"{exp.get('company', '')}"
                            )

                            st.write(
                                f"**Years:** "
                                f"{exp.get('years', '')}"
                            )

                            st.divider()

                    # ==================================
                    # RAW JSON
                    # ==================================

                    with st.expander(
                        "🔍 View Raw JSON"
                    ):

                        st.json(data)

                else:

                    st.error(
                        f"API Error: "
                        f"{response.status_code}"
                    )

                    try:

                        st.json(
                            response.json()
                        )

                    except:

                        st.write(
                            response.text
                        )

            except requests.exceptions.Timeout:

                st.error(
                    "The AI model took too long "
                    "to respond. Please try again."
                )

            except requests.exceptions.ConnectionError:

                st.error(
                    "Could not connect to the API. "
                    "Check that Kaggle and ngrok are running."
                )

            except Exception as e:

                st.error(
                    f"Unexpected error: {str(e)}"
                )