import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt 

st.title("Dashboard dữ liệu nhân khẩu học");

uploaded_file = st.file_uploader("Chọn file dữ liệu", type=["csv", "xlsx"])
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file);
    st.write(df.head(20))
    st.subheader("Thông Tin Tổng Quan")
    st.subheader("Lọc Dữ Liệu")
    columns = df.columns.tolist()
    selected_column = st.selectbox("Chọn cột để lọc:", columns)
    unique_values = df[selected_column].unique()
    selected_value = st.selectbox("Chọn giá trị:", unique_values)
    filtered_df = df[df[selected_column] == selected_value]

    st.write(filtered_df)
    st.subheader("Vẽ Biểu Đồ")
    x_column = st.selectbox("Chọn cột cho trục X:", columns, key="x_axis")
    y_column = st.selectbox("Chọn cột cho trục Y:", columns, key="y_axis")
    if st.button("Vẽ Biểu Đồ"):
        fig, ax = plt.subplots(figsize=(50, 50))

        ax.plot(df[x_column], df[y_column], marker='o')
        
        ax.set_title(f"{y_column} theo {x_column} cho {selected_column}={columns}")
        ax.set_xlabel(x_column)
        ax.set_ylabel(y_column)
        
        st.pyplot(fig)
else:
    st.write("Đang chờ tải file lên...")