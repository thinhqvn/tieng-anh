import streamlit as st
import random
from datetime import datetime

# ================== CẤU HÌNH CƠ BẢN ==================
QUIZ_DURATION_MINUTES = 30
QUIZ_DURATION_SECONDS = QUIZ_DURATION_MINUTES * 60

st.set_page_config(
    page_title="Luyện tập tiếng Anh 9 - I Learn Smart World",
    page_icon="📘",
    layout="wide",
)

# ================== CSS GIAO DIỆN ==================
CUSTOM_CSS = """
<style>
/* Nền sáng, tươi */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #fdfbfb 0%, #f9f7ff 40%, #e2f6ff 100%);
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #f3f4f6;
}

/* Ẩn menu và footer nếu muốn gọn gàng */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

/* Thẻ scoreboard */
.score-box {
    background-color: rgba(255, 255, 255, 0.96);
    padding: 1rem 1.5rem;
    border-radius: 1rem;
    box-shadow: 0 4px 12px rgba(15, 23, 42, 0.08);
    border: 1px solid #e5e7eb;
}

/* Tiêu đề chính */
.main-title {
    font-size: 2rem;
    font-weight: 800;
    color: #111827;
}

/* Nhãn phụ */
.sub-title {
    font-size: 0.95rem;
    color: #6b7280;
}

/* Đồng hồ */
.timer-text {
    font-size: 1.3rem;
    font-weight: 700;
}

/* Ẩn chấm tròn radio trong phần lựa chọn đáp án */
div.row-widget.stRadio > div[role="radiogroup"] > label > div:first-child {
    display: none !important;
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ================== NGÂN HÀNG CÂU HỎI (MẪU) ==================
# Đây là câu hỏi minh hoạ, không lấy nguyên văn từ sách.
QUESTION_BANK = [
    # UNIT 1 - Vocabulary
    {
        "unit": 1,
        "skill": "Vocabulary",
        "question": "Choose the best word to complete the sentence:\n\n"
                    "My sister is very ____. She often helps her friends with homework.",
        "options": ["shy", "selfish", "helpful", "lazy"],
        "answer_index": 2,
        "explanation": "‘Helpful’ means willing to help others."
    },
    {
        "unit": 1,
        "skill": "Vocabulary",
        "question": "Choose the word that is CLOSEST in meaning to ‘intelligent’.",
        "options": ["clever", "boring", "noisy", "careless"],
        "answer_index": 0,
        "explanation": "‘Clever’ is similar in meaning to ‘intelligent’."
    },
    # UNIT 1 - Grammar
    {
        "unit": 1,
        "skill": "Grammar",
        "question": "Choose the correct sentence.",
        "options": [
            "She don’t like playing badminton.",
            "She doesn’t likes playing badminton.",
            "She doesn’t like playing badminton.",
            "She not like playing badminton."
        ],
        "answer_index": 2,
        "explanation": "With ‘she’, we use ‘doesn’t + bare verb’: doesn’t like."
    },
    {
        "unit": 1,
        "skill": "Grammar",
        "question": "Choose the correct verb form:\n\n"
                    "They ____ to school every day.",
        "options": ["go", "goes", "is going", "going"],
        "answer_index": 0,
        "explanation": "‘They’ + V (present simple): go."
    },
    # UNIT 1 - Reading
    {
        "unit": 1,
        "skill": "Reading",
        "question": "Read the text and answer the question:\n\n"
                    "Minh lives in a small town. Every morning, he gets up at 6 a.m., "
                    "has breakfast with his family, and then walks to school. It takes "
                    "him about fifteen minutes to get there.\n\n"
                    "Question: How does Minh go to school?",
        "options": ["By bus", "On foot", "By bike", "By car"],
        "answer_index": 1,
        "explanation": "‘walks to school’ → he goes on foot."
    },
    {
        "unit": 1,
        "skill": "Reading",
        "question": "According to the text about Minh, when does he get up?",
        "options": ["At 5 a.m.", "At 6 a.m.", "At 6:30 a.m.", "At 7 a.m."],
        "answer_index": 1,
        "explanation": "The text says: ‘he gets up at 6 a.m.’"
    },
    # UNIT 2 - Vocabulary
    {
        "unit": 2,
        "skill": "Vocabulary",
        "question": "Choose the best word to complete the sentence:\n\n"
                    "Air ____ is becoming a serious problem in big cities.",
        "options": ["pollution", "population", "tradition", "education"],
        "answer_index": 0,
        "explanation": "The correct phrase is ‘air pollution’."
    },
    {
        "unit": 2,
        "skill": "Vocabulary",
        "question": "Choose the word that is OPPOSITE in meaning to ‘modern’.",
        "options": ["ancient", "crowded", "expensive", "quiet"],
        "answer_index": 0,
        "explanation": "‘Ancient’ means very old, opposite of ‘modern’."
    },
    # UNIT 2 - Grammar
    {
        "unit": 2,
        "skill": "Grammar",
        "question": "Choose the correct sentence using ‘used to’.",
        "options": [
            "I used to play football when I am a child.",
            "I use to play football when I was a child.",
            "I used play football when I was a child.",
            "I used to play football when I was a child."
        ],
        "answer_index": 3,
        "explanation": "Structure: used to + V (past habit)."
    },
    {
        "unit": 2,
        "skill": "Grammar",
        "question": "Choose the correct verb:\n\n"
                    "People ____ recycle more to protect the environment.",
        "options": ["should", "mustn’t", "can’t", "did"],
        "answer_index": 0,
        "explanation": "‘should’ expresses advice: should recycle more."
    },
    # UNIT 2 - Reading
    {
        "unit": 2,
        "skill": "Reading",
        "question": "Read the text and answer the question:\n\n"
                    "Many students ride their bikes to school instead of using motorbikes. "
                    "This helps reduce air pollution and keeps them healthy.\n\n"
                    "Question: Why do students ride their bikes to school?",
        "options": [
            "Because it is more expensive.",
            "To reduce air pollution and stay healthy.",
            "Because they don’t like motorbikes.",
            "Because there are no buses."
        ],
        "answer_index": 1,
        "explanation": "The text states both reasons: reduce pollution and keep healthy."
    },
    {
        "unit": 2,
        "skill": "Reading",
        "question": "According to the text, which statement is TRUE?",
        "options": [
            "Riding bikes is bad for students’ health.",
            "Using motorbikes is the only way to go to school.",
            "Riding bikes can help protect the environment.",
            "All students must walk to school."
        ],
        "answer_index": 2,
        "explanation": "The text says riding bikes helps reduce air pollution."
    },
]

SKILLS = ["Vocabulary", "Grammar", "Reading", "Mixed"]
MODES = ["Practice", "Test"]

# ================== HÀM HỖ TRỢ ==================
def init_session_state():
    defaults = {
        "unit": 1,
        "skill": "Vocabulary",
        "mode": "Practice",
        "quiz_questions": [],
        "answers": [],
        "current_q_index": 0,
        "score": 0,
        "answered_count": 0,
        "quiz_running": False,
        "quiz_finished": False,
        "start_time": None,
        "quiz_run_id": 0,
        "just_submitted_msg": "",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def filter_questions(unit, skill):
    if skill == "Mixed":
        candidates = [q for q in QUESTION_BANK if q["unit"] == unit]
    else:
        candidates = [q for q in QUESTION_BANK if q["unit"] == unit and q["skill"] == skill]
    return candidates


def start_quiz(unit, skill, mode, num_questions=10):
    candidates = filter_questions(unit, skill)
    if not candidates:
        st.warning("Chưa có câu hỏi cho Unit/Skill này. Vui lòng chọn Unit hoặc Skill khác.")
        return

    n = min(num_questions, len(candidates))
    quiz_qs = random.sample(candidates, n)

    st.session_state["unit"] = unit
    st.session_state["skill"] = skill
    st.session_state["mode"] = mode
    st.session_state["quiz_questions"] = quiz_qs
    st.session_state["answers"] = [
        {"selected": None, "is_correct": None} for _ in quiz_qs
    ]
    st.session_state["current_q_index"] = 0
    st.session_state["score"] = 0
    st.session_state["answered_count"] = 0
    st.session_state["quiz_running"] = True
    st.session_state["quiz_finished"] = False
    st.session_state["start_time"] = datetime.now()
    st.session_state["quiz_run_id"] += 1
    st.session_state["just_submitted_msg"] = ""


def get_remaining_time():
    if not st.session_state["quiz_running"] or st.session_state["start_time"] is None:
        return QUIZ_DURATION_SECONDS
    elapsed = (datetime.now() - st.session_state["start_time"]).total_seconds()
    remaining = QUIZ_DURATION_SECONDS - int(elapsed)
    return max(0, remaining)


def format_time(seconds):
    m = seconds // 60
    s = seconds % 60
    return f"{int(m):02d}:{int(s):02d}"


def finish_quiz():
    """Kết thúc bài (hết giờ hoặc bấm kết thúc)."""
    if st.session_state["quiz_finished"]:
        return

    qs = st.session_state["quiz_questions"]
    ans = st.session_state["answers"]

    if st.session_state["mode"] == "Test":
        score = 0
        answered_count = 0
        for i, q in enumerate(qs):
            sel = ans[i]["selected"]
            if sel is not None:
                answered_count += 1
                if sel == q["answer_index"]:
                    score += 1
                    ans[i]["is_correct"] = True
                else:
                    ans[i]["is_correct"] = False
            else:
                ans[i]["is_correct"] = False
        st.session_state["score"] = score
        st.session_state["answered_count"] = answered_count
    else:
        # Practice mode: score đã được cộng dần, chỉ cần đếm lại số câu đã trả lời
        answered_count = sum(1 for a in ans if a["selected"] is not None)
        st.session_state["answered_count"] = answered_count

    st.session_state["quiz_running"] = False
    st.session_state["quiz_finished"] = True


def go_prev():
    if st.session_state["current_q_index"] > 0:
        st.session_state["current_q_index"] -= 1


def go_next():
    qs = st.session_state.get("quiz_questions", [])
    if qs and st.session_state["current_q_index"] < len(qs) - 1:
        st.session_state["current_q_index"] += 1


def render_scoreboard():
    qs = st.session_state["quiz_questions"]
    total_q = len(qs) if qs else 0
    remaining_secs = get_remaining_time()
    time_str = format_time(remaining_secs)

    unit = st.session_state["unit"]
    skill = st.session_state["skill"]
    mode = st.session_state["mode"]
    score = st.session_state["score"]
    answered = st.session_state["answered_count"]

    col1, col2, col3, col4 = st.columns(4)

    # Ô Unit & Skill
    with col1:
        card_html = f"""
        <div class="score-box">
            <div><b>🧩 Unit &amp; Skill</b></div>
            <div><strong>Unit {unit}</strong> – <em>{skill}</em></div>
            <div>Mode: <strong>{mode}</strong></div>
        </div>
        """
        st.markdown(card_html, unsafe_allow_html=True)

    # Ô Điểm hiện tại
    with col2:
        card_html = f"""
        <div class="score-box">
            <div><b>✅ Điểm hiện tại</b></div>
            <div style="font-size:1.4rem; font-weight:700; margin-top:0.25rem;">
                {score} / {total_q}
            </div>
        </div>
        """
        st.markdown(card_html, unsafe_allow_html=True)

    # Ô Số câu đã làm
    with col3:
        card_html = f"""
        <div class="score-box">
            <div><b>📝 Số câu đã làm</b></div>
            <div style="font-size:1.4rem; font-weight:700; margin-top:0.25rem;">
                {answered} / {total_q}
            </div>
        </div>
        """
        st.markdown(card_html, unsafe_allow_html=True)

    # Ô Thời gian còn lại
    with col4:
        card_html = f"""
        <div class="score-box">
            <div><b>⏱ Thời gian còn lại</b></div>
            <div class="timer-text" style="margin-top:0.25rem;">
                {time_str}
            </div>
        </div>
        """
        st.markdown(card_html, unsafe_allow_html=True)

    # Hết giờ thì tự nộp bài
    if remaining_secs == 0 and st.session_state["quiz_running"]:
        st.warning("⏰ Hết giờ! Hệ thống tự động nộp bài.")
        finish_quiz()


def render_question_area():
    qs = st.session_state["quiz_questions"]
    ans = st.session_state["answers"]

    if not qs:
        st.info("Hãy chọn Unit, Skill và bấm **Bắt đầu** để luyện tập.")
        return

    # Nếu đã kết thúc bài → hiển thị kết quả tổng
    if st.session_state["quiz_finished"]:
        st.subheader("🎉 Kết quả bài luyện tập")
        total_q = len(qs)
        score = st.session_state["score"]
        if total_q > 0:
            st.write(f"**Điểm: {score} / {total_q}** – Tỉ lệ đúng: {score/total_q*100:.1f}%")
        else:
            st.write("Chưa có câu hỏi trong bài.")

        result_rows = []
        for i, q in enumerate(qs):
            selected = ans[i]["selected"]
            selected_text = (
                q["options"][selected] if selected is not None else "Chưa trả lời"
            )
            correct_text = q["options"][q["answer_index"]]
            is_correct = ans[i]["is_correct"]
            result_rows.append({
                "Câu": i + 1,
                "Kỹ năng": q["skill"],
                "Bạn chọn": selected_text,
                "Đáp án đúng": correct_text,
                "Kết quả": "Đúng" if is_correct else "Sai",
            })

        if result_rows:
            st.write("📋 **Chi tiết từng câu**")
            st.dataframe(result_rows, hide_index=True)
        return

    # 👉 Thông báo nhỏ cho chế độ Test sau khi lưu đáp án
    msg = st.session_state.get("just_submitted_msg", "")
    if msg:
        st.info(msg)
        st.session_state["just_submitted_msg"] = ""

    # ===== Đang làm một câu =====
    idx = st.session_state["current_q_index"]
    q = qs[idx]
    answer_state = ans[idx]

    st.markdown(f"### Câu {idx + 1}/{len(qs)} – {q['skill']}")
    st.write(q["question"])

    raw_options = q["options"]
    display_options = list(raw_options)

    # Nếu đang ở Practice và câu này đã được nộp → gắn icon vào label
    if st.session_state["mode"] == "Practice" and answer_state["selected"] is not None:
        sel_idx = answer_state["selected"]
        correct_idx = q["answer_index"]
        for i, opt in enumerate(raw_options):
            suffix = ""
            if sel_idx == correct_idx:
                # Làm đúng → chỉ tick chỗ được chọn
                if i == sel_idx:
                    suffix = " ✅"
            else:
                # Làm sai → cross chỗ chọn sai, tick chỗ đúng
                if i == sel_idx:
                    suffix = " ❌"
                if i == correct_idx:
                    suffix = " ✅"
            display_options[i] = opt + suffix

    # Tạo danh sách option cho radio (thêm dòng "-- Chọn đáp án --" ở đầu)
    options = ["-- Chọn đáp án --"] + display_options

    # Vị trí mặc định của con trỏ radio
    if answer_state["selected"] is None:
        default_index = 0
    else:
        default_index = answer_state["selected"] + 1

    widget_key = f"quiz_{st.session_state['quiz_run_id']}_q_{idx}"
    selected_label = st.radio(
        "Chọn đáp án:",
        options,
        index=default_index,
        key=widget_key,
    )

    selected_index = None
    if selected_label != "-- Chọn đáp án --":
        selected_index = options.index(selected_label) - 1

    # ================== HÀNG NÚT ĐIỀU KHIỂN ==================
    col_btn1, col_btn2, col_btn3 = st.columns(3)

    # 🔹 Nút Nộp câu trả lời (Practice + Test)
    with col_btn1:
        if st.button("✅ Nộp câu trả lời", key=f"submit_{idx}"):
            if selected_index is None:
                st.warning("Hãy chọn một đáp án trước khi nộp.")
            else:
                first_time_submit = answer_state["selected"] is None
                if first_time_submit:
                    st.session_state["answered_count"] += 1

                answer_state["selected"] = selected_index

                if st.session_state["mode"] == "Practice":
                    # Chấm luôn
                    if selected_index == q["answer_index"]:
                        answer_state["is_correct"] = True
                        if first_time_submit:
                            st.session_state["score"] += 1
                    else:
                        answer_state["is_correct"] = False

                    # Rerun để vẽ lại icon ✅ / ❌ trên đáp án ngay lập tức
                    st.rerun()

                else:
                    # ===== MODE TEST =====
                    # Không show đúng/sai, chỉ lưu + auto skip
                    st.session_state["just_submitted_msg"] = (
                        f"✅ Đã lưu đáp án cho câu {idx + 1}."
                    )

                    if idx < len(qs) - 1:
                        # Chuyển sang câu kế tiếp
                        go_next()
                    else:
                        # Câu cuối thì nộp bài
                        finish_quiz()

                    # Rerun để hiển thị câu mới + dòng "Đã lưu..."
                    st.rerun()

    # 🔹 Nút Câu trước / Câu tiếp
    with col_btn2:
        st.button(
            "⬅ Câu trước",
            disabled=(idx == 0),
            key=f"prev_{idx}",
            on_click=go_prev,
        )

    with col_btn3:
        st.button(
            "Câu tiếp ➡",
            disabled=(idx == len(qs) - 1),
            key=f"next_{idx}",
            on_click=go_next,
        )

    # 🔹 Feedback thêm cho Practice
    if st.session_state["mode"] == "Practice" and answer_state["selected"] is not None:
        if answer_state["is_correct"] is True:
            # Đúng: chỉ hiện báo đúng, KHÔNG có giải thích
            st.success("🎯 Chính xác! Rất tốt!")
        elif answer_state["is_correct"] is False:
            # Sai: hiện báo sai + giải thích
            correct_text = raw_options[q["answer_index"]]
            st.error(f"❌ Chưa chính xác. Đáp án đúng là: **{correct_text}**")
            st.info(f"Giải thích: {q['explanation']}")

    st.markdown("---")
    if st.button("📤 Kết thúc bài và xem kết quả", key="finish_quiz"):
        finish_quiz()



# ================== GIAO DIỆN CHÍNH ==================
def main():
    init_session_state()

    st.markdown(
        '<h1 class="main-title">📘 Luyện tập tiếng Anh 9 – I Learn Smart World</h1>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<p class="sub-title">Web luyện trắc nghiệm giúp học sinh ôn tập sau giờ học: '
        'bám sát từng Unit, kỹ năng Vocabulary – Grammar – Reading, có bảng điểm và đồng hồ đếm ngược.</p>',
        unsafe_allow_html=True,
    )

    # Sidebar: cấu hình bài luyện
    st.sidebar.header("🧩 Nội dung tập luyện")
    unit = st.sidebar.selectbox("Chọn Unit", options=list(range(1, 11)), index=0)
    skill = st.sidebar.selectbox("Chọn kỹ năng", options=SKILLS, index=0)
    mode = st.sidebar.radio("Chế độ làm bài", options=MODES, index=0)
    num_q = st.sidebar.slider("Số câu trong bài", min_value=5, max_value=20, value=10, step=1)

    st.sidebar.markdown("---")
    if st.sidebar.button("🚀 Bắt đầu / Làm lại bài"):
        start_quiz(unit, skill, mode, num_questions=num_q)

    # Hiển thị scoreboard nếu đã có bài
    if st.session_state["quiz_questions"]:
        render_scoreboard()

    # Vùng câu hỏi chính
    render_question_area()


if __name__ == "__main__":
    main()
