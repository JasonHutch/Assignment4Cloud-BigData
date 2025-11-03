import streamlit as st
from lib.search_index import SearchIndex
import os

# Initialize session state
if 'search_index' not in st.session_state:
    st.session_state.search_index = SearchIndex()
    st.session_state.indexed = False

st.title("Search Index Tester")
st.write("A simple app to test your search index with word-level positioning")

# Sidebar for indexing documents
st.sidebar.header("Document Indexing")

# Path input for indexing
doc_path = st.sidebar.text_input("Documents Path", value="./documents")

if st.sidebar.button("Index Documents"):
    if os.path.exists(doc_path):
        try:
            st.session_state.search_index = SearchIndex()
            st.session_state.search_index.index_text_documents(doc_path)
            st.session_state.indexed = True

            # Show stats
            num_terms = len(st.session_state.search_index.index)
            st.sidebar.success(f"✓ Indexed successfully!")
            st.sidebar.info(f"Total unique terms: {num_terms}")
        except Exception as e:
            st.sidebar.error(f"Error indexing: {str(e)}")
    else:
        st.sidebar.error(f"Path not found: {doc_path}")

# Main search interface
if st.session_state.indexed:
    st.header("Search")

    # Search type selection
    search_type = st.radio("Search Type", ["Single Term", "Phrase Search"])

    # Search input
    query = st.text_input("Enter your search query:", placeholder="e.g., machine learning")

    if st.button("Search"):
        if query:
            if search_type == "Single Term":
                results = st.session_state.search_index.search(query)

                if results:
                    st.success(f"Found {sum(len(v) for v in results.values())} total matches")

                    for token, positions in results.items():
                        with st.expander(f"Term: '{token}' ({len(positions)} occurrences)"):
                            for pos in positions:
                                st.write(f"- Document: `{pos.doc_id}`, Paragraph: {pos.paragraph_num}, Word Position: {pos.word_position}")
                else:
                    st.warning("No results found")

            else:  # Phrase Search
                results = st.session_state.search_index.search_phrase(query)

                if results:
                    st.success(f"Found {len(results)} phrase matches")

                    for pos in results:
                        st.write(f"- Document: `{pos.doc_id}`, Paragraph: {pos.paragraph_num}, Starting at word position: {pos.word_position}")
                else:
                    st.warning("No phrase matches found")
        else:
            st.warning("Please enter a search query")

    # Display index statistics
    st.header("Index Statistics")
    col1, col2 = st.columns(2)

    with col1:
        st.metric("Unique Terms", len(st.session_state.search_index.index))

    with col2:
        total_positions = sum(len(v) for v in st.session_state.search_index.index.values())
        st.metric("Total Positions", total_positions)

    # Show sample of indexed terms
    if st.checkbox("Show sample of indexed terms"):
        sample_terms = list(st.session_state.search_index.index.keys())[:20]
        st.write("Sample terms (first 20):")
        st.write(", ".join(sorted(sample_terms)))

else:
    st.info("👈 Please index documents using the sidebar first")

    # Instructions
    st.header("How to Use")
    st.markdown("""
    1. **Index Documents**:
       - Enter the path to your text documents in the sidebar
       - Click "Index Documents" to process them

    2. **Search**:
       - Choose between "Single Term" or "Phrase Search"
       - Enter your query and click "Search"
       - View results with document, paragraph, and word positions

    3. **Single Term Search**: Finds all occurrences of each word in your query

    4. **Phrase Search**: Finds exact phrase matches using word positioning
    """)

# Footer
st.markdown("---")
st.caption("Built with Streamlit for Cloud & Big Data Assignment 4")
