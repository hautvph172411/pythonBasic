import streamlit as st
from PIL import Image
import pandas as pd
import time
import base64
from streamlit_lottie import st_lottie
import requests
import json
import numpy as np
import matplotlib.pyplot as plt

# Page configuration
st.set_page_config(
    page_title="Interactive CV",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for animations and styling
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@100;300;400;500;700;900&display=swap');

* {
    font-family: 'Roboto', sans-serif;
}

.highlight {
    padding: 20px;
    border-radius: 10px;
    margin-bottom: 20px;
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    transition: transform 0.3s ease;
}

.highlight:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 20px rgba(0,0,0,0.1);
}

.skill-bar {
    height: 10px;
    border-radius: 5px;
    background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%);
    margin-bottom: 15px;
}

.fade-in {
    animation: fadeIn 1.5s;
}

@keyframes fadeIn {
    0% { opacity: 0; }
    100% { opacity: 1; }
}

.slide-in {
    animation: slideIn 1s ease-out;
}

@keyframes slideIn {
    0% { transform: translateX(-50px); opacity: 0; }
    100% { transform: translateX(0); opacity: 1; }
}

.bounce {
    animation: bounce 1s;
}

@keyframes bounce {
    0%, 20%, 50%, 80%, 100% {transform: translateY(0);}
    40% {transform: translateY(-20px);}
    60% {transform: translateY(-10px);}
}

.section-title {
    font-size: 24px;
    font-weight: 700;
    margin-bottom: 20px;
    color: #333;
    border-bottom: 2px solid #4facfe;
    padding-bottom: 10px;
}

.timeline-item {
    padding: 15px;
    border-left: 2px solid #4facfe;
    position: relative;
    margin-left: 20px;
    margin-bottom: 20px;
}

.timeline-item:before {
    content: '';
    position: absolute;
    width: 15px;
    height: 15px;
    border-radius: 50%;
    background: #4facfe;
    left: -8.5px;
    top: 15px;
}

.contact-icon {
    font-size: 20px;
    margin-right: 10px;
    color: #4facfe;
}

.profile-container {
    display: flex;
    align-items: center;
    margin-bottom: 30px;
}

.profile-image {
    border-radius: 50%;
    width: 150px;
    height: 150px;
    object-fit: cover;
    border: 5px solid #fff;
    box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    margin-right: 30px;
}

.profile-text {
    flex: 1;
}

.name {
    font-size: 36px;
    font-weight: 700;
    margin-bottom: 5px;
    color: #333;
}

.title {
    font-size: 20px;
    color: #666;
    margin-bottom: 15px;
}

.bio {
    font-size: 16px;
    line-height: 1.6;
    color: #555;
}

