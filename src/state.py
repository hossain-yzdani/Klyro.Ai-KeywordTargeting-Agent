from typing import TypedDict, List, Dict, Literal, Optional
from pydantic import BaseModel, Field

class KeywordItem(BaseModel):
  raw: str
  normalized: str
  intent: Optional[Literal[
    "Informational", 
    "Commercial", 
    "Transactional", 
    "Navigational"
  ]] = None
  cluster_id: Optional[int] = None
  cluster_name: Optional[str] = None
  search_volume: int = 100
  difficulty: int = 30
  score: float = 0.0
  
class ClusterSummary(BaseModel):
  id: int
  name: str
  keywords: List[str]
  dominant_intent: str
  recommended_page_type: Literal[
    "Pillar", 
    "Cluster", 
    "Sub-Page"
  ]
  target_page: Optional[str] = None
  cannibalization_risk: bool = False
  competing_pages: List[str] = []
  priority_score: float = 0.0
  
class ContentBrief(BaseModel):
  cluster_name: str
  page_type: str
  seo_title: str
  h1: str
  meta_description: str
  headings_structure: List[str]
  faqs: List[Dict[str, str]]
  internal_linking_suggestions: List[str]
  
class KeywordTargetingState(TypedDict):
  domain: str
  market: str
  target_theme: str
  existing_pages: List[Dict[str, str]]
  raw_keywords: List[str]
  processed_keywords: List[KeywordItem]
  clusters: List[ClusterSummary]
  briefs: List[ContentBrief]
  logs: List[str]