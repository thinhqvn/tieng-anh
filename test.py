import streamlit as st
import random
from datetime import datetime

# ================== CẤU HÌNH CƠ BẢN ==================
QUIZ_DURATION_MINUTES = 30
QUIZ_DURATION_SECONDS = QUIZ_DURATION_MINUTES * 60

st.set_page_config(
    page_title="Luyện tập: Bảo vệ môi trường",
    page_icon="🌱",
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

/* Ẩn menu và footer để gọn gàng */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

/* Thẻ scoreboard (4 ô trên đầu) */
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

/* Khung hiển thị CÂU HỎI */
.question-card {
    background-color: rgba(255, 255, 255, 0.96);
    padding: 1.25rem 1.5rem;
    border-radius: 1rem;
    box-shadow: 0 4px 10px rgba(15, 23, 42, 0.06);
    border: 1px solid #e5e7eb;
    margin-top: 0.5rem;
    margin-bottom: 0.75rem;
    font-size: 1.02rem;
    line-height: 1.5;
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ================== NGÂN HÀNG CÂU HỎI: BẢO VỆ MÔI TRƯỜNG ==================
# Chỉ là câu hỏi kiến thức môi trường, không phân loại Grammar/Reading
QUESTION_BANK = [
    {
        "question": "Which of the following is a type of renewable energy?",
        "options": ["Coal power", "Oil power", "Solar power", "Diesel power"],
        "answer_index": 2,
        "explanation": "Solar power comes from the sun and can be replaced naturally."
    },
    {
        "question": "Which source of energy is NOT renewable?",
        "options": ["Wind", "Hydropower", "Natural gas", "Solar"],
        "answer_index": 2,
        "explanation": "Natural gas is a fossil fuel and cannot be replaced quickly."
    },
    {
        "question": "Which daily habit helps reduce plastic waste the MOST?",
        "options": [
            "Buying a new plastic bottle every day",
            "Using a reusable water bottle",
            "Throwing plastic into the general bin",
            "Burning plastic at home"
        ],
        "answer_index": 1,
        "explanation": "Reusable bottles replace many single-use plastic bottles."
    },
    {
        "question": "Which item should go into the \"organic waste\" bin?",
        "options": ["A glass bottle", "Vegetable peels", "An old battery", "A broken phone"],
        "answer_index": 1,
        "explanation": "Vegetable peels can rot and become compost, so they are organic waste."
    },
    {
        "question": "Which kind of waste should be put into the \"e-waste\" collection box?",
        "options": ["Banana skins", "Old newspapers", "Broken mobile phones", "Glass bottles"],
        "answer_index": 2,
        "explanation": "E-waste includes old electronic devices like phones and computers."
    },
    {
        "question": "Which item should go into the \"paper recycling\" bin?",
        "options": ["An empty can", "A cardboard box", "A plastic straw", "A glass cup"],
        "answer_index": 1,
        "explanation": "Cardboard is made from paper and can be recycled with paper."
    },
    {
        "question": "Which phrase best describes \"waste separation\"?",
        "options": [
            "Mixing all types of rubbish together",
            "Burning rubbish in the garden",
            "Sorting rubbish into different groups before throwing it away",
            "Hiding rubbish under the ground"
        ],
        "answer_index": 2,
        "explanation": "Waste separation means sorting rubbish into groups like paper, plastic and organic."
    },
    {
        "question": "Which of the following is the BEST way to save electricity at home?",
        "options": [
            "Leaving the TV on all night",
            "Turning off lights when leaving a room",
            "Using more air conditioners",
            "Opening the fridge many times"
        ],
        "answer_index": 1,
        "explanation": "Turning off lights when not needed helps reduce electricity use."
    },
    {
        "question": "What is the main gas that causes the greenhouse effect?",
        "options": ["Oxygen (O2)", "Nitrogen (N2)", "Carbon dioxide (CO2)", "Hydrogen (H2)"],
        "answer_index": 2,
        "explanation": "Carbon dioxide is one of the main greenhouse gases warming the Earth."
    },
    {
        "question": "What do we call the total amount of CO2 that a person or activity produces?",
        "options": ["Green zone", "Carbon footprint", "Ozone layer", "Climate line"],
        "answer_index": 1,
        "explanation": "Carbon footprint is the total amount of carbon dioxide produced."
    },
    {
        "question": "Which of these actions directly reduces air pollution from transport?",
        "options": [
            "Driving alone in a car every day",
            "Carpooling with friends",
            "Buying a bigger car",
            "Leaving the engine on while waiting"
        ],
        "answer_index": 1,
        "explanation": "Carpooling means fewer cars on the road and less air pollution."
    },
    {
        "question": "Which habit helps save water most effectively?",
        "options": [
            "Taking very long showers",
            "Letting the tap run while brushing teeth",
            "Fixing leaking taps quickly",
            "Washing a small number of clothes many times"
        ],
        "answer_index": 2,
        "explanation": "Fixing leaks prevents a lot of water from being wasted."
    },
    {
        "question": "Which of the following is an example of wind energy?",
        "options": [
            "A coal power plant",
            "A wind farm with many turbines",
            "A gas stove in the kitchen",
            "A petrol generator"
        ],
        "answer_index": 1,
        "explanation": "A wind farm uses moving air to turn turbines and make electricity."
    },
    {
        "question": "Hydropower mainly uses the energy of ______ to make electricity.",
        "options": ["moving water", "sunlight", "hot rocks", "natural gas"],
        "answer_index": 0,
        "explanation": "Hydropower plants use the force of moving water."
    },
    {
        "question": "Geothermal energy comes from ______.",
        "options": [
            "the heat inside the Earth",
            "the light of the Moon",
            "the wind in the mountains",
            "the waves in the sea"
        ],
        "answer_index": 0,
        "explanation": "Geothermal energy is heat stored under the Earth's surface."
    },
    {
        "question": "A city produced 200,000 tons of household waste last year. 25 percent of this waste was recycled. How many tons were recycled?",
        "options": ["25,000 tons", "50,000 tons", "100,000 tons", "150,000 tons"],
        "answer_index": 1,
        "explanation": "25% of 200,000 is 50,000 tons."
    },
    {
        "question": "The same city produced 200,000 tons of waste and recycled 25 percent. How many tons went to landfill?",
        "options": ["50,000 tons", "100,000 tons", "150,000 tons", "200,000 tons"],
        "answer_index": 2,
        "explanation": "If 25% is recycled, 75% goes to landfill: 75% of 200,000 is 150,000 tons."
    },
    {
        "question": "Planting more trees in a city mainly helps to ______.",
        "options": [
            "make the air cleaner",
            "increase traffic jams",
            "create more plastic waste",
            "make the city noisier"
        ],
        "answer_index": 0,
        "explanation": "Trees absorb CO2 and release oxygen, improving air quality."
    },
    {
        "question": "Which action at the supermarket is the MOST environmentally friendly?",
        "options": [
            "Using a new plastic bag every time",
            "Bringing your own cloth bag",
            "Taking two plastic bags for each item",
            "Asking for extra plastic bags"
        ],
        "answer_index": 1,
        "explanation": "Cloth bags can be reused many times and reduce plastic waste."
    },
    {
        "question": "Which product label shows that a plastic bottle can be recycled?",
        "options": [
            "A picture of a tree",
            "A green star",
            "A triangle of three chasing arrows",
            "A picture of a car"
        ],
        "answer_index": 2,
        "explanation": "The triangle of three arrows is the universal recycling symbol."
    },
]

MODES = ["Practice", "Test"]

# ================== HÀM HỖ TRỢ ==================
def init_session_state():
    defaults = {
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
        "scroll_to_questions": False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def start_quiz(mode: str, num_questions: int):
    """Khởi tạo bài mới khi bấm START."""
    if not QUESTION_BANK:
        st.error("Chưa có câu hỏi trong ngân hàng.")
        return

    n = min(num_questions, len(QUESTION_BANK))
    quiz_qs = random.sample(QUESTION_BANK, n)

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
    st.session_state["scroll_to_questions"] = True  # báo hiệu cần cuộn xuống


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
    """Kết thúc bài (hết giờ hoặc bấm Kết thúc)."""
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
        # Practice: score đã cộng dần, chỉ đếm số câu đã trả lời
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

    mode = st.session_state["mode"]
    score = st.session_state["score"]
    answered = st.session_state["answered_count"]

    col1, col2, col3, col4 = st.columns(4)

    # Chủ đề & chế độ
    with col1:
        card_html = f"""
        <div class="score-box">
            <div><b>🌱 Chủ đề</b></div>
            <div><strong>Bảo vệ môi trường</strong></div>
            <div>Chế độ: <strong>{mode}</strong></div>
        </div>
        """
        st.markdown(card_html, unsafe_allow_html=True)

    # Điểm
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

    # Số câu đã làm
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

    # Thời gian còn lại
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


def scroll_to_question_section():
    """Sau khi bấm START, cuộn xuống vùng câu hỏi."""
    if st.session_state.get("scroll_to_questions"):
        st.markdown(
            """
            <script>
            const q = document.getElementById("question-section");
            if (q) {
                q.scrollIntoView({behavior: "smooth", block: "start"});
            }
            </script>
            """,
            unsafe_allow_html=True,
        )
        st.session_state["scroll_to_questions"] = False


def render_question_area():
    qs = st.session_state["quiz_questions"]
    ans = st.session_state["answers"]

    if not qs:
        st.info("Hãy bấm nút **START** để bắt đầu bài luyện tập về bảo vệ môi trường.")
        return

    # Nếu đã kết thúc bài
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
                "Bạn chọn": selected_text,
                "Đáp án đúng": correct_text,
                "Kết quả": "Đúng" if is_correct else "Sai",
            })

        if result_rows:
            st.write("📋 **Chi tiết từng câu**")
            st.dataframe(result_rows, hide_index=True)
        return

    # Thông báo nhỏ cho Test mode
    msg = st.session_state.get("just_submitted_msg", "")
    if msg:
        st.info(msg)
        st.session_state["just_submitted_msg"] = ""

    # ===== Đang làm một câu =====
    idx = st.session_state["current_q_index"]
    q = qs[idx]
    answer_state = ans[idx]

    st.markdown(f"### Câu {idx + 1}/{len(qs)}")

    # Câu hỏi trong khung
    question_html = q["question"].replace("\n", "<br>")
    st.markdown(
        f'<div class="question-card">{question_html}</div>',
        unsafe_allow_html=True,
    )

    raw_options = q["options"]
    display_options = list(raw_options)

    # Gắn icon cho Practice mode nếu câu đã nộp
    if st.session_state["mode"] == "Practice" and answer_state["selected"] is not None:
        sel_idx = answer_state["selected"]
        correct_idx = q["answer_index"]
        for i, opt in enumerate(raw_options):
            suffix = ""
            if sel_idx == correct_idx:
                if i == sel_idx:
                    suffix = " ✅"
            else:
                if i == sel_idx:
                    suffix = " ❌"
                if i == correct_idx:
                    suffix = " ✅"
            display_options[i] = opt + suffix

    options = ["-- Chọn đáp án --"] + display_options

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

    # ================== HÀNG NÚT ==================
    col_btn1, col_btn2, col_btn3 = st.columns(3)

    # Nộp câu trả lời
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
                    if selected_index == q["answer_index"]:
                        answer_state["is_correct"] = True
                        if first_time_submit:
                            st.session_state["score"] += 1
                    else:
                        answer_state["is_correct"] = False

                    st.rerun()
                else:
                    st.session_state["just_submitted_msg"] = (
                        f"✅ Đã lưu đáp án cho câu {idx + 1}."
                    )
                    if idx < len(qs) - 1:
                        go_next()
                    else:
                        finish_quiz()
                    st.rerun()

    # Câu trước / Câu tiếp
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

    # Feedback Practice
    if st.session_state["mode"] == "Practice" and answer_state["selected"] is not None:
        if answer_state["is_correct"] is True:
            st.success("🎯 Chính xác! Rất tốt!")
        elif answer_state["is_correct"] is False:
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
        '<h1 class="main-title">🌱 Luyện tập trắc nghiệm: Bảo vệ môi trường</h1>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<p class="sub-title">Học sinh luyện tập các câu hỏi về năng lượng tái tạo, phân loại rác, '
        'thói quen xanh và kiến thức môi trường – có đồng hồ đếm ngược và bảng điểm.</p>',
        unsafe_allow_html=True,
    )

    st.markdown("### ⚙️ Cài đặt bài luyện tập")

    col_left, col_right = st.columns([2, 1])

    with col_left:
        mode_choice = st.radio(
            "Chọn chế độ làm bài:",
            MODES,
            index=0,
            horizontal=True,
        )
        max_q = len(QUESTION_BANK)
        num_q = st.slider(
            "Số câu hỏi trong bài:",
            min_value=5,
            max_value=max_q,
            value=min(10, max_q),
            step=1,
        )

    with col_right:
        st.write("")
        st.write("")
        if st.button("🚀 START / LÀM LẠI BÀI", use_container_width=True):
            start_quiz(mode_choice, num_q)

    if st.session_state["quiz_questions"]:
        render_scoreboard()

    # Anchor cho phần câu hỏi + auto scroll
    st.markdown('<div id="question-section"></div>', unsafe_allow_html=True)
    scroll_to_question_section()

    render_question_area()


if __name__ == "__main__":
    main()
