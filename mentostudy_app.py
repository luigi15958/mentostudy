import streamlit as st
import openai
import datetime

st.set_page_config(page_title="Mentostudy - המנטור החכם ללמידה", layout="wide")

# קלט מפתח API
api_key = st.sidebar.text_input("🔑 הזן את OpenAI API Key שלך", type="password")
if api_key:
    openai.api_key = api_key

st.title("Mentostudy 🧠")
st.write("סוכן הלמידה החכם שלך - מותאם אישית לתחום, לקצב ולסקרנות שלך")

if "stage" not in st.session_state:
    st.session_state.stage = 1

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
            deadline = st.date_input("תאריך יעד לסיום התהליך", value=datetime.date.today())
            uploaded_file = st.file_uploader("העלה קובץ טקסט או PDF", type=["txt", "pdf"])
            source_link = st.text_input("או הדבק קישור למקור ידע")
        personal_note = st.text_area("💬 אמור לנו משהו אישי שחשוב לך שנדע כדי להתאים את תהליך הלמידה (למשל: אני רוצה ללמד את הבן שלי לכתוב מספרים)")
        submitted = st.form_submit_button("המשך לשלב הבא")
        if submitted:
            st.session_state.profile = {
                "name": name, "age": age, "gender": gender, "background": background,
                "knowledge": knowledge, "subject": subject, "goal": goal,
                "goal_text": goal_text, "deadline": str(deadline),
                "source_link": source_link, "personal_note": personal_note
            }
            st.session_state.stage = 2

if st.session_state.stage == 2:
    st.header("שלב 2: בניית תכנית הלמידה 📚")
    with st.spinner("בונה עבורך תכנית מותאמת אישית..."):
        profile = st.session_state.profile
        prompt = f'''
        צור תוכנית למידה מותאמת אישית עבור הלומד הבא:

        שם: {profile["name"]}
        גיל: {profile["age"]}
        רקע: {profile["background"]}
        לשון פנייה: {profile["gender"]}
        ידע קודם: {profile["knowledge"]}/5
        תחום הלמידה: {profile["subject"]}
        מטרה כללית: {profile["goal"]}
        פירוט מטרה: {profile["goal_text"]}
        תאריך יעד: {profile["deadline"]}
        קישור למקור ידע: {profile["source_link"]}
        פרטים נוספים חשובים: {profile["personal_note"]}

        צור תוכנית בת 6–8 שבועות שמבוססת על רמת הידע והמטרה, מחולקת לפי שלבים. כל שלב יכלול:
        - משימות ללמידה עצמאית
        - חיזוק מיומנויות לומד עצמאי
        - טכניקות למידה אפקטיביות
        - שימוש במקורות מרובים
        - רמזים לאיך ניתן להשתמש בבינה מלאכותית

        כתוב את התכנית בעברית ברורה, ידידותית ללומד.
        '''

        if api_key:
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "אתה מנטור למידה מקצועי ומעורר השראה."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7
                )
                plan = response['choices'][0]['message']['content']
                st.markdown("### ✨ תכנית הלמידה שלך:")
                st.write(plan)
                st.success("התוכנית מוכנה! בהמשך נוכל לעבור לשלב הליווי")
                if st.button("אני מוכן/ה להתחיל"):
                    st.session_state.stage = 3
            except Exception as e:
                st.error(f"שגיאה בהתחברות ל-GPT: {e}")
        else:
            st.warning("נא להזין מפתח API תקף משמאל כדי להמשיך")

if st.session_state.stage == 3:
    st.header("שלב 3: ליווי הלמידה (בהמשך הפיתוח)")
    st.info("בגרסה הבאה נוסיף תזכורות, משוב, המלצות AI ותוצרים חכמים 💡")
