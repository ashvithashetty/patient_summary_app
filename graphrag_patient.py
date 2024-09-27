import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
# generate KG
from llama_index.core import SimpleDirectoryReader, KnowledgeGraphIndex
from llama_index.core.graph_stores import SimpleGraphStore

from llama_index.llms.openai import OpenAI
from llama_index.core import Settings
from IPython.display import Markdown, display
from llama_index.core import PropertyGraphIndex
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI

# documents = SimpleDirectoryReader("/Users/ashvi/Documents/Canvass/healthcare/pdf_patients").load_data()

# index = PropertyGraphIndex.from_documents(
#     documents,
#     llm=OpenAI(model="gpt-4o", temperature=0),
#     embed_model=OpenAIEmbedding(model_name="text-embedding-3-small"),
#     # show_progress=True,
# )
# # # 

# query_engine = index.as_query_engine(
#     include_text=True,
# )


# Cache the document loading
@st.cache_data
def load_documents():
    return SimpleDirectoryReader("/Users/ashvi/Documents/Canvass/healthcare/pdf_patients").load_data()

documents = load_documents()

# Create index
@st.cache_resource
def create_index(_documents):
    return PropertyGraphIndex.from_documents(
        documents,
        llm=OpenAI(model="gpt-4o", temperature=0),
        embed_model=OpenAIEmbedding(model_name="text-embedding-3-small"),
    )

index = create_index(documents)

# Create query engine
query_engine = index.as_query_engine(include_text=True)




if 'responses' not in st.session_state:
    st.session_state['responses'] = []

if 'selected_patient' not in st.session_state:
    st.session_state['selected_patient'] = None

with st.sidebar:
  st.title('Summarizer and Q/A App')
  patient = st.selectbox(
  "Choose a patient",
  ("Sarah", "John Doe", "Jane", "Robert","Michael", "David"), key="dropdown"
  )
  if st.session_state['selected_patient'] != patient:
        st.session_state['responses'] = []  # Clear previous responses
        st.session_state['question'] = ""  # Clear previous responses
        st.session_state['selected_patient'] = patient 



def main():
    

  st.header("Summarize Patient History")
  col1, col2, col3, col4= st.columns(4)

  if col1.button('Generic Format'):
    response = query_engine.query(f"summarize the history of {patient} for a doctor showing the summary for all 5 years. \
    Provide Past medical history, Past Surgical History, past Hospitalizations, Family History, Social History, Past and Current Medications, Allergies, Past Immunizations. Format the response")
    # st.session_state['responses'].append(str(response))
    st.session_state['responses'] = str(response)

  if col2.button('SOAP Format'):
    response = query_engine.query(f"summarize the history of {patient} for a doctor showing the summary for all 5 years in  SOAP format")
    st.session_state['responses'] = str(response)

  if col3.button('PSATTP Format'):
    response = query_engine.query(f"summarize the history of {patient} for a doctor showing the summary for all 5 years in  PSATTP therapy format")
    st.session_state['responses'] = str(response)

  if col4.button('CHART Format'):
    response = query_engine.query(f"provide the history of {patient} for a doctor showing the summary for all 5 years in  CHART format")
    # st.session_state['responses'].append(str(response))
    st.session_state['responses'] = str(response)


    # st.write(str(response))
  if st.session_state['responses'] :
    st.write(st.session_state['responses'] )

  st.header("Ask questions about the Patient")
  user_question = st.text_input("Type your question here", key="question")
  if st.button("Submit"):
    patient_question = user_question + str(patient)
    response = query_engine.query(patient_question)
    st.write(str(response))
  
    

if __name__ == '__main__':
    main()