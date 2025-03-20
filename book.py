import streamlit as st
import requests
import time
import re
import datetime

API_URL = "http://127.0.0.1:8000"

# Hàm tải danh sách sách
def fetch_books():
    try:
        response = requests.get(f"{API_URL}/books")
        response.raise_for_status()
        st.session_state.books = response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Lỗi khi tải danh sách sách: {e}")
        st.session_state.books = []

# Hàm kiểm tra chỉ nhập chữ
def is_valid_text(text):
    return bool(re.fullmatch(r"[A-Za-zÀ-Ỹà-ỹ\s]+", text))

# Hàm cập nhật sách
def update_book(book_id, title, author, year):
    try:
        payload = {"title": title, "author": author, "published_year": year}
        response = requests.post(f"{API_URL}/books/{book_id}/update", json=payload)
        response.raise_for_status()
        
        st.success("✅ Cập nhật sách thành công!")
        fetch_books()  # Reload danh sách sau khi cập nhật
    except requests.exceptions.RequestException as e:
        st.error(f"Lỗi khi cập nhật sách: {e}")

# Hàm xóa sách
def delete_book(book_id):
    try:
        response = requests.post(f"{API_URL}/books/{book_id}/delete")
        response.raise_for_status()

        st.session_state["delete_success"] = True
        st.session_state["confirm_delete_id"] = None  # Ẩn modal
        fetch_books()  # Reload danh sách
    except requests.exceptions.RequestException as e:
        st.error(f"Lỗi khi xóa sách: {e}")

# Chỉ gọi API khi chưa có dữ liệu
if "books" not in st.session_state:
    fetch_books()

st.title("📚 Quản lý Sách")

# Hiển thị thông báo xóa thành công trong 5 giây
if st.session_state.get("delete_success", False):
    st.success("🗑️ Xóa sách thành công! Trang sẽ tự động cập nhật.")
    time.sleep(5)
    st.session_state["delete_success"] = False  # Ẩn thông báo

# Bộ lọc tìm kiếm
search_query = st.text_input("🔍 Tìm kiếm theo tiêu đề", "")

# Lọc danh sách sách
books = st.session_state.books
if search_query:
    books = [book for book in books if search_query.lower() in book["title"].lower()]

# Hiển thị danh sách sách
if books:
    for book in books:
        col1, col2, col3, col4, col5, col6 = st.columns([1, 3, 3, 2, 2, 2])
        col1.write(book["id"])
        col2.write(book["title"])
        col3.write(book["author"])
        col4.write(book["published_year"])

        if col5.button("✏️ Sửa", key=f"edit_{book['id']}"):
            st.session_state[f"editing_{book['id']}"] = True

        if col6.button("🗑️ Xóa", key=f"delete_{book['id']}"):
            st.session_state["confirm_delete_id"] = book["id"]

        if st.session_state.get(f"editing_{book['id']}", False):
            st.subheader("📝 Chỉnh sửa sách")
            new_title = st.text_input("Tiêu đề", book["title"], key=f"title_{book['id']}")
            new_author = st.text_input("Tác giả", book["author"], key=f"author_{book['id']}")
            new_date = st.date_input("📅 Ngày xuất bản", datetime.date(book["published_year"], 1, 1), key=f"year_{book['id']}")

            new_year = new_date.year

            title_valid = is_valid_text(new_title)
            author_valid = is_valid_text(new_author)

            if not title_valid:
                st.error("⚠️ Tiêu đề chỉ được chứa chữ cái và khoảng trắng.")

            if not author_valid:
                st.error("⚠️ Tác giả chỉ được chứa chữ cái và khoảng trắng.")

            if st.button("💾 Lưu thay đổi", key=f"save_{book['id']}") and title_valid and author_valid:
                update_book(book["id"], new_title, new_author, new_year)
                st.session_state[f"editing_{book['id']}"] = False  # Ẩn form sau khi cập nhật

# --- Xác nhận xóa (Modal giả lập) ---
if "confirm_delete_id" in st.session_state and st.session_state["confirm_delete_id"] is not None:
    book_id = st.session_state["confirm_delete_id"]
    st.warning("⚠️ Bạn có chắc chắn muốn xóa sách này?")
    col_confirm1, col_confirm2 = st.columns([1, 1])

    if col_confirm1.button("✅ Đồng ý"):
        delete_book(book_id)

    if col_confirm2.button("❌ Hủy bỏ"):
        st.session_state["confirm_delete_id"] = None  # Ẩn modal

# --- Nút Thêm Mới ---
st.markdown("---")
if "show_add_form" not in st.session_state:
    st.session_state.show_add_form = False

if st.button("➕ Thêm mới"):
    st.session_state.show_add_form = not st.session_state.show_add_form

if st.session_state.show_add_form:
    st.subheader("📌 Nhập thông tin sách mới")

    title = st.text_input("Tiêu đề", key="new_title")
    author = st.text_input("Tác giả", key="new_author")
    published_date = st.date_input("📅 Ngày xuất bản", datetime.date.today())

    year = published_date.year

    title_valid = is_valid_text(title)
    author_valid = is_valid_text(author)

    if not title_valid:
        st.error("⚠️ Tiêu đề chỉ được chứa chữ cái và khoảng trắng.")

    if not author_valid:
        st.error("⚠️ Tác giả chỉ được chứa chữ cái và khoảng trắng.")

    if st.button("📚 Lưu sách") and title_valid and author_valid:
        try:
            response = requests.post(f"{API_URL}/books", json={"title": title, "author": author, "published_year": year})
            response.raise_for_status()
            st.success("📚 Thêm sách thành công!")
            fetch_books()  # Reload danh sách
            st.session_state.show_add_form = False  # Ẩn form
        except requests.exceptions.RequestException as e:
            st.error(f"Lỗi khi thêm sách: {e}")
