import streamlit as st
from openai import OpenAI
import datetime

st.set_page_config(page_title="Mentostudy - המנטור שלך ללמידה", layout="wide")

# עיצוב RTL
st.markdown(
    "<style>body {direction: rtl; text-align: right;} .stTextInput>div>div>input {text-align: right;} .stTextArea textarea {text-align: right;}</style>",
    unsafe_allow_html=True
)

# API Key
api_key = st.sidebar.text_input("🔑 הזן את OpenAI API Key שלך", type="password")
if api_key:
    client = OpenAI(api_key=api_key)

st.title("Mentostudy 🧠")
st.write("המנטור החכם שלך ללמידה מותאמת אישית")

if "stage" not in st.session_state:
    st.session_state.stage = 1

# שלב 1: אפיון
if st.session_state.stage == 1:
    st.header("שלב 1: אפיון הלומד")
    with st.form("user_profile"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("שם פרטי")
            age = st.number_input("גיל", min_value=5, max_value=120, step=1)
            gender = st.selectbox("לשון פנייה מועדפת", ["זכר", "נקבה", "אחר"])
            background = st.selectbox("רקע לימודי", ["תלמיד חטיבה", "תלמיד תיכון", "סטודנט", "מבוגר לומד", "אחר"])
            knowledge = st.slider("עד כמה יש לך ידע קודם בתחום?", 1, 5)
        with col2:
            subject = st.text_input("תחום הלמידה")
            goal = st.selectbox("מטרת הלמידה", ["למידה חופשית", "פיתוח סקרנות", "הצלחה בבחינת בגרות", "אחר"])
            goal_text = st.text_input("פירוט המטרה (רשות)")
            deadline = st.date_input("תאריך יעד", value=datetime.date.today())
            source_link = st.text_input("קישור למקור ידע (רשות)")
            uploaded_file = st.file_uploader("העלה קובץ טקסט / PDF", type=["txt", "pdf"])
        personal_note = st.text_area("משהו אישי שחשוב שנדע")
        submitted = st.form_submit_button("המשך לשלב הבא")
        if submitted:
            st.session_state.profile = {
                "name": name, "age": age, "gender": gender, "background": background,
                "knowledge": knowledge, "subject": subject, "goal": goal,
                "goal_text": goal_text, "deadline": str(deadline),
                "source_link": source_link, "personal_note": personal_note
            }
            st.session_state.stage = 2
