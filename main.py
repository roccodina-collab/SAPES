import os
from typing import TypedDict, Annotated, Sequence
import operator

from langchain_groq import ChatGroq
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langgraph.graph import StateGraph, END

# 1. Validar la clau d'API
if "GROQ_API_KEY" not in os.environ:
    print("❌ Error: Falta la clau GROQ_API_KEY.")
    print("Executa a PowerShell: $env:GROQ_API_KEY='la_teva_clau'")
    exit(1)

# 2. Carregar la base de dades vectorial
embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
vector_db = Chroma(
    persist_directory="./data/chromadb",
    embedding_function=embedding_function,
    collection_name="project_knowledge"
)

# 3. Inicialitzar el model Llama 3.3 via Groq
llm = ChatGroq(
    model="openai/gpt-oss-120b",
    groq_api_key=os.environ["GROQ_API_KEY"],
    temperature=0.2
)

# 4. Definició de l'estat i el graf de LangGraph
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    context: str

def retrieve_context(state: AgentState):
    last_query = state["messages"][-1].content
    docs = vector_db.similarity_search(last_query, k=3)
    context_str = "\n---\n".join([doc.page_content for doc in docs]) if docs else "Sense context."
    return {"context": context_str}

def generate_response(state: AgentState):
    system_prompt = SystemMessage(content=(
        "Ets l'assistent d'IA del projecte SAPES. "
        "Respon a l'usuari utilitzant exclusivament la següent informació dels fitxers del projecte:\n\n"
        f"--- CONTEXT ---\n{state['context']}\n---------------\n"
        "Si la informació no apareix al context, indica que no està documentada a la carpeta SAPES."
    ))
    response = llm.invoke([system_prompt] + list(state["messages"]))
    return {"messages": [response]}

workflow = StateGraph(AgentState)
workflow.add_node("retrieve", retrieve_context)
workflow.add_node("generate", generate_response)
workflow.set_entry_point("retrieve")
workflow.add_edge("retrieve", "generate")
workflow.add_edge("generate", END)

app = workflow.compile()

# 5. Bucle interactiu per a la terminal
print("\n🤖 Agent d'IA de SAPES a punt! Escriu la teva pregunta (o 'sortir' per tancar):\n")

while True:
    user_input = input("Tu: ")
    if user_input.lower() in ["sortir", "exit", "quit"]:
        print("Fins aviat!")
        break
    if not user_input.strip():
        continue

    inputs = {"messages": [HumanMessage(content=user_input)]}
    result = app.invoke(inputs)
    
    print(f"\nAgent: {result['messages'][-1].content}\n")
    print("-" * 60)