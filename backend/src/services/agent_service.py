import operator
from typing import Annotated, TypedDict, Union, List

from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, FunctionMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolExecutor

from src.services.rag_service import rag_service

# --- 1. Define Tools ---

@tool
def search_textbook(query: str):
    """Searches the Physical AI textbook for concepts, definitions, and explanations."""
    result = rag_service.query(query)
    # LangGraph expects a string output typically for the agent to parse
    return f"Response: {result['response']}\nSources: {result['sources']}"

@tool
def physics_calculator(expression: str):
    """Evaluates a mathematical expression for physics problems. 
    Use python syntax. e.g. 'numpy.sin(45 * numpy.pi / 180)'."""
    import math
    import numpy
    
    allowed_locals = {"math": math, "numpy": numpy, "np": numpy}
    try:
        # SAFETY: This is a basic eval. In production, use langchain_experimental.utilities.PythonREPL with sandbox.
        result = eval(expression, {"__builtins__": None}, allowed_locals)
        return str(result)
    except Exception as e:
        return f"Error evaluating expression: {e}"

@tool
def quiz_generator(topic: str):
    """Generates a short quiz to test the user's understanding of a specific topic."""
    # We use RAG to get the facts first
    context = rag_service.query(topic)
    return f"CONTEXT: {context['response']}\n\nINSTRUCTION: Create a 3-question multiple choice quiz based on the above context. Format it cleanly."

tools = [search_textbook, physics_calculator, quiz_generator]
tool_executor = ToolExecutor(tools)

# --- 2. Define State ---

class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]

# --- 3. Define Nodes ---

# Initialize LLM with Tools
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
llm_with_tools = llm.bind_functions(tools)

def call_model(state: AgentState):
    messages = state['messages']
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

def call_tool(state: AgentState):
    messages = state['messages']
    last_message = messages[-1]
    
    # "function_call" logic for OpenAI Functions
    if "function_call" not in last_message.additional_kwargs:
        return {"messages": []}

    action = last_message.additional_kwargs["function_call"]
    function_name = action["name"]
    # We need to parse arguments, typically JSON
    import json
    arguments = json.loads(action["arguments"])
    
    # Execute Tool
    response = tool_executor.invoke(
        {"name": function_name, "arguments": arguments}
    )
    
    # Return as FunctionMessage
    function_message = FunctionMessage(content=str(response), name=function_name)
    return {"messages": [function_message]}

def should_continue(state: AgentState):
    messages = state['messages']
    last_message = messages[-1]
    
    # If no function call, stop
    if "function_call" not in last_message.additional_kwargs:
        return "end"
    # Otherwise continue to tool execution
    return "continue"

# --- 4. Build Graph ---

workflow = StateGraph(AgentState)

workflow.add_node("agent", call_model)
workflow.add_node("action", call_tool)

workflow.set_entry_point("agent")

workflow.add_conditional_edges(
    "agent",
    should_continue,
    {
        "continue": "action",
        "end": END
    }
)

workflow.add_edge("action", "agent")

app = workflow.compile()

class AgentService:
    def invoke(self, message: str):
        inputs = {"messages": [HumanMessage(content=message)]}
        result = app.invoke(inputs)
        
        # Extract final response
        last_msg = result['messages'][-1]
        steps = [] 
        
        # Simple extraction of "steps" for UI visualization
        for msg in result['messages']:
            if isinstance(msg, FunctionMessage):
                steps.append(f"Used Tool: {msg.name} -> {msg.content[:50]}...")
                
        return {
            "response": last_msg.content,
            "steps": steps
        }

agent_service = AgentService()