.skills-section {
    margin-top: 30px;
    padding: 20px;
    background-color: #f8f9fa;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# Function to load Lottie animations
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Sidebar
def sidebar():
    st.sidebar.title("Trần Văn Hậu")
    
    # Add profile picture to sidebar
    profile_url = "https://scontent.fhan17-1.fna.fbcdn.net/v/t39.30808-1/454004006_3477787332520265_3062416834254944162_n.jpg?stp=dst-jpg_s480x480_tt6&_nc_cat=110&ccb=1-7&_nc_sid=e99d92&_nc_eui2=AeF8s7yoXFdnDjEfJAMVaOU2uy-RFL5bx_u7L5EUvlvH-0Apl3xB24VRsIkZZDcvH2evrxU5UPE290TRFAVzSJGZ&_nc_ohc=qi6mnJUeOiMQ7kNvgGSZ8LH&_nc_oc=AdhFzExGdB3Hw9tqKWTCffLHxebrvLedaKFyUdxmYxWrLIAc3dKclPW2Nx17LAR7wxtaulMfq_7UrRwhEe-OqhfP&_nc_zt=24&_nc_ht=scontent.fhan17-1.fna&_nc_gid=AbNYMcz_Jf09LkMoALl0JuB&oh=00_AYE5s1k5H-M0_xqYRm2jP7cOEFxtDC6plGsjYKCbaDdmZg&oe=67D993B3"
    st.sidebar.image(profile_url, width=200)
    
    # Lottie animation in sidebar
    lottie_coding = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_fcfjwiyb.json")
    if lottie_coding:
        st_lottie(lottie_coding, height=200, key="coding")
    
    # Download CV button
    st.sidebar.markdown("### Download CV")
    st.sidebar.download_button(
        label="📥 Download PDF",
        data=b"Sample CV data - in a real app this would be a PDF file",
        file_name="sample_cv.pdf",
        mime="application/pdf"
    )
    
    # Social media links
    st.sidebar.markdown("### Connect with me")
    cols = st.sidebar.columns(4)
    cols[0].markdown("[![LinkedIn](https://img.icons8.com/?size=100&id=xuvGCOXi8Wyg&format=png&color=000000)](https://www.linkedin.com/in/tran-hau-314316255/)")
    cols[1].markdown("[![GitHub](https://img.icons8.com/?size=100&id=12599&format=png&color=000000)](https://github.com)")
    cols[2].markdown("[![Facebook](https://img.icons8.com/?size=100&id=118497&format=png&color=000000)](https://www.facebook.com/hautvph17241)")

# About Me section with Skills
def about_me_with_skills():
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)
    st.markdown('<h1 class="section-title">About Me</h1>', unsafe_allow_html=True)
    
    # Profile section
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.image("https://scontent.fhan17-1.fna.fbcdn.net/v/t39.30808-1/454004006_3477787332520265_3062416834254944162_n.jpg?stp=dst-jpg_s480x480_tt6&_nc_cat=110&ccb=1-7&_nc_sid=e99d92&_nc_eui2=AeF8s7yoXFdnDjEfJAMVaOU2uy-RFL5bx_u7L5EUvlvH-0Apl3xB24VRsIkZZDcvH2evrxU5UPE290TRFAVzSJGZ&_nc_ohc=qi6mnJUeOiMQ7kNvgGSZ8LH&_nc_oc=AdhFzExGdB3Hw9tqKWTCffLHxebrvLedaKFyUdxmYxWrLIAc3dKclPW2Nx17LAR7wxtaulMfq_7UrRwhEe-OqhfP&_nc_zt=24&_nc_ht=scontent.fhan17-1.fna&_nc_gid=AbNYMcz_Jf09LkMoALl0JuB&oh=00_AYE5s1k5H-M0_xqYRm2jP7cOEFxtDC6plGsjYKCbaDdmZg&oe=67D993B3", width=250)
    
    with col2:
        st.markdown('<div class="profile-text">', unsafe_allow_html=True)
        st.markdown('<h2 class="name">Trần Văn Hậu</h2>', unsafe_allow_html=True)
        st.markdown('<p class="title">Tester</p>', unsafe_allow_html=True)
        st.markdown('<p class="bio">Tester có 2 năm kinh nghiệm trong việc đảm bảo chất lượng phần mềm. Nắm vững nghiệp vụ kiểm thử, quy trình sản phẩm, khả năng xây dựng kịch bản kiểm thử chi tiết và thực thi hiệu quả. Am hiểu các công nghệ web cơ bản như HTML, Java và JavaScript.</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Bio section
    st.markdown('<div class="highlight">', unsafe_allow_html=True)
    st.markdown("""
    Tôi là một người kiểm thử tỉ mỉ, luôn tìm kiếm những lỗi tiềm ẩn để đảm bảo chất lượng sản phẩm. 
    Với 2 năm kinh nghiệm trong lĩnh vực kiểm thử phần mềm, tôi đã rèn luyện được khả năng phân tích vấn đề và xây dựng các kịch bản kiểm thử hiệu quả. 
    Tôi luôn hướng đến việc nâng cao chất lượng sản phẩm bằng cách tìm ra những giải pháp tối ưu nhất.
    
    Ngoài công việc, tôi thích khám phá những công nghệ mới, đọc sách về phát triển phần mềm và tận hưởng những buổi cà phê cùng bạn bè.
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Personal details with icons
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="slide-in">', unsafe_allow_html=True)
        st.markdown("### Thông tin chi tiết cá nhân")
        st.markdown("🎂 **Sinh nhật:** 07/04/2002")
        st.markdown("🏠 **Quê quán:** Quảng Ninh")
        st.markdown("📧 **Email:** hautvph17241@gmail.com")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="slide-in">', unsafe_allow_html=True)
        st.markdown("### Ngôn ngữ")
        st.markdown("🇻🇳 **Tiếng Việt:** Bản địa")
        st.markdown("🇺🇸 **Tiếng Anh:** Trung cấp")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Skills section (moved from the original skills function)
    st.markdown('<div class="skills-section">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-title">Skills</h2>', unsafe_allow_html=True)
    
    # Technical skills with animated progress bars
    st.subheader("Technical Skills")
    
    col1, col2 = st.columns(2)
    
    # Technical skills data
    skills_1 = {
        "Manual Testing": 95,
        "Test Case Design": 90,
        "Bug Reporting": 95,
        "Test Management": 85,
        "API Testing": 80
    }
    
    skills_2 = {
        "HTML/CSS": 75,
        "JavaScript": 70,
        "SQL": 80,
        "Selenium": 65,
        "JIRA": 90
    }
    
    # Display skill bars
    for skill, level in skills_1.items():
        col1.markdown(f"**{skill}**")
        col1.markdown(f'<div class="skill-bar" style="width: {level}%;"></div>', unsafe_allow_html=True)
        col1.text(f"{level}%")
    
    for skill, level in skills_2.items():
        col2.markdown(f"**{skill}**")
        col2.markdown(f'<div class="skill-bar" style="width: {level}%;"></div>', unsafe_allow_html=True)
        col2.text(f"{level}%")
    
    # Soft skills with radar chart
    st.subheader("Soft Skills")
    
    soft_skills = {
        'Attention to Detail': 95,
        'Communication': 90,
        'Problem Solving': 85,
        'Teamwork': 90,
        'Time Management': 85
    }
    
    # Create radar chart data
    categories = list(soft_skills.keys())
    values = list(soft_skills.values())
    
    # Normalize values for the chart (0 to 1)
    normalized_values = [v/100 for v in values]
    
    # Create a radar chart
    fig = plt.figure(figsize=(6, 6))
    ax = fig.add_subplot(111, polar=True)
    
    # Set the angles for each category
    angles = np.linspace(0, 2*np.pi, len(categories), endpoint=False).tolist()
    values = normalized_values + [normalized_values[0]]
    angles = angles + [angles[0]]
    categories = categories + [categories[0]]
    
    # Plot the values
    ax.plot(angles, values, 'o-', linewidth=2)
    ax.fill(angles, values, alpha=0.25)
    
    # Set the labels
    ax.set_thetagrids(np.degrees(angles[:-1]), categories[:-1])
    
    # Set the y-axis limits
    ax.set_ylim(0, 1)
    
    # Remove the y-axis labels
    ax.set_yticklabels([])
    
    # Add a title
    plt.title('Soft Skills', size=15, y=1.1)
    
    # Display the chart
    st.pyplot(fig)
    
    # Languages with horizontal bars
    st.subheader("Languages")
    
    languages = {
        "Tiếng Việt": "Native",
        "Tiếng Anh": "Intermediate"
    }
    
    for lang, level in languages.items():
        col1, col2 = st.columns([1, 4])
        col1.write(f"**{lang}**")
        
        if level == "Native":
            col2.progress(100)
        elif level == "Fluent":
            col2.progress(90)
        elif level == "Intermediate":
            col2.progress(60)
        elif level == "Basic":
            col2.progress(30)
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Main function
def main():
    # Display a loading animation
    with st.spinner("Loading CV..."):
        time.sleep(1)
    
    # Show success message
    st.success("CV loaded successfully!")
    
    # Display sidebar
    sidebar()
    
    # Display About Me with Skills
    about_me_with_skills()
    
    # Footer
    st.markdown("---")
    st.markdown("© 2025")

if __name__ == "__main__":
    main()