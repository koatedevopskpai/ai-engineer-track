# agent.py #
from typing import TypedDict
from langgraph.graph import StateGraph, END
from langchain_ollama import ChatOllama

llm = ChatOllama(model="llama3.2", temperature=0)


class State(TypedDict):
    query: str
    tier: str
    answer: str
    confidence: float


def triage(state: State):
    prompt = (
        f"Classify this support ticket as one of: L1, L2, L3. Ticket: {state['query']}"
    )
    return {"tier": llm.invoke(prompt).content.strip()}


def resolve(state: State):
    # In the real build this calls Phase 2 retrieval for grounded context.
    prompt = f"Answer this support question concisely. Ticket: {state['query']}"
    return {"answer": llm.invoke(prompt).content}


def qa(state: State):
    # Simple heuristic confidence; the real build uses RAGAS scoring.
    conf = min(1.0, 0.5 + 0.2 * len(state["answer"].split()))
    return {"confidence": conf}


def route_after_qa(state: State) -> str:
    return "escalate" if state["confidence"] < 0.7 else "done"


g = StateGraph(State)
g.add_node("triage", triage)
g.add_node("resolve", resolve)
g.add_node("qa", qa)
g.set_entry_point("triage")
g.add_edge("triage", "resolve")
g.add_edge("resolve", "qa")
g.add_conditional_edges("qa", route_after_qa, {"done": END, "escalate": END})
app = g.compile()

result = app.invoke({"query": "How do I reset my password?"})
print(result)
