from pathlib import Path
from collections import Counter
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from dotenv import load_dotenv
from openai import OpenAI
import os
import ast


# Load environment variables from .env file
load_dotenv()
apikey = os.environ["OPENAI_API_KEY"]

# Initialize OpenAI client
client = OpenAI(api_key=apikey)

# 1. Load and split PDF
pdf_path = Path(__file__).parent / "node_js_sample.pdf"
loader = PyPDFLoader(pdf_path)
docs = loader.load()

# Split document into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
)
split_docs = text_splitter.split_documents(documents=docs)

# 2. Create an embedder
embedder = OpenAIEmbeddings(
    model="text-embedding-3-large",
    api_key=apikey
)

# Only run the below once to insert data into Qdrant
# vector_store = QdrantVectorStore.from_documents(
#     documents=split_docs,
#     embedding=embedder,
#     url="http://localhost:6333",
#     collection_name="learning_node_js",
# )
# vector_store.add_documents(documents=split_docs)

# Connect to existing Qdrant vector store
retriever = QdrantVectorStore.from_existing_collection(
    url="http://localhost:6333",
    collection_name="learning_node_js",
    embedding=embedder,
)

print("📄 PDF Ingestion Complete!\n")

# 3. Take user question
user_query = input("Ask a question about Node.js: ")

# 4. Query Expansion Prompt
augmentation_prompt = f"""Generate 3 semantically different variations of this question for better retrieval:
"{user_query}"
Only return a Python list of 3 strings.

Example: ["hi", "hello", "how are you"]
"""

# Call OpenAI to expand query
query_expansion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": augmentation_prompt}]
)

# 5. Parse string output to actual Python list
raw_response = query_expansion.choices[0].message.content.replace("`", "")
similar_queries = ast.literal_eval(raw_response)

print("🔍 Expanded Queries:\n", similar_queries)

# 6. Search for relevant docs for each variation
all_relevant_docs = []

for q in similar_queries:
    docs = retriever.similarity_search(query=q, k=3)
    all_relevant_docs.extend(docs)


# 7. Deduplicate by content
unique_docs = list({doc.page_content: doc for doc in all_relevant_docs}.values())
context = "\n\n".join(doc.page_content for doc in unique_docs)

# 8. Send to OpenAI for final answer generation
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant knowledgeable in Node.js."},
        {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {user_query}"}
    ]
)

# 9. Display response
answer = response.choices[0].message.content.replace("*", "").replace("`", "").replace("#", "")
print("\n💡 Answer:\n", answer)
