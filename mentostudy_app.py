import streamlit as st
from openai import OpenAI
import datetime

st.set_page_config(page_title="Mentostudy - המנטור שלך ללמידה", layout="wide")

# עיצוב RTL לעברית
st.markdown(
    "<style>body {direction: rtl; text-align: right;} .stTextInput>div>div>input {text-align: right;} .stTextArea textarea {text-align: right;}</style>",
    unsafe_allow_html=True
)

# API key
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
        personal_note = st.text_area("משהו אישי שחשוב שנדע (למשל: אני רוצה ללמד את הבן שלי לכתוב מספרים)")
        submitted = st.form_submit_button("המשך לשלב הבא")
        if submitted:
            st.session_state.profile = {
                "name": name, "age": age, "gender": gender, "background": background,
                "knowledge": knowledge, "subject": subject, "goal": goal,
                "goal_text": goal_text, "deadline": str(deadline),
                "source_link": source_link, "personal_note": personal_note
            }
            st.session_state.stage = 2

# שלב 2: תכנית למידה
if st.session_state.stage == 2:
    st.header("שלב 2: בניית תכנית הלמידה 📚")
    with st.spinner("בונה תכנית מותאמת אישית..."):
        profile = st.session_state.profile
        prompt = f'''
        צור תכנית למידה עבור לומד/ת בגיל {profile["age"]}, רקע: {profile["background"]}, 
        ידע קודם {profile["knowledge"]}/5, תחום הלמידה: {profile["subject"]}.
        מטרה כללית: {profile["goal"]}, פירוט: {profile["goal_text"]}, תאריך יעד: {profile["deadline"]}.
        פרטים חשובים נוספים: {profile["personal_note"]}

        התכנית צריכה להיות מחולקת לשבועות או שלבים, לכלול משימות, טכניקות למידה אפקטיביות, חיזוק עצמאות בלמידה,
        שימוש במקורות מגוונים וכלים של בינה מלאכותית (למשל סיכום, המחשה, תרגול).

        כתוב בעברית ברורה ומעוררת מוטיבציה.
        '''
        if api_key:
            try:response = client.chat.completions.create(
               model="gpt-4",
               messages=messages,
               temperature=0.7
                )
                reply = response.choices[0].message.content

                st.session_state.plan = plan
                st.markdown("### ✨ תכנית הלמידה שלך:")
                st.write(plan)
                if st.button("אני מוכן/ה לשלב הליווי"):
                    st.session_state.stage = 3
            except Exception as e:
                st.error(f"שגיאה בהתחברות ל-GPT: {e}")
        else:
            st.warning("נא להזין מפתח API בשורת הצד")

# שלב 3: ליווי
if st.session_state.stage == 3:
    st.header("שלב 3: ליווי הלמידה 🎯")
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "weekly_tasks" not in st.session_state:
        st.session_state.weekly_tasks = [
            {"שבוע": "שבוע 1", "משימה": "היכרות עם הנושא וקריאה ראשונית", "הושלם": False},
            {"שבוע": "שבוע 2", "משימה": "צפייה בחומר מסכם ותרגול", "הושלם": False},
            {"שבוע": "שבוע 3", "משימה": "העמקה והפקת תוצר", "הושלם": False},
        ]
    st.subheader("משימות שבועיות")
    for i, task in enumerate(st.session_state.weekly_tasks):
        completed = st.checkbox(f'{task["שבוע"]}: {task["משימה"]}', value=task["הושלם"], key=f"task_{i}")
        st.session_state.weekly_tasks[i]["הושלם"] = completed

    st.subheader("שוחח עם מנטו-סטדי")
    user_input = st.text_area("מה אתה רוצה לשאול או לשתף?")
    if st.button("שלח"):
        if user_input and api_key:
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            messages = [{"role": "system", "content": "אתה מנטור למידה תומך ומקצועי"}] + st.session_state.chat_history
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=messages,
                    temperature=0.7
                )
                reply = response["choices"][0]["message"]["content"]
                st.session_state.chat_history.append({"role": "assistant", "content": reply})
            except Exception as e:
                st.error(f"שגיאה מהשרת: {e}")

    for msg in reversed(st.session_state.chat_history):
        speaker = "👤 אתה" if msg["role"] == "user" else "🤖 מנטו-סטדי"
        st.markdown(f"**{speaker}:** {msg['content']}")
