import os
import random
from datetime import datetime, timedelta
from typing import List, Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

app = FastAPI(title="StellarRank", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

PORT = int(os.environ.get("COMPANY_PORT", 8000))

# ---------- MOCK DATA ----------
MOCK_KEYWORDS = [
    {"id": 1, "keyword": "best running shoes", "volume": 45000, "difficulty": 78, "current_rank": 12, "target_rank": 1, "search_intent": "commercial"},
    {"id": 2, "keyword": "organic coffee beans online", "volume": 22000, "difficulty": 45, "current_rank": 8, "target_rank": 1, "search_intent": "transactional"},
    {"id": 3, "keyword": "vegan protein powder", "volume": 18000, "difficulty": 62, "current_rank": 15, "target_rank": 3, "search_intent": "commercial"},
    {"id": 4, "keyword": "wireless earbuds noise cancelling", "volume": 34000, "difficulty": 85, "current_rank": 22, "target_rank": 5, "search_intent": "commercial"},
    {"id": 5, "keyword": "sustainable fashion brands", "volume": 12000, "difficulty": 38, "current_rank": 6, "target_rank": 1, "search_intent": "informational"},
    {"id": 6, "keyword": "home gym equipment", "volume": 28000, "difficulty": 70, "current_rank": 10, "target_rank": 2, "search_intent": "commercial"},
    {"id": 7, "keyword": "yoga mat natural rubber", "volume": 9500, "difficulty": 30, "current_rank": 4, "target_rank": 1, "search_intent": "transactional"},
    {"id": 8, "keyword": "LED desk lamp adjustable", "volume": 16000, "difficulty": 55, "current_rank": 18, "target_rank": 5, "search_intent": "commercial"},
]

MOCK_CONTENT = [
    {"id": 1, "title": "10 Best Running Shoes for Marathon Training in 2025", "status": "published", "word_count": 2450, "keyword_focus": "best running shoes", "ai_score": 92, "published_at": "2025-02-15T10:00:00Z", "url": "/blog/best-running-shoes-marathon-training"},
    {"id": 2, "title": "Organic Coffee: A Complete Buyer's Guide", "status": "published", "word_count": 3100, "keyword_focus": "organic coffee beans online", "ai_score": 88, "published_at": "2025-02-12T14:30:00Z", "url": "/blog/organic-coffee-buyers-guide"},
    {"id": 3, "title": "Vegan Protein Powder vs Whey: Which is Better?", "status": "draft", "word_count": 1800, "keyword_focus": "vegan protein powder", "ai_score": 85, "published_at": None, "url": None},
    {"id": 4, "title": "Top 7 Noise Cancelling Wireless Earbuds (Tested)", "status": "published", "word_count": 4200, "keyword_focus": "wireless earbuds noise cancelling", "ai_score": 95, "published_at": "2025-02-10T08:00:00Z", "url": "/blog/top-noise-cancelling-earbuds"},
    {"id": 5, "title": "Sustainable Fashion 101: How to Build an Eco-Friendly Wardrobe", "status": "published", "word_count": 2850, "keyword_focus": "sustainable fashion brands", "ai_score": 91, "published_at": "2025-02-08T11:00:00Z", "url": "/blog/sustainable-fashion-guide"},
    {"id": 6, "title": "Home Gym Equipment Under $500: Budget-Friendly Picks", "status": "draft", "word_count": 2200, "keyword_focus": "home gym equipment", "ai_score": 79, "published_at": None, "url": None},
    {"id": 7, "title": "Best Natural Rubber Yoga Mats Reviewed", "status": "published", "word_count": 1650, "keyword_focus": "yoga mat natural rubber", "ai_score": 87, "published_at": "2025-02-05T09:15:00Z", "url": "/blog/natural-rubber-yoga-mats"},
    {"id": 8, "title": "Adjustable LED Desk Lamps: Features to Look For", "status": "scheduled", "word_count": 1950, "keyword_focus": "LED desk lamp adjustable", "ai_score": 82, "published_at": "2025-03-01T12:00:00Z", "url": None},
]

MOCK_BACKLINKS = [
    {"id": 1, "source_domain": "forbes.com", "target_url": "/blog/best-running-shoes-marathon-training", "domain_authority": 95, "type": "dofollow", "acquired_at": "2025-02-18T16:00:00Z", "anchor_text": "best running shoes for marathon"},
    {"id": 2, "source_domain": "nytimes.com", "target_url": "/blog/organic-coffee-buyers-guide", "domain_authority": 93, "type": "dofollow", "acquired_at": "2025-02-17T12:30:00Z", "anchor_text": "organic coffee beans"},
    {"id": 3, "source_domain": "healthline.com", "target_url": "/blog/sustainable-fashion-guide", "domain_authority": 88, "type": "nofollow", "acquired_at": "2025-02-16T09:00:00Z", "anchor_text": "sustainable fashion"},
    {"id": 4, "source_domain": "techcrunch.com", "target_url": "/blog/top-noise-cancelling-earbuds", "domain_authority": 91, "type": "dofollow", "acquired_at": "2025-02-15T14:45:00Z", "anchor_text": "noise cancelling earbuds review"},
    {"id": 5, "source_domain": "businessinsider.com", "target_url": "/blog/best-running-shoes-marathon-training", "domain_authority": 89, "type": "dofollow", "acquired_at": "2025-02-14T11:20:00Z", "anchor_text": "marathon running shoes"},
    {"id": 6, "source_domain": "wired.com", "target_url": "/blog/top-noise-cancelling-earbuds", "domain_authority": 92, "type": "nofollow", "acquired_at": "2025-02-13T08:30:00Z", "anchor_text": "best wireless earbuds"},
    {"id": 7, "source_domain": "huffpost.com", "target_url": "/blog/sustainable-fashion-guide", "domain_authority": 85, "type": "dofollow", "acquired_at": "2025-02-12T17:00:00Z", "anchor_text": "eco-friendly clothing brands"},
    {"id": 8, "source_domain": "cnet.com", "target_url": "/blog/organic-coffee-buyers-guide", "domain_authority": 87, "type": "dofollow", "acquired_at": "2025-02-11T10:10:00Z", "anchor_text": "best organic coffee"},
]

MOCK_SITE_AUDITS = [
    {"id": 1, "score": 87, "issues_critical": 2, "issues_warning": 8, "issues_info": 15, "pages_crawled": 1240, "crawl_date": "2025-02-20T06:00:00Z", "domain": "example-store.com"},
    {"id": 2, "score": 72, "issues_critical": 5, "issues_warning": 12, "issues_info": 20, "pages_crawled": 890, "crawl_date": "2025-02-13T06:00:00Z", "domain": "example-store.com"},
    {"id": 3, "score": 94, "issues_critical": 0, "issues_warning": 3, "issues_info": 7, "pages_crawled": 2100, "crawl_date": "2025-02-06T06:00:00Z", "domain": "example-store.com"},
    {"id": 4, "score": 65, "issues_critical": 8, "issues_warning": 15, "issues_info": 25, "pages_crawled": 560, "crawl_date": "2025-01-30T06:00:00Z", "domain": "example-store.com"},
    {"id": 5, "score": 81, "issues_critical": 3, "issues_warning": 7, "issues_info": 12, "pages_crawled": 1520, "crawl_date": "2025-01-23T06:00:00Z", "domain": "example-store.com"},
    {"id": 6, "score": 78, "issues_critical": 4, "issues_warning": 10, "issues_info": 18, "pages_crawled": 980, "crawl_date": "2025-01-16T06:00:00Z", "domain": "example-store.com"},
    {"id": 7, "score": 55, "issues_critical": 12, "issues_warning": 18, "issues_info": 30, "pages_crawled": 410, "crawl_date": "2025-01-09T06:00:00Z", "domain": "example-store.com"},
    {"id": 8, "score": 69, "issues_critical": 6, "issues_warning": 14, "issues_info": 22, "pages_crawled": 730, "crawl_date": "2025-01-02T06:00:00Z", "domain": "example-store.com"},
]

MOCK_RANKINGS = [
    {"id": 1, "keyword": "best running shoes", "current_rank": 12, "previous_rank": 15, "change": 3, "serp_features": ["shopping_ads", "featured_snippet"], "date": "2025-02-20"},
    {"id": 2, "keyword": "organic coffee beans online", "current_rank": 8, "previous_rank": 10, "change": 2, "serp_features": ["local_pack"], "date": "2025-02-20"},
    {"id": 3, "keyword": "vegan protein powder", "current_rank": 15, "previous_rank": 18, "change": 3, "serp_features": ["shopping_ads"], "date": "2025-02-20"},
    {"id": 4, "keyword": "wireless earbuds noise cancelling", "current_rank": 22, "previous_rank": 25, "change": 3, "serp_features": ["featured_snippet", "video_carousel"], "date": "2025-02-20"},
    {"id": 5, "keyword": "sustainable fashion brands", "current_rank": 6, "previous_rank": 7, "change": 1, "serp_features": ["knowledge_panel"], "date": "2025-02-20"},
    {"id": 6, "keyword": "home gym equipment", "current_rank": 10, "previous_rank": 12, "change": 2, "serp_features": ["shopping_ads", "related_questions"], "date": "2025-02-20"},
    {"id": 7, "keyword": "yoga mat natural rubber", "current_rank": 4, "previous_rank": 5, "change": 1, "serp_features": ["featured_snippet"], "date": "2025-02-20"},
    {"id": 8, "keyword": "LED desk lamp adjustable", "current_rank": 18, "previous_rank": 20, "change": 2, "serp_features": ["shopping_ads"], "date": "2025-02-20"},
]

MOCK_COMPETITORS = [
    {"id": 1, "domain": "competitor-store-a.com", "organic_traffic": 450000, "keywords_ranking": 12500, "domain_authority": 82, "overlap_score": 0.65, "last_updated": "2025-02-20T06:00:00Z"},
    {"id": 2, "domain": "competitor-store-b.com", "organic_traffic": 320000, "keywords_ranking": 9800, "domain_authority": 76, "overlap_score": 0.58, "last_updated": "2025-02-20T06:00:00Z"},
    {"id": 3, "domain": "competitor-store-c.com", "organic_traffic": 280000, "keywords_ranking": 8200, "domain_authority": 71, "overlap_score": 0.52, "last_updated": "2025-02-20T06:00:00Z"},
    {"id": 4, "domain": "competitor-store-d.com", "organic_traffic": 510000, "keywords_ranking": 14000, "domain_authority": 88, "overlap_score": 0.72, "last_updated": "2025-02-20T06:00:00Z"},
    {"id": 5, "domain": "competitor-store-e.com", "organic_traffic": 190000, "keywords_ranking": 5600, "domain_authority": 62, "overlap_score": 0.41, "last_updated": "2025-02-20T06:00:00Z"},
    {"id": 6, "domain": "competitor-store-f.com", "organic_traffic": 380000, "keywords_ranking": 11000, "domain_authority": 79, "overlap_score": 0.60, "last_updated": "2025-02-20T06:00:00Z"},
    {"id": 7, "domain": "competitor-store-g.com", "organic_traffic": 240000, "keywords_ranking": 7200, "domain_authority": 68, "overlap_score": 0.48, "last_updated": "2025-02-20T06:00:00Z"},
    {"id": 8, "domain": "competitor-store-h.com", "organic_traffic": 460000, "keywords_ranking": 13500, "domain_authority": 84, "overlap_score": 0.68, "last_updated": "2025-02-20T06:00:00Z"},
]

MOCK_RECENT_ACTIVITY = [
    {"id": 1, "type": "keyword_rank_change", "description": "Keyword 'best running shoes' improved by 3 positions", "timestamp": "2025-02-20T14:30:00Z", "severity": "positive"},
    {"id": 2, "type": "backlink_acquired", "description": "New dofollow backlink from forbes.com", "timestamp": "2025-02-18T16:00:00Z", "severity": "positive"},
    {"id": 3, "type": "content_published", "description": "Blog post 'Top 7 Noise Cancelling Wireless Earbuds' published", "timestamp": "2025-02-10T08:00:00Z", "severity": "info"},
    {"id": 4, "type": "site_audit_completed", "description": "Site audit completed with score 87 (2 critical issues)", "timestamp": "2025-02-20T06:00:00Z", "severity": "warning"},
    {"id": 5, "type": "competitor_milestone", "description": "Competitor-store-d.com gained 200 new keywords", "timestamp": "2025-02-19T10:00:00Z", "severity": "negative"},
    {"id": 6, "type": "keyword_added", "description": "5 new keywords added to tracking: 'LED desk lamp', 'smartwatch fitness'", "timestamp": "2025-02-17T09:30:00Z", "severity": "info"},
    {"id": 7, "type": "content_optimized", "description": "Updated content for 'Organic Coffee Buyers Guide' - word count increased to 3100", "timestamp": "2025-02-12T14:30:00Z", "severity": "positive"},
    {"id": 8, "type": "backlink_lost", "description": "Nofollow backlink from huffpost.com dropped", "timestamp": "2025-02-16T11:00:00Z", "severity": "negative"},
]

MOCK_CHART_DATA = {
    "labels": ["Jan 1", "Jan 8", "Jan 15", "Jan 22", "Jan 29", "Feb 5", "Feb 12", "Feb 19"],
    "organic_traffic": [120000, 128000, 135000, 142000, 148000, 155000, 162000, 170000],
    "avg_ranking": [15.2, 14.8, 14.1, 13.5, 12.9, 12.3, 11.7, 11.2],
    "backlinks_count": [340, 365, 390, 420, 455, 490, 520, 555],
    "conversion_rate": [2.1, 2.3, 2.5, 2.7, 2.8, 3.0, 3.2, 3.4],
}

MOCK_STATS = {
    "total_keywords": 12500,
    "ranking_in_top3": 1850,
    "ranking_in_top10": 5200,
    "keywords_on_page1": 3400,
    "avg_domain_authority": 72,
    "total_backlinks": 555,
    "referring_domains": 180,
    "content_pieces": 320,
    "site_audit_score": 87,
    "monthly_traffic": 170000,
    "traffic_growth": 8.5,
    "conversion_rate": 3.4,
}

# ---------- PYDANTIC MODELS ----------
class Keyword(BaseModel):
    id: int
    keyword: str
    volume: int
    difficulty: int
    current_rank: int
    target_rank: int
    search_intent: str

class Content(BaseModel):
    id: int
    title: str
    status: str
    word_count: int
    keyword_focus: str
    ai_score: int
    published_at: Optional[str] = None
    url: Optional[str] = None

class Backlink(BaseModel):
    id: int
    source_domain: str
    target_url: str
    domain_authority: int
    type: str
    acquired_at: str
    anchor_text: str

class SiteAudit(BaseModel):
    id: int
    score: int
    issues_critical: int
    issues_warning: int
    issues_info: int
    pages_crawled: int
    crawl_date: str
    domain: str

class Ranking(BaseModel):
    id: int
    keyword: str
    current_rank: int
    previous_rank: int
    change: int
    serp_features: List[str]
    date: str

class Competitor(BaseModel):
    id: int
    domain: str
    organic_traffic: int
    keywords_ranking: int
    domain_authority: int
    overlap_score: float
    last_updated: str

class Activity(BaseModel):
    id: int
    type: str
    description: str
    timestamp: str
    severity: str

class ChartData(BaseModel):
    labels: List[str]
    organic_traffic: List[int]
    avg_ranking: List[float]
    backlinks_count: List[int]
    conversion_rate: List[float]

class Stats(BaseModel):
    total_keywords: int
    ranking_in_top3: int
    ranking_in_top10: int
    keywords_on_page1: int
    avg_domain_authority: int
    total_backlinks: int
    referring_domains: int
    content_pieces: int
    site_audit_score: int
    monthly_traffic: int
    traffic_growth: float
    conversion_rate: float

# ---------- ENDPOINTS ----------
@app.get("/health")
def health():
    return {"status": "ok", "app": "StellarRank", "version": "1.0.0"}

@app.get("/api/info")
def info():
    return {
        "name": "StellarSEO",
        "app_name": "StellarRank",
        "tagline": "AI-powered SEO for e-commerce brands that want to dominate Google",
        "founded": "2020",
        "team_size": 45,
        "headquarters": "San Francisco, CA",
        "clients_served": 320,
        "industries": ["e-commerce", "retail", "D2C brands"],
        "description": "StellarSEO combines AI-powered keyword research, automated content generation, and intelligent link building to help e-commerce brands achieve top Google rankings. Our platform tracks over 12,000 keywords across 8 major markets.",
        "features": ["Automated Keyword Research", "AI Content Generation", "Backlink Analysis", "Site Audits", "Competitor Tracking", "Rank Tracking", "SERP Analysis"],
        "pricing_tiers": ["Starter - $299/mo", "Growth - $599/mo", "Enterprise - Custom"],
    }

@app.get("/api/metrics")
def metrics():
    return Stats(**MOCK_STATS)

@app.get("/api/stats")
def stats():
    return Stats(**MOCK_STATS)

@app.get("/api/recent-activity")
def recent_activity(limit: int = Query(8, ge=1, le=50)):
    return MOCK_RECENT_ACTIVITY[:limit]

@app.get("/api/chart-data")
def chart_data():
    return ChartData(**MOCK_CHART_DATA)

@app.get("/api/keywords")
def keywords(search: Optional[str] = None, min_volume: Optional[int] = None):
    data = MOCK_KEYWORDS
    if search:
        data = [k for k in data if search.lower() in k["keyword"].lower()]
    if min_volume:
        data = [k for k in data if k["volume"] >= min_volume]
    return data

@app.get("/api/keywords/{keyword_id}")
def keyword_detail(keyword_id: int):
    for k in MOCK_KEYWORDS:
        if k["id"] == keyword_id:
            return k
    raise HTTPException(status_code=404, detail="Keyword not found")

@app.get("/api/content")
def content(status: Optional[str] = None):
    data = MOCK_CONTENT
    if status:
        data = [c for c in data if c["status"] == status]
    return data

@app.get("/api/content/{content_id}")
def content_detail(content_id: int):
    for c in MOCK_CONTENT:
        if c["id"] == content_id:
            return c
    raise HTTPException(status_code=404, detail="Content not found")

@app.get("/api/backlinks")
def backlinks(min_da: Optional[int] = None, link_type: Optional[str] = None):
    data = MOCK_BACKLINKS
    if min_da:
        data = [b for b in data if b["domain_authority"] >= min_da]
    if link_type:
        data = [b for b in data if b["type"] == link_type]
    return data

@app.get("/api/backlinks/{backlink_id}")
def backlink_detail(backlink_id: int):
    for b in MOCK_BACKLINKS:
        if b["id"] == backlink_id:
            return b
    raise HTTPException(status_code=404, detail="Backlink not found")

@app.get("/api/site-audits")
def site_audits():
    return MOCK_SITE_AUDITS

@app.get("/api/site-audits/{audit_id}")
def site_audit_detail(audit_id: int):
    for a in MOCK_SITE_AUDITS:
        if a["id"] == audit_id:
            return a
    raise HTTPException(status_code=404, detail="Site audit not found")

@app.get("/api/rankings")
def rankings(keyword: Optional[str] = None):
    data = MOCK_RANKINGS
    if keyword:
        data = [r for r in data if keyword.lower() in r["keyword"].lower()]
    return data

@app.get("/api/rankings/{ranking_id}")
def ranking_detail(ranking_id: int):
    for r in MOCK_RANKINGS:
        if r["id"] == ranking_id:
            return r
    raise HTTPException(status_code=404, detail="Ranking not found")

@app.get("/api/competitors")
def competitors(min_overlap: Optional[float] = None):
    data = MOCK_COMPETITORS
    if min_overlap:
        data = [c for c in data if c["overlap_score"] >= min_overlap]
    return data

@app.get("/api/competitors/{competitor_id}")
def competitor_detail(competitor_id: int):
    for c in MOCK_COMPETITORS:
        if c["id"] == competitor_id:
            return c
    raise HTTPException(status_code=404, detail="Competitor not found")

@app.post("/api/keywords")
def create_keyword(keyword: Keyword):
    MOCK_KEYWORDS.append(keyword.dict())
    return keyword

@app.post("/api/content")
def create_content(content: Content):
    MOCK_CONTENT.append(content.dict())
    return content

@app.post("/api/backlinks")
def create_backlink(backlink: Backlink):
    MOCK_BACKLINKS.append(backlink.dict())
    return backlink

@app.post("/api/site-audits")
def create_site_audit(audit: SiteAudit):
    MOCK_SITE_AUDITS.append(audit.dict())
    return audit

@app.post("/api/rankings")
def create_ranking(ranking: Ranking):
    MOCK_RANKINGS.append(ranking.dict())
    return ranking

@app.post("/api/competitors")
def create_competitor(competitor: Competitor):
    MOCK_COMPETITORS.append(competitor.dict())
    return competitor

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=PORT, reload=True)