import os
from typing import TypedDict, Annotated, Sequence
import operator
from langchain_groq import ChatGroq
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langgraph.graph import StateGraph, END
from src.rag import query_knowledge_base

# 1. Configurar el Model via Groq API
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    groq_api_key=os.getenv("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"),
    temperature=0.1
)

# 2. Definir l'estat compartit del graf
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    context: str

# 3. Nodes del Graf
def retrieve_context_node(state: AgentState):
    """Llegeix la darrera petició de l'usuari i cerca context a ChromaDB."""
    last_message = state["messages"][-1].content
    context = query_knowledge_base(last_message)
    return {"context": context}

def generate_response_node(state: AgentState):
    """Agent principal que genera la resposta basant-se en el context i les regles."""
    system_prompt = SystemMessage(content=(
        "Ets un assistent tècnic d'IA per al projecte. "
        "Utilitza el següent context del repositori per respondre de forma senzilla i precisa:\n"
        f"CONTEXT:\n{state['context']}"
    ))
    
    messages = [system_prompt] + state["messages"]
    response = llm.invoke(messages)
    return {"messages": [response]}

# 4. Construir el Graf de LangGraph
workflow = StateGraph(AgentState)

# Afegir nodes
workflow.add_node("retrieve_context", retrieve_context_node)
workflow.add_node("generate_response", generate_response_node)

# Definir el flux (arestes)
workflow.set_entry_point("retrieve_context")
workflow.add_edge("retrieve_context", "generate_response")
workflow.add_edge("generate_response", END)

# Compilar el graf
app = workflow.compile()