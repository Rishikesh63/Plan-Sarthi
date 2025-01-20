from typing import TypedDict, Annotated
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.message import add_messages
import os
# from dotenv import load_dotenv
# load_dotenv()  

groq_api_key = os.getenv("GROQ_API_KEY")
class AgentState(TypedDict):
    """Contains the state of the agent."""
    messages: Annotated[list, add_messages]
    human_approval: bool  
    human_feedback: str  

llm = ChatGroq(model="llama-3.3-70b-versatile",temperature=0 ,api_key=groq_api_key)

def ai_response(state: AgentState):
    print("Generating AI response...")
    ai_message = llm.invoke(state["messages"])
    print("AI response generated:", ai_message)
    return {
        "messages": state["messages"] + [ai_message],
        "human_approval": False,
        "human_feedback": ""
    }

def human_review(state: AgentState):
    print("Waiting for human review...")
    if state["human_approval"]:
        print("Review approved. Continuing workflow.")
        return {"messages": state["messages"]}
    else:
        print("Review not approved. Feedback:", state["human_feedback"])
        return state 

def should_continue(state: AgentState):
    if state["human_approval"]:
        print("Human approved. Moving to END.")
        return END
    else:
        print("Human feedback provided. Redirecting to generate_response.")
        return "generate_response"  

workflow = StateGraph(AgentState)
workflow.add_node("generate_response", ai_response)
workflow.add_node("review_response", human_review)
workflow.set_entry_point("generate_response")
workflow.add_edge("generate_response", "review_response")
workflow.add_conditional_edges("review_response", should_continue)  

memory = MemorySaver()
graph = workflow.compile(checkpointer=memory, interrupt_after=["generate_response"])
