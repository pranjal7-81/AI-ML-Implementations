import json
import os
import sys
import boto3
import streamlit as st

## we will be using titan model to generate embeddings 

from langchain_aws import BedrockEmbeddings
from langchain_aws import BedrockLLM

## data ingestion

import numpy as np
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFDirectoryLoader

## vector embeddings

from langchain_community.vectorstores import FAISS

##LLM models

from langchain_core.prompts import PromptTemplate
from langchain_classic.chains import RetrievalQA

## Bedrock client


bedrock = boto3.client(
    service_name='bedrock-runtime'
)

bedrock_embeddings = BedrockEmbeddings(
    model_id="amazon.titan-embed-text-v2:0",
    client=bedrock
)


## data ingestion

def data_ingestion():

    loader = PyPDFDirectoryLoader("data")

    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100
    )

    docs = text_splitter.split_documents(documents)

    return docs


## vector embeddings and vector store creation

def vector_store(docs):

    vectorestore = FAISS.from_documents(
        docs,
        bedrock_embeddings
    )

    vectorestore.save_local("faiss_index")

    return vectorestore


## load existing vector store

def load_vector_store():

    vectorestore = FAISS.load_local(
        "faiss_index",
        bedrock_embeddings,
        allow_dangerous_deserialization=True
    )

    return vectorestore


## LLM models

def get_claude_llm():

    llm = BedrockLLM(
        model_id="anthropic.claude-v2",
        client=bedrock,
        model_kwargs={
            "max_tokens_to_sample": 512
        }
    )

    return llm


def get_llama2_llm():

    llm = BedrockLLM(
        model_id="meta.llama3-8b-instruct-v1:0",
        client=bedrock,
        model_kwargs={
            "max_gen_len": 512
        }
    )

    return llm


prompt_template = """
Human: Use the following pieces of context to provide a concise answer to the question at the end.

Give a clear and detailed explanation of around 250 words.

If you don't know the answer from the provided context, just say that you don't know.
Do not make up an answer.

<context>
{context}
</context>

Question: {question}

Assistant:
"""


PROMPT = PromptTemplate(
    template=prompt_template,
    input_variables=["context", "question"]
)


def get_response_llm(llm, vectorstore_faiss, query):

    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore_faiss.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 3}
        ),
        return_source_documents=True,
        chain_type_kwargs={
            "prompt": PROMPT
        }
    )

    answer = qa.invoke({
        "query": query
    })

    return answer["result"], answer["source_documents"]


# ============================================================
# STREAMLIT APP
# ============================================================

st.set_page_config(
    page_title="PDF RAG Chatbot",
    page_icon="📚"
)

st.title("📚 PDF Question Answering System")

st.write(
    "Ask questions from the PDF documents stored in the data folder."
)


## Create vector store

if st.button("Create Vector Store"):

    with st.spinner("Reading and processing PDFs..."):

        docs = data_ingestion()

        if len(docs) == 0:

            st.error("No PDF files found in the data folder.")

        else:

            vector_store(docs)

            st.success(
                f"Vector store created successfully! "
                f"{len(docs)} chunks created."
            )


## Question input

query = st.text_input(
    "Ask a question:"
)


## Ask question

if st.button("Ask"):

    if query.strip() == "":

        st.warning("Please enter a question.")

    elif not os.path.exists("faiss_index"):

        st.error(
            "Vector store does not exist. "
            "Please click 'Create Vector Store' first."
        )

    else:

        with st.spinner("Generating answer..."):

            try:

                ## Load existing FAISS vector store

                vectorstore_faiss = load_vector_store()


                ## Select LLM

                llm = get_llama2_llm()


                ## Get response

                answer, source_documents = get_response_llm(
                    llm,
                    vectorstore_faiss,
                    query
                )


                ## Display answer

                st.subheader("Answer")

                st.write(answer)


                ## Display sources

                st.subheader("Sources")

                for i, document in enumerate(source_documents):

                    st.write(f"Source {i + 1}")

                    st.write(
                        document.page_content[:500]
                    )

                    if "source" in document.metadata:

                        st.caption(
                            f"File: {document.metadata['source']}"
                        )


            except Exception as e:

                st.error(
                    f"Error: {str(e)}"
                )