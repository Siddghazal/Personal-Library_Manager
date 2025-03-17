import streamlit as st
import json

# File to store library data
LIBRARY_FILE = "library.json"

def load_library():
    try:
        with open(LIBRARY_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_library(library):
    with open(LIBRARY_FILE, "w") as file:
        json.dump(library, file, indent=4)

def add_book(title, author, year, genre, read):
    library = load_library()
    book = {"title": title, "author": author, "year": int(year), "genre": genre, "read": read.lower() == "yes"}
    library.append(book)
    save_library(library)

def remove_book(title):
    library = load_library()
    new_library = [book for book in library if book["title"].lower() != title.lower()]
    if len(new_library) < len(library):
        save_library(new_library)
        return True
    return False

def search_books_by_title(title):
    library = load_library()
    return [book for book in library if title.lower() in book["title"].lower()]

def search_books_by_author(author):
    library = load_library()
    return [book for book in library if author.lower() in book["author"].lower()]

def display_all_books():
    return load_library()

def get_statistics():
    library = load_library()
    total_books = len(library)
    read_books = sum(1 for book in library if book["read"])
    read_percentage = (read_books / total_books * 100) if total_books > 0 else 0
    return total_books, read_percentage

def main():
    st.set_page_config(page_title="Personal Library Manager", page_icon="📚", layout="centered")
    st.title("📚 Welcome to your Personal Library Manager!")
    st.sidebar.header("📖 Menu")
    
    menu = [
        "📖 Add a book",
        "❌ Remove a book",
        "🔍 Search for a book",
        "📚 Display all books",
        "📊 Display statistics",
        "🚪 Exit"
    ]
    choice = st.sidebar.radio("Select an option:", menu)

    if choice == "📖 Add a book":
        st.subheader("➕ Add a Book")
        title = st.text_input("📌 Enter the book title:")
        author = st.text_input("✍️ Enter the author:")
        year = st.number_input("📅 Enter the publication year:", min_value=0, max_value=2100, step=1)
        genre = st.text_input("🏷️ Enter the genre:")
        read = st.radio("📖 Have you read this book?", ["yes", "no"], horizontal=True)
        if st.button("📥 Add Book", use_container_width=True):
            add_book(title, author, year, genre, read)
            st.success("✅ Book added successfully!")
    
    elif choice == "❌ Remove a book":
        st.subheader("🗑 Remove a Book")
        title = st.text_input("Enter the title of the book to remove:")
        if st.button("🗑 Remove Book", use_container_width=True):
            if remove_book(title):
                st.success(f"✅ Book '{title}' removed successfully!")
            else:
                st.warning(f"⚠ Book '{title}' not found!")
    
    elif choice == "🔍 Search for a book":
        st.subheader("🔍 Search for a Book")
        search_option = st.radio("Search by:", ["Title", "Author"], horizontal=True)
        query = st.text_input("Enter your search query:")
        if st.button("🔎 Search", use_container_width=True):
            results = search_books_by_title(query) if search_option == "Title" else search_books_by_author(query)
            if results:
                st.write("### Matching Books:")
                for idx, book in enumerate(results, start=1):
                    st.write(f"{idx}. **{book['title']}** by *{book['author']}* ({book['year']}) - {book['genre']} - {'✅ Read' if book['read'] else '❌ Unread'}")
            else:
                st.warning("⚠ No matching books found.")
    
    elif choice == "📚 Display all books":
        st.subheader("📚 Your Library")
        library = display_all_books()
        if library:
            for idx, book in enumerate(library, start=1):
                st.write(f"{idx}. **{book['title']}** by *{book['author']}* ({book['year']}) - {book['genre']} - {'✅ Read' if book['read'] else '❌ Unread'}")
        else:
            st.info("ℹ No books in your library.")
    
    elif choice == "📊 Display statistics":
        st.subheader("📊 Library Statistics")
        total, percentage = get_statistics()
        st.write(f"📚 **Total books:** {total}")
        st.write(f"📖 **Percentage read:** {percentage:.2f}%")
    
    elif choice == "🚪 Exit":
        st.success("💾 Library saved to file. Goodbye!")

if __name__ == "__main__":
    main()
