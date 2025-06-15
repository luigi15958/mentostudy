import streamlit as st
from openai import OpenAI
import datetime

st.set_page_config(page_title="Mentostudy - המנטור שלך ללמידה", layout="wide")

st.markdown(
    "<style>body {direction: rtl; text-align: right;} .stTextInput input, .stTextArea textarea {text-align: right;}</style>",
    unsafe_allow_html=True
)

api_key = st.sidebar.text_input("🔑 הזן את OpenAI API Key שלך", type="password")
if api_key:
    client = OpenAI(api_key=api_key)

st.title("Mentostudy 🧠")
st.write("המנטור החכם שלך ללמידה מותאמת אישית")

if "stage" not in st.session_state:
    st.session_state.stage = 1

# שלב 1: אפיון הלומד
if st.session_state.stage == 1:
    st.header("שלב 1: אפיון הלומד")
    with st.form("user_profile"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("שם פרטי")
            age = st.number_input("גיל", min_value=5, max_value=120, step=1)
            gender = st.selectbox("לשון פנייה מועדפת", ["זכר", "נקבה", "אחר"])
            background = st.selectbox("רקע לימודי", ["תלמיד חטיבה", "תלמיד תיכון", "סטודנט", "מבוגר לומד", "אחר"])
            knowledge = st.slider("רמת ידע קודם בתחום", 1, 5)
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

# שלב 2: בניית תכנית למידה
if st.session_state.stage == 2:
    st.header("שלב 2: בניית תכנית למידה 📚")
    with st.spinner("בונה תכנית מותאמת אישית..."):
        profile = st.session_state.profile
        prompt = f'''
        צור תכנית למידה עבור:
        גיל: {profile["age"]}, רקע: {profile["background"]}, ידע קודם: {profile["knowledge"]}/5,
        תחום: {profile["subject"]}, מטרה: {profile["goal"]}, תאריך יעד: {profile["deadline"]},
        הערות: {profile["goal_text"]}, מידע נוסף: {profile["personal_note"]}

        חלק את התכנית לשלבים או שבועות. כל שלב יכלול משימות, טכניקות למידה, חיזוק עצמאות,
        המלצות למקורות ויישום כלים של בינה מלאכותית. כתוב בעברית ברורה ומעודדת.
        '''
        if api_key:
            try:
                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "אתה מנטור למידה מקצועי ותומך"},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7
                )
                plan = response.choices[0].message.content
                st.session_state.plan = plan
                st.markdown("### ✨ תכנית הלמידה שלך:")
                st.write(plan)
                if st.button("המשך לשלב הליווי"):
                    st.session_state.stage = 3
            except Exception as e:
                st.error(f"שגיאה מהשרת: {e}")
        else:
            st.warning("נא להזין מפתח API תקף")

# שלב 3: ליווי הלמידה
if st.session_state.stage == 3:
    st.header("שלב 3: ליווי תהליך הלמידה 🎯")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if "weekly_tasks" not in st.session_state:
        st.session_state.weekly_tasks = [
            {"שבוע": "שבוע 1", "משימה": "היכרות עם נושא והבנת עקרונות בסיסיים", "הושלם": False},
            {"שבוע": "שבוע 2", "משימה": "צפייה בחומר תומך + תרגול", "הושלם": False},
            {"שבוע": "שבוע 3", "משימה": "הפקת תוצר מסכם + רפלקציה", "הושלם": False},
        ]

    st.subheader("📋 משימות שבועיות")
    for i, task in enumerate(st.session_state.weekly_tasks):
        completed = st.checkbox(f'{task["שבוע"]}: {task["משימה"]}', value=task["הושלם"], key=f"task_{i}")
        st.session_state.weekly_tasks[i]["הושלם"] = completed

    st.subheader("💬 שיחה עם הסוכן שלך")
    user_input = st.text_area("מה ברצונך לשאול או לשתף?")
    if st.button("שלח"):
        if user_input and api_key:
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            messages = [{"role": "system", "content": "אתה מנטור למידה תומך ומעודד"}] + st.session_state.chat_history
            try:
                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=messages,
                    temperature=0.7
                )
                reply = response.choices[0].message.content
                st.session_state.chat_history.append({"role": "assistant", "content": reply})
            except Exception as e:
                st.error(f"שגיאה מהשרת: {e}")

    for msg in reversed(st.session_state.chat_history):
        speaker = "👤 אתה" if msg["role"] == "user" else "🤖 מנטו-סטדי"
        st.markdown(f"**{speaker}:** {msg['content']}")
