from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

from .state import KeywordTargetingState
from .nodes.discover import discover_node
from .nodes.expand import expand_node
from .nodes.normalize import normalize_node
from .nodes.intent import intent_node
from .nodes.cluster import cluster_node
from .nodes.map_pages import map_pages_node
from .nodes.prioritize import prioritize_node
from .nodes.brief import brief_node

def build_keyword_agent(llm, embedding_model):
  """
  سرهم‌بندی خط لوله ترتیبی (Sequential Pipeline) در فریم‌ورک LangGraph
  """
  workflow = StateGraph(KeywordTargetingState)

  workflow.add_node("discover", lambda state: discover_node(state, llm))
  workflow.add_node("expand", lambda state: expand_node(state, llm))
  workflow.add_node("normalize", normalize_node)
  workflow.add_node("intent", lambda state: intent_node(state, llm))
  workflow.add_node("cluster", lambda state: cluster_node(state, embedding_model, llm))
  workflow.add_node("map_pages", map_pages_node)
  workflow.add_node("prioritize", prioritize_node)
  workflow.add_node("brief", lambda state: brief_node(state, llm))

  workflow.set_entry_point("discover")

  workflow.add_edge("discover", "expand")
  workflow.add_edge("expand", "normalize")
  workflow.add_edge("normalize", "intent")
  workflow.add_edge("intent", "cluster")
  workflow.add_edge("cluster", "map_pages")
  workflow.add_edge("map_pages", "prioritize")
  workflow.add_edge("prioritize", "brief")
  workflow.add_edge("brief", END)

  checkpointer = MemorySaver()

  compiled_agent = workflow.compile(checkpointer=checkpointer)
  return compiled_agent