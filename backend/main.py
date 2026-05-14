import os
import uvicorn
from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict
from datetime import datetime, timedelta

PORT = int(os.environ.get("COMPANY_PORT", 8000))

app = FastAPI(title="StellarRank", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- Pydantic Models ----------
class HealthResponse(BaseModel):
    status: str
    app: str
    version: str

class CompanyInfo(BaseModel):
    name: str
    tagline: str
    founded: int
    team_size: int
    location: str
    mission: str

class MetricsResponse(BaseModel):
    monthly_active_users: int
    total_clients: int
    average_rank_improvement: float
    total_keywords_monitored: int
    monthly_revenue_usd: float

class StatItem(BaseModel):
    name: str
    value: float

class StatsResponse(BaseModel):
    total_keywords: int
    total_content_generated: int
    total_backlinks: int
    average_position: float
    traffic_gain_percent: float

class ActivityItem(BaseModel):
    timestamp: datetime
    activity_type: str
    project: str
    details: str

class RecentActivityResponse(BaseModel):
    activities: List[ActivityItem]

class ChartDataPoint(BaseModel):
    period: str
    value: float

class ChartDataResponse(BaseModel):
    traffic_growth: List[ChartDataPoint]
    rank_distribution: List[ChartDataPoint]

class KeywordItem(BaseModel):
    keyword: str
    current_rank: int
    difficulty: int = Field(..., description="SEO difficulty score 0-100")
    search_volume: int
    last_updated: datetime

class NewKeywordRequest(BaseModel):
    keyword: str
    target_url: str

class ContentItem(BaseModel):
    id: int
    title: str
    status: str
    generated_at: datetime
    url: str

class NewContentRequest(BaseModel):
    title: str
    brief: str

class LinkItem(BaseModel):
    source_domain: str
    target_url: str
    authority_score: float
    acquired_at: datetime

class NewLinkRequest(BaseModel):
    source_domain: str
    target_url: str

# ---------- Mock Data ----------
company_info = CompanyInfo(
    name="StellarSEO",
    tagline="AI-Powered SEO for E‑Commerce Brands",
    founded=2022,
    team_size=48,
    location="San Francisco, CA",
    mission="Help e‑commerce brands rank #1 on Google through automated keyword research, content generation, and link building."
)

metrics_data = MetricsResponse(
    monthly_active_users=1245,
    total_clients=342,
    average_rank_improvement=2.7,
    total_keywords_monitored=87456,
    monthly_revenue_usd=158732.40
)

stats_data = StatsResponse(
    total_keywords=84231,
    total_content_generated=5274,
    total_backlinks=19384,
    average_position=3.9,
    traffic_gain_percent=27.5
)

recent_activities = [
    ActivityItem(
        timestamp=datetime.utcnow() - timedelta(hours=2),
        activity_type="Keyword Research",
        project="EcoGear Sneakers",
        details="Added 25 new long‑tail keywords."
    ),
    ActivityItem(
        timestamp=datetime.utcnow() - timedelta(hours=5),
        activity_type="Content Generation",
        project="EcoGear Sneakers",
        details="Generated blog post 'Top 10 Sustainable Sneakers'."
    ),
    ActivityItem(
        timestamp=datetime.utcnow() - timedelta(days=1, hours=3),
        activity_type="Link Building",
        project="EcoGear Sneakers",
        details="Secured 5 backlinks from authority fashion sites."
    ),
    ActivityItem(
        timestamp=datetime.utcnow() - timedelta(days=1, hours=6),
        activity_type="Keyword Research",
        project="ZenHome Furniture",
        details="Identified 18 high‑intent keywords."
    ),
    ActivityItem(
        timestamp=datetime.utcnow() - timedelta(days=2, hours=1),
        activity_type="Content Generation",
        project="ZenHome Furniture",
        details="Created product description series for 12 items."
    ),
    ActivityItem(
        timestamp=datetime.utcnow() - timedelta(days=2, hours=4),
        activity_type="Link Building",
        project="ZenHome Furniture",
        details="Acquired 3 guest post placements."
    ),
]

chart_data = ChartDataResponse(
    traffic_growth=[
        ChartDataPoint(period="Jan", value=12000),
        ChartDataPoint(period="Feb", value=14500),
        ChartDataPoint(period="Mar", value=16700),
        ChartDataPoint(period="Apr", value=18900),
        ChartDataPoint(period="May", value=21000),
        ChartDataPoint(period="Jun", value=23500),
    ],
    rank_distribution=[
        ChartDataPoint(period="#1", value=15),
        ChartDataPoint(period="#2-3", value=30),
        ChartDataPoint(period="#4-10", value=40),
        ChartDataPoint(period="#11-20", value=12),
        ChartDataPoint(period="#21+", value=3),
    ]
)

keyword_list = [
    KeywordItem(
        keyword="organic cotton t‑shirts",
        current_rank=3,
        difficulty=45,
        search_volume=8200,
        last_updated=datetime.utcnow() - timedelta(days=1)
    ),
    KeywordItem(
        keyword="sustainable sneakers for women",
        current_rank=1,
        difficulty=38,
        search_volume=5400,
        last_updated=datetime.utcnow() - timedelta(hours=12)
    ),
    KeywordItem(
        keyword="eco friendly kitchen appliances",
        current_rank=5,
        difficulty=52,
        search_volume=2300,
        last_updated=datetime.utcnow() - timedelta(days=2)
    ),
    KeywordItem(
        keyword="recycled material furniture",
        current_rank=2,
        difficulty=44,
        search_volume=3100,
        last_updated=datetime.utcnow() - timedelta(hours=8)
    ),
    KeywordItem(
        keyword="zero waste home products",
        current_rank=4,
        difficulty=49,
        search_volume=1900,
        last_updated=datetime.utcnow() - timedelta(days=1, hours=5)
    ),
    KeywordItem(
        keyword="biodegradable packaging suppliers",
        current_rank=7,
        difficulty=55,
        search_volume=1250,
        last_updated=datetime.utcnow() - timedelta(days=3)
    ),
    KeywordItem(
        keyword="green seo tools",
        current_rank=6,
        difficulty=42,
        search_volume=8700,
        last_updated=datetime.utcnow() - timedelta(hours=20)
    ),
    KeywordItem(
        keyword="eco friendly gift ideas",
        current_rank=9,
        difficulty=48,
        search_volume=6400,
        last_updated=datetime.utcnow() - timedelta(days=2, hours=7)
    ),
]

content_list = [
    ContentItem(
        id=101,
        title="Top 10 Sustainable Sneakers for 2024",
        status="published",
        generated_at=datetime.utcnow() - timedelta(days=1, hours=2),
        url="https://stellarseo.com/blog/sustainable-sneakers-2024"
    ),
    ContentItem(
        id=102,
        title="How to Choose Eco‑Friendly Kitchen Appliances",
        status="in_review",
        generated_at=datetime.utcnow() - timedelta(hours=10),
        url=""
    ),
    ContentItem(
        id=103,
        title="The Rise of Recycled Furniture in Modern Homes",
        status="published",
        generated_at=datetime.utcnow() - timedelta(days=3),
        url="https://stellarseo.com/blog/recycled-furniture"
    ),
    ContentItem(
        id=104,
        title="Zero Waste Living: 5 Products You Need",
        status="draft",
        generated_at=datetime.utcnow() - timedelta(hours=5),
        url=""
    ),
    ContentItem(
        id=105,
        title="Biodegradable Packaging: Benefits for Brands",
        status="published",
        generated_at=datetime.utcnow() - timedelta(days=2, hours=4),
        url="https://stellarseo.com/blog/biodegradable-packaging"
    ),
    ContentItem(
        id=106,
        title="Green SEO Tools Compared: Ahrefs vs. StellarRank",
        status="published",
        generated_at=datetime.utcnow() - timedelta(days=4),
        url="https://stellarseo.com/blog/green-seo-tools"
    ),
    ContentItem(
        id=107,
        title="Eco‑Friendly Gift Guide for the Holiday Season",
        status="in_review",
        generated_at=datetime.utcnow() - timedelta(days=1, hours=6),
        url=""
    ),
    ContentItem(
        id=108,
        title="Sustainable Fashion Trends 2024",
        status="published",
        generated_at=datetime.utcnow() - timedelta(days=5),
        url="https://stellarseo.com/blog/sustainable-fashion-2024"
    ),
]

link_list = [
    LinkItem(
        source_domain="fashionista.com",
        target_url="https://stellarseo.com/blog/sustainable-sneakers-2024",
        authority_score=78.2,
        acquired_at=datetime.utcnow() - timedelta(days=2)
    ),
    LinkItem(
        source_domain="greenliving.org",
        target_url="https://stellarseo.com/blog/zero-waste-living",
        authority_score=82.5,
        acquired_at=datetime.utcnow() - timedelta(days=4)
    ),
    LinkItem(
        source_domain="techreviewer.net",
        target_url="https://stellarseo.com/blog/eco-friendly-kitchen-appliances",
        authority_score=70.1,
        acquired_at=datetime.utcnow() - timedelta(days=1, hours=3)
    ),
    LinkItem(
        source_domain="sustainabledesigns.co",
        target_url="https://stellarseo.com/blog/recycled-furniture",
        authority_score=65.4,
        acquired_at=datetime.utcnow() - timedelta(days=3, hours=8)
    ),
    LinkItem(
        source_domain="ecoblog.io",
        target_url="https://stellarseo.com/blog/biodegradable-packaging",
        authority_score=73.9,
        acquired_at=datetime.utcnow() - timedelta(days=5)
    ),
    LinkItem(
        source_domain="homegoodsmag.com",
        target_url="https://stellarseo.com/blog/eco-friendly-gift-ideas",
        authority_score=68.0,
        acquired_at=datetime.utcnow() - timedelta(days=2, hours=6)
    ),
    LinkItem(
        source_domain="sustainabilitydaily.com",
        target_url="https://stellarseo.com/blog/green-seo-tools",
        authority_score=77.3,
        acquired_at=datetime.utcnow() - timedelta(days=1, hours=12)
    ),
    LinkItem(
        source_domain="fashionfuture.org",
        target_url="https://stellarseo.com/blog/sustainable-fashion-2024",
        authority_score=80.0,
        acquired_at=datetime.utcnow() - timedelta(days=6)
    ),
]

# ---------- Endpoints ----------
@app.get("/health", response_model=HealthResponse)
def health_check():
    return HealthResponse(status="ok", app=app.title, version=app.version)

@app.get("/api/info", response_model=CompanyInfo)
def get_company_info():
    return company_info

@app.get("/api/metrics", response_model=MetricsResponse)
def get_metrics():
    return metrics_data

# Dashboard