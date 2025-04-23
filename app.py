import streamlit as st
import fitz
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import ConversationalRetrievalChain
from langchain_community.llms import Ollama
from langchain.memory import ConversationBufferMemory

class BookChat:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        self.vector_store = None
        self.conversation_chain = None

    def process_pdf(self, file_path: str) -> bool:
        try:
            doc = fitz.open(file_path)
            text = ""
            for page in doc:
                text += page.get_text()
            doc.close()

            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200,
                length_function=len
            )
            chunks = text_splitter.split_text(text)

            self.vector_store = Chroma.from_texts(
                chunks,
                self.embeddings,
                collection_name="book_chunks"
            )

            self.conversation_chain = ConversationalRetrievalChain.from_llm(
                llm=Ollama(model="llama2"),
                retriever=self.vector_store.as_retriever(search_kwargs={"k": 3}),
                memory=ConversationBufferMemory(
                    memory_key="chat_history",
                    return_messages=True
                )
            )

            return True
        except Exception as e:
            st.error(f"Error processing PDF: {str(e)}")
            return False

    def ask_question(self, question: str) -> str:
        try:
            if not self.conversation_chain:
                return "Please process a PDF file first."
            result = self.conversation_chain({"question": question})
            return result["answer"]
        except Exception as e:
            return f"Error generating response: {str(e)}"

def main():
    st.title("📚 Book Chat")
    
    if 'chat' not in st.session_state:
        st.session_state.chat = BookChat()
    if 'pdf_processed' not in st.session_state:
        st.session_state.pdf_processed = False

    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

    if uploaded_file and not st.session_state.pdf_processed:
        with open(uploaded_file.name, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        if st.button("Process PDF"):
            with st.spinner("Processing PDF..."):
                if st.session_state.chat.process_pdf(uploaded_file.name):
                    st.session_state.pdf_processed = True
                    st.success("PDF processed successfully!")

    if st.session_state.pdf_processed:
        question = st.text_input("Ask a question about the book:")
        if question:
            response = st.session_state.chat.ask_question(question)
            st.write(response)

if __name__ == "__main__":
    main()