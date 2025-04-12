import streamlit as st
import os
import json


data_file = 'library.txt'

def load_library():
    if os.path.exists(data_file):
        with open(data_file, 'r') as file:
            return json.load(file)
    return []

def save_library(library):
    with open(data_file, 'w') as file:
        json.dump(library, file, indent=4)

#app header
st.set_page_config(page_title="📚 Library Manager", layout="wide")

st.title("📚 Library Manager")
st.markdown("**Manage your personal book collection effortlessly!**")
st.divider()


#sidebar navigation

st.sidebar.header("📖 Menu")
option = st.sidebar.radio("Select an Action ", ["📌 Add Book", "❌ Remove Book", "🔍 Search", "📚 View All", "📊 Statistics"])




if option == "📌 Add Book":
    st.subheader("➕ Add a New Book")
    with st.expander("📌 Click to Add a New Book", expanded=True):
        col1, col2 = st.columns(2)

        with col1:
            title = st.text_input("📖 Book Title")
            author = st.text_input("✍️ Author")
            year = st.text_input("📅 Publication Year")

        with col2:
            genre = st.text_input("📂 Genre")
            read = st.checkbox("✅ Mark as Read")

        if st.button("🚀 Add Book"):
            if title and author:
                library = load_library()
                new_book = {"title": title, "author": author, "year": year, "genre": genre, "read": read}
                library.append(new_book)
                save_library(library)
                st.success(f'🎉 **"{title}"** added successfully!')
            else:
                st.warning("⚠️ Title and Author are required fields.")





elif option == "❌ Remove Book":
    st.subheader("🗑 Remove a Book")
    library = load_library()
    
    if library:
        book_titles = [book["title"] for book in library]
        book_to_remove = st.selectbox("📖 Select a book to remove:", book_titles)

        if st.button("🗑 Remove"):
            library = [book for book in library if book["title"] != book_to_remove]
            save_library(library)
            st.success(f'❌ **"{book_to_remove}"** removed successfully!')
    else:
        st.warning("📭 No books in the library.")





elif option == "🔍 Search":
    st.subheader("🔎 Search Books in Library")
    
    search_query = st.text_input("🔍 Enter book title or author:")
    
    if st.button("Search"):
        library = load_library()
        results = [book for book in library if search_query.lower() in book["title"].lower() or search_query.lower() in book["author"].lower()]
        
        if results:
            for book in results:
                st.write(f'📖 **{book["title"]}** by {book["author"]} ({book["year"]}) - {book["genre"]} - {"✅ Read" if book["read"] else "❌ Not Read"}')
        else:
            st.warning("⚠️ No matching books found!")




elif option == "📊 Statistics":
    st.subheader("📊 Library Statistics")

    library = load_library()
    total_books = len(library)
    read_books = len([book for book in library if book["read"]])
    unread_books = total_books - read_books
    percentage_read = (read_books / total_books) * 100 if total_books > 0 else 0

    st.metric(label="📚 Total Books", value=total_books)
    st.metric(label="✅ Books Read", value=read_books)
    st.metric(label="📖 Books Unread", value=unread_books)

    st.progress(percentage_read / 100)
    st.write(f"📈 **{percentage_read:.2f}%** books read")

