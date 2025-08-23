import streamlit as st
from sklearn.linear_model import LinearRegression
import feedparser
import numpy as np

USER_NAME = "Bạn"

st.sidebar.title("Danh sách nghệ sĩ")
selected_artist = st.sidebar.radio(
    "Chọn một nghệ sĩ:", 
    ["Laufey"]
)

videos = {
    "Laufey": [
        ("From The Start", "https://www.youtube.com/watch?v=rHvQakk1zMA&list=RDrHvQakk1zMA&start_radio=1"),
        ("Valentine", "https://www.youtube.com/watch?v=GsmQt-2xpw0&list=RDGsmQt-2xpw0&start_radio=1"),
        ("Falling Behind", "https://www.youtube.com/watch?v=ii7wMothcqI&list=RDii7wMothcqI&start_radio=1"),
        ("Promise", "https://www.youtube.com/watch?v=Zu2Spp4nrTM&list=RDZu2Spp4nrTM&start_radio=1")
    ]
}

st.title(f"Chào {USER_NAME}! App Giải trí và Sức khỏe")

tab_titles = [
    "Nghệ sĩ yêu thích",
    "Dự đoán giờ ngủ", 
    "Tin tức", 
    "Giá vàng", 
    "Kiểm tra sức khỏe (BMI)",
    "Điểm rủi ro tim mạch",
    "Nhu cầu nước hàng ngày",
    "Bước chân mỗi ngày"
]

tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs(tab_titles)

with tab1:
    st.header(f"Âm nhạc của {selected_artist}")
    for title, url in videos[selected_artist]:
        st.subheader(title)
        st.video(url)

with tab2:
    st.title("Dự đoán giờ ngủ lý tưởng")
    x = [
        [10, 8, 1],
        [20, 6, 5],
        [25, 3, 8],
        [30, 2, 6],
        [50, 2, 2],
        [15, 9, 2],
        [40, 4, 3]
    ]
    y = [10, 8, 6, 6, 5, 7, 9.5]
    model = LinearRegression()
    model.fit(x, y)

    st.write("Điền thông tin dưới đây để xem giờ ngủ phù hợp:")
    age = st.number_input("Tuổi của bạn:", min_value=5, max_value=100, value=25)
    activity = st.slider("Mức độ hoạt động (1 = ít, 10 = nhiều)", 1, 10, 5)
    screen_time = st.number_input("Thời gian sử dụng màn hình mỗi ngày (giờ)", min_value=0, max_value=24, value=6)

    if st.button("Tính giờ ngủ"):
        result = model.predict([[age, activity, screen_time]])[0]
        st.success(f"Bạn nên ngủ {result:.1f} giờ mỗi đêm")
        if result < 6.5:
            st.warning("Bạn có thể thiếu ngủ.")
        elif result > 9:
            st.info("Bạn có mức hoạt động cao, ngủ lâu sẽ giúp phục hồi.")
        else:
            st.success("Giấc ngủ cân bằng.")

with tab3:
    st.header("Tin mới nhất từ VnExpress")
    feed = feedparser.parse("https://vnexpress.net/rss/tin-moi-nhat.rss")
    for entry in feed.entries[:10]:
        st.subheader(entry.title)
        st.write(entry.published)
        st.write(entry.link)

with tab4:
    st.header("Giá vàng mới nhất từ Vietnamnet")
    feed = feedparser.parse("https://vietnamnet.vn/rss/kinh-doanh.rss")
    gold_news = [entry for entry in feed.entries if "vàng" in entry.title.lower() or "giá vàng" in entry.summary.lower()]
    if gold_news:
        for entry in gold_news[:5]:
            st.subheader(entry.title)
            st.write(entry.published)
            st.write(entry.link)
    else:
        st.warning("Không tìm thấy tin tức về giá vàng gần đây.")

with tab5:
    st.header("Kiểm tra BMI")
    can_nang = st.number_input("Cân nặng (kg)", min_value=10.0, max_value=200.0, value=60.0, step=0.1)
    chieu_cao = st.number_input("Chiều cao (m)", min_value=1.0, max_value=2.5, value=1.7, step=0.01)
    if st.button("Tính BMI"):
        bmi = can_nang / (chieu_cao ** 2)
        st.success(f"BMI của bạn là: {bmi:.2f}")
        if bmi < 18.5:
            st.warning("Thiếu cân.")
        elif 18.5 <= bmi < 25:
            st.info("Cân nặng hợp lý.")
        elif 25 <= bmi < 30:
            st.warning("Thừa cân.")
        else:
            st.error("Béo phì.")

with tab6:
    st.header("Dự đoán rủi ro tim mạch")
    x = np.array([
        [100, 2, 12],
        [95, 4, 15],
        [90, 6, 18],
        [85, 9, 20],
        [80, 12, 25],
        [75, 20, 50],
        [72, 30, 65],
        [70, 40, 70],
        [68, 50, 75],
        [66, 58, 78],
        [70, 65, 70],
        [75, 70, 68],
        [80, 75, 65],
        [85, 80, 60],
        [90, 85, 58],
    ])
    y = np.array([
        1.2, 1.3, 1.5, 1.6, 1.7,
        2.0, 2.3, 2.7, 3.0, 3.2,
        3.5, 3.8, 4.0, 4.3, 4.6
    ])
    model = LinearRegression()
    model.fit(x, y)

    hr = st.number_input("Nhịp tim (bpm)", min_value=40, max_value=200, value=75)
    age = st.number_input("Tuổi", min_value=1, max_value=120, value=30)
    weight = st.number_input("Cân nặng (kg)", min_value=10.0, max_value=200.0, value=60.0)

    if st.button("Kiểm tra rủi ro"):
        score = model.predict([[hr, age, weight]])[0]
        st.success(f"Điểm rủi ro: {score:.2f}")
        if score < 1.5:
            st.info("Rủi ro thấp.")
        elif score < 2.5:
            st.warning("Rủi ro nhẹ.")
        elif score < 3.5:
            st.warning("Rủi ro vừa.")
        else:
            st.error("Rủi ro cao, nên đi khám.")

with tab7:
    st.title("Lượng nước cần mỗi ngày")
    tuoi = st.number_input("Nhập tuổi của bạn:", min_value=1, max_value=100, value=18, step=1, key="tuoi")
    if st.button("Kiểm tra lượng nước"):
        if tuoi < 4:
            st.info("1.3 lít/ngày")
        elif 4 <= tuoi <= 8:
            st.info("1.7 lít/ngày")
        elif 9 <= tuoi <= 13:
            st.info("2.1-2.4 lít/ngày")
        elif 14 <= tuoi <= 18:
            st.info("2.3-3.3 lít/ngày")
        elif 19 <= tuoi <= 50:
            st.info("2.7 lít/ngày (nữ), 3.7 lít/ngày (nam)")
        elif tuoi > 50:
            st.info("2.5-3.0 lít/ngày")

with tab8:
    st.header("Số bước khuyến nghị mỗi ngày")
    age2 = st.number_input("Nhập tuổi của bạn:", min_value=0.0, max_value=130.0, value=18.0, step=1.0)
    if st.button("Kiểm tra bước chân"):
        if age2 < 18:
            st.info("12,000-15,000 bước/ngày")
        elif 17 < age2 <= 39:
            st.info("8,000-10,000 bước/ngày")
        elif 39 < age2 <= 64:
            st.warning("7,000-9,000 bước/ngày")
        elif age2 > 64:
            st.warning("6,000-8,000 bước/ngày")
