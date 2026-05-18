from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import uvicorn
import os
import random
import uuid

PORT = int(os.environ.get("COMPANY_PORT", 8000))

app = FastAPI(title="StellarSEO", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Pydantic Models ---

class User(BaseModel):
    id: str
    name: str
    email: str
    role: str
    avatar: str
    created_at: str

class Client(BaseModel):
    id: str
    name: str
    domain: str
    industry: str
    monthly_budget: int
    keywords_tracked: int
    rank_improvement: float
    active_campaigns: int
    last_active: str

class Keyword(BaseModel):
    id: str
    keyword: str
    volume: int
    difficulty: int
    current_rank: int
    target_rank: int
    trend: str
    search_intent: str
    client_id: str

class Content(BaseModel):
    id: str
    title: str
    url: str
    word_count: int
    status: str
    seo_score: int
    published_at: str
    views: int
    clicks: int
    client_id: str

class Link(BaseModel):
    id: str
    source_url: str
    target_url: str
    anchor_text: str
    domain_authority: int
    type: str
    status: str
    acquired_at: str
    client_id: str

class Campaign(BaseModel):
    id: str
    name: str
    client_id: str
    status: str
    type: str
    start_date: str
    end_date: str
    budget_spent: int
    impressions: int
    clicks: int
    conversions: int

class AnalyticsSnapshot(BaseModel):
    id: str
    date: str
    total_traffic: int
    organic_traffic: int
    referral_traffic: int
    avg_session_duration: float
    bounce_rate: float
    top_pages: List[Dict[str, Any]]
    client_id: str

# --- Mock Data ---

MOCK_USERS = [
    User(id="u1", name="Alex Rivera", email="alex@stellarseo.ai", role="admin", avatar="https://api.dicebear.com/7.x/avataaars/svg?seed=Alex", created_at="2023-01-15"),
    User(id="u2", name="Sophia Chen", email="sophia@stellarseo.ai", role="manager", avatar="https://api.dicebear.com/7.x/avataaars/svg?seed=Sophia", created_at="2023-03-22"),
    User(id="u3", name="Marcus Johnson", email="marcus@stellarseo.ai", role="editor", avatar="https://api.dicebear.com/7.x/avataaars/svg?seed=Marcus", created_at="2023-06-10"),
    User(id="u4", name="Priya Patel", email="priya@stellarseo.ai", role="analyst", avatar="https://api.dicebear.com/7.x/avataaars/svg?seed=Priya", created_at="2023-08-05"),
    User(id="u5", name="James Wilson", email="james@stellarseo.ai", role="editor", avatar="https://api.dicebear.com/7.x/avataaars/svg?seed=James", created_at="2024-02-14"),
    User(id="u6", name="Emma Thompson", email="emma@stellarseo.ai", role="manager", avatar="https://api.dicebear.com/7.x/avataaars/svg?seed=Emma", created_at="2024-04-01"),
]

MOCK_CLIENTS = [
    Client(id="c1", name="EcoVibe Naturals", domain="ecovibenaturals.com", industry="Health & Wellness", monthly_budget=5000, keywords_tracked=245, rank_improvement=12.5, active_campaigns=4, last_active="2025-03-28"),
    Client(id="c2", name="UrbanThreads", domain="urbanthreads.com", industry="Fashion", monthly_budget=8000, keywords_tracked=412, rank_improvement=18.3, active_campaigns=6, last_active="2025-03-29"),
    Client(id="c3", name="GadgetFlow", domain="gadgetflow.io", industry="Electronics", monthly_budget=12000, keywords_tracked=680, rank_improvement=9.8, active_campaigns=8, last_active="2025-03-30"),
    Client(id="c4", name="PurePet Supply", domain="purepetsupply.com", industry="Pet Care", monthly_budget=3500, keywords_tracked=189, rank_improvement=22.1, active_campaigns=3, last_active="2025-03-27"),
    Client(id="c5", name="HomeBloom", domain="homebloom.com", industry="Home & Garden", monthly_budget=6000, keywords_tracked=320, rank_improvement=15.7, active_campaigns=5, last_active="2025-03-29"),
    Client(id="c6", name="FitFuel", domain="fitfuel.com", industry="Fitness", monthly_budget=7500, keywords_tracked=450, rank_improvement=20.4, active_campaigns=5, last_active="2025-03-28"),
    Client(id="c7", name="BabyBliss", domain="babybliss.com", industry="Baby Products", monthly_budget=4000, keywords_tracked=210, rank_improvement=16.2, active_campaigns=4, last_active="2025-03-26"),
]

def generate_keyword_volume():
    return random.randint(100, 50000)

def generate_difficulty():
    return random.randint(10, 95)

def generate_rank():
    return random.randint(1, 100)

MOCK_KEYWORDS = [
    Keyword(id="kw1", keyword="organic skincare routine", volume=12500, difficulty=65, current_rank=8, target_rank=1, trend="up", search_intent="informational", client_id="c1"),
    Keyword(id="kw2", keyword="best natural moisturizer", volume=8900, difficulty=72, current_rank=14, target_rank=3, trend="stable", search_intent="commercial", client_id="c1"),
    Keyword(id="kw3", keyword="vegan face cream", volume=5600, difficulty=58, current_rank=22, target_rank=5, trend="up", search_intent="commercial", client_id="c1"),
    Keyword(id="kw4", keyword="sustainable beauty products", volume=3400, difficulty=45, current_rank=11, target_rank=2, trend="up", search_intent="informational", client_id="c1"),
    Keyword(id="kw5", keyword="eco-friendly packaging", volume=2800, difficulty=38, current_rank=6, target_rank=1, trend="up", search_intent="informational", client_id="c1"),
    Keyword(id="kw6", keyword="men's streetwear fashion", volume=15200, difficulty=78, current_rank=19, target_rank=4, trend="down", search_intent="commercial", client_id="c2"),
    Keyword(id="kw7", keyword="affordable graphic tees", volume=9800, difficulty=62, current_rank=7, target_rank=2, trend="up", search_intent="commercial", client_id="c2"),
    Keyword(id="kw8", keyword="vintage denim jacket", volume=7200, difficulty=55, current_rank=12, target_rank=3, trend="stable", search_intent="transactional", client_id="c2"),
    Keyword(id="kw9", keyword="wireless noise cancelling earbuds", volume=28300, difficulty=88, current_rank=34, target_rank=10, trend="up", search_intent="commercial", client_id="c3"),
    Keyword(id="kw10", keyword="best budget smartwatch 2025", volume=19500, difficulty=82, current_rank=27, target_rank=8, trend="up", search_intent="commercial", client_id="c3"),
    Keyword(id="kw11", keyword="portable bluetooth speaker", volume=16700, difficulty=75, current_rank=16, target_rank=5, trend="stable", search_intent="commercial", client_id="c3"),
    Keyword(id="kw12", keyword="grain free dog food", volume=14200, difficulty=60, current_rank=9, target_rank=2, trend="up", search_intent="commercial", client_id="c4"),
    Keyword(id="kw13", keyword="organic cat treats", volume=8900, difficulty=48, current_rank=5, target_rank=1, trend="up", search_intent="commercial", client_id="c4"),
    Keyword(id="kw14", keyword="small space furniture", volume=11300, difficulty=70, current_rank=21, target_rank=6, trend="down", search_intent="commercial", client_id="c5"),
    Keyword(id="kw15", keyword="indoor plant care guide", volume=9800, difficulty=52, current_rank=4, target_rank=1, trend="up", search_intent="informational", client_id="c5"),
    Keyword(id="kw16", keyword="home protein powder", volume=20500, difficulty=68, current_rank=18, target_rank=5, trend="up", search_intent="commercial", client_id="c6"),
    Keyword(id="kw17", keyword="pre workout supplement", volume=17800, difficulty=85, current_rank=31, target_rank=10, trend="stable", search_intent="commercial", client_id="c6"),
    Keyword(id="kw18", keyword="organic baby formula", volume=12100, difficulty=55, current_rank=7, target_rank=2, trend="up", search_intent="commercial", client_id="c7"),
]

def generate_content_status():
    return random.choice(["published", "draft", "review", "optimized"])

def generate_seo_score():
    return random.randint(45, 98)

def generate_views():
    return random.randint(500, 25000)

MOCK_CONTENT = [
    Content(id="co1", title="10 Organic Skincare Myths Debunked", url="https://ecovibenaturals.com/blog/organic-skincare-myths", word_count=2100, status="published", seo_score=88, published_at="2025-03-20", views=12500, clicks=890, client_id="c1"),
    Content(id="co2", title="Complete Guide to Natural Moisturizers", url="https://ecovibenaturals.com/blog/natural-moisturizer-guide", word_count=3200, status="published", seo_score=92, published_at="2025-03-15", views=18900, clicks=1450, client_id="c1"),
    Content(id="co3", title="Why Sustainable Beauty Matters", url="https://ecovibenaturals.com/blog/sustainable-beauty", word_count=1800, status="published", seo_score=85, published_at="2025-03-25", views=8700, clicks=620, client_id="c1"),
    Content(id="co4", title="Ultimate Streetwear Style Guide 2025", url="https://urbanthreads.com/blog/streetwear-style-guide", word_count=2800, status="published", seo_score=91, published_at="2025-03-22", views=22300, clicks=1780, client_id="c2"),
    Content(id="co5", title="Top 10 Vintage Fashion Trends", url="https://urbanthreads.com/blog/vintage-trends", word_count=1600, status="draft", seo_score=72, published_at="2025-03-28", views=0, clicks=0, client_id="c2"),
    Content(id="co6", title="Best Wireless Earbuds for Workouts", url="https://gadgetflow.io/blog/workout-earbuds", word_count=2400, status="published", seo_score=86, published_at="2025-03-18", views=31200, clicks=2560, client_id="c3"),
    Content(id="co7", title="Smartwatch vs Traditional Watch: Which is Better?", url="https://gadgetflow.io/blog/smartwatch-vs-traditional", word_count=1900, status="review", seo_score=79, published_at="2025-03-26", views=4500, clicks=380, client_id="c3"),
    Content(id="co8", title="Grain Free vs Regular Dog Food: Vet Explains", url="https://purepetsupply.com/blog/grain-free-dog-food", word_count=2600, status="published", seo_score=94, published_at="2025-03-10", views=15800, clicks=1240, client_id="c4"),
    Content(id="co9", title="Small Apartment Decor Ideas That Save Space", url="https://homebloom.com/blog/small-apartment-decor", word_count=2200, status="published", seo_score=87, published_at="2025-03-19", views=19600, clicks=1520, client_id="c5"),
    Content(id="co10", title="Best Home Gym Equipment for Small Spaces", url="https://fitfuel.com/blog/home-gym-small-space", word_count=3000, status="optimized", seo_score=96, published_at="2025-03-12", views=28900, clicks=2310, client_id="c6"),
    Content(id="co11", title="Organic Baby Food: What Parents Need to Know", url="https://babybliss.com/blog/organic-baby-food", word_count=3500, status="published", seo_score=90, published_at="2025-03-14", views=21300, clicks=1690, client_id="c7"),
    Content(id="co12", title="Safe Baby Products Guide 2025", url="https://babybliss.com/blog/safe-baby-products", word_count=2800, status="draft", seo_score=68, published_at="2025-03-27", views=0, clicks=0, client_id="c7"),
]

def generate_domain_authority():
    return random.randint(15, 85)

MOCK_LINKS = [
    Link(id="l1", source_url="https://healthline.com/skincare-tips", target_url="https://ecovibenaturals.com/blog/natural-moisturizer-guide", anchor_text="natural moisturizer guide", domain_authority=82, type="guest_post", status="active", acquired_at="2025-02-15", client_id="c1"),
    Link(id="l2", source_url="https://forbes.com/beauty-trends-2025", target_url="https://ecovibenaturals.com", anchor_text="organic skincare brand", domain_authority=92, type="editorial", status="active", acquired_at="2025-03-01", client_id="c1"),
    Link(id="l3", source_url="https://vogue.com/fashion-week", target_url="https://urbanthreads.com/blog/streetwear-style-guide", anchor_text="streetwear fashion", domain_authority=90, type="guest_post", status="active", acquired_at="2025-02-20", client_id="c2"),
    Link(id="l4", source_url="https://techcrunch.com/gadgets-2025", target_url="https://gadgetflow.io", anchor_text="best tech gadgets", domain_authority=88, type="press_release", status="active", acquired_at="2025-03-05", client_id="c3"),
    Link(id="l5", source_url="https://cnet.com/earbuds-review", target_url="https://gadgetflow.io/blog/workout-earbuds", anchor_text="wireless earbuds", domain_authority=85, type="editorial", status="pending", acquired_at="2025-03-22", client_id="c3"),
    Link(id="l6", source_url="https://petmd.com/dog-nutrition", target_url="https://purepetsupply.com/blog/grain-free-dog-food", anchor_text="grain free dog food", domain_authority=76, type="guest_post", status="active", acquired_at="2025-02-28", client_id="c4"),
    Link(id="l7", source_url="https://apartmenttherapy.com/small-spaces", target_url="https://homebloom.com/blog/small-apartment-decor", anchor_text="small space decor", domain_authority=72, type="guest_post", status="active", acquired_at="2025-03-10", client_id="c5"),
    Link(id="l8", source_url="https://menshealth.com/fitness", target_url="https://fitfuel.com/blog/home-gym-small-space", anchor_text="home gym equipment", domain_authority=78, type="editorial", status="active", acquired_at="2025-03-08", client_id="c6"),
    Link(id="l9", source_url="https://parents.com/baby-care", target_url="https://babybliss.com/blog/organic-baby-food", anchor_text="organic baby food", domain_authority=74, type="guest_post", status="active", acquired_at="2025-03-02", client_id="c7"),
    Link(id="l10", source_url="https://thespruce.com/gardening-tips", target_url="https://homebloom.com", anchor_text="indoor plant guide", domain_authority=65, type="forum", status="active", acquired_at="2025-03-18", client_id="c5"),
]

MOCK_CAMPAIGNS = [
    Campaign(id="cam1", name="Organic Keywords Q1 2025", client_id="c1", status="active", type="keyword_optimization", start_date="2025-01-01", end_date="2025-03-31", budget_spent=4500, impressions=125000, clicks=8900, conversions=420),
    Campaign(id="cam2", name="Link Building Outreach - Fashion", client_id="c2", status="active", type="link_building", start_date="2025-02-01", end_date="2025-04-30", budget_spent=6800, impressions=89000, clicks=7200, conversions=310),
    Campaign(id="cam3", name="Content Marketing - Gadget Reviews", client_id="c3", status="active", type="content_marketing", start_date="2025-01-15", end_date="2025-04-15", budget_spent=10200, impressions=245000, clicks=18200, conversions=890),
    Campaign(id="cam4", name="Local SEO - Pet Stores", client_id="c4", status="active", type="local_seo", start_date="2025-03-01", end_date="2025-05-31", budget_spent=2800, impressions=56000, clicks=4100, conversions=190),
    Campaign(id="cam5", name="Home Decor Blog Content", client_id="c5", status="active", type="content_marketing", start_date="2025-02-15", end_date="2025-04-30", budget_spent=5100, impressions=112000, clicks=8400, conversions=375),
    Campaign(id="cam6", name="Fitness Influencer Outreach", client_id="c6", status="active", type="influencer_marketing", start_date="2025-03-01", end_date="2025-05-15", budget_spent=6500, impressions=178000, clicks=14200, conversions=620),
    Campaign(id="cam7", name="Baby Product Keyword Strategy", client_id="c7", status="active", type="keyword_optimization", start_date="2025-02-01", end_date="2025-04-30", budget_spent=3400, impressions=78000, clicks=5800, conversions=280),
    Campaign(id="cam8", name="Technical SEO Audit - All Clients", client_id="c1", status="completed", type="technical_seo", start_date="2025-01-10", end_date="2025-02-28", budget_spent=2000, impressions=0, clicks=0, conversions=0),
]

def generate_traffic():
    return random.randint(5000, 80000)

MOCK_ANALYTICS = [
    AnalyticsSnapshot(
        id=f"analytics_{i}",
        date=(datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d"),
        total_traffic=generate_traffic(),
        organic_traffic=generate_traffic(),
        referral_traffic=generate_traffic(),
        avg_session_duration=round(random.uniform(1.5, 5.5), 2),
        bounce_rate=round(random.uniform(25.0, 65.0), 1),
        top_pages=[
            {"url": f"/blog/post-{j}", "views": random.randint(500, 5000), "avg_time": round(random.uniform(30, 300), 1)}
            for j in range(1, 6)
        ],
        client_id=random.choice(["c1", "c2", "c3", "c4", "c5", "c6", "c7"])
    )
    for i in range(30)
]

# --- Endpoints ---

@app.get("/health")
async def health():
    return {"status": "ok", "app": "StellarSEO", "version": "1.0.0"}

@app.get("/api/info")
async def info():
    return {
        "name": "StellarSEO",
        "tagline": "AI-Powered SEO That Puts Your Brand on the Stars",
        "description": "StellarSEO is an AI-driven SEO agency specializing in helping e-commerce brands dominate Google search results through automated keyword research, intelligent content generation, and strategic link building.",
        "founded": "2022",
        "team_size": 42,
        "headquarters": "San Francisco, CA",
        "clients_served": 150,
        "average_rank_improvement": 16.8,
        "keywords_tracked_total": 25800,
        "monthly_content_generated": 320,
        "backlinks_built": 4500,
        "industries_covered": ["Health & Wellness", "Fashion", "Electronics", "Pet Care", "Home & Garden", "Fitness", "Baby Products"],
        "features": ["AI Keyword Research", "Automated Content Generation", "Smart Link Building", "Real-time Analytics", "Competitor Analysis", "Rank Tracking"],
        "pricing_tiers": ["Starter", "Growth", "Enterprise"],
        "contact_email": "hello@stellarseo.ai"
    }

@app.get("/api/metrics")
async def metrics():
    return {
        "total_revenue": 1245000,
        "monthly_recurring_revenue": 124000,
        "active_clients": 45,
        "total_campaigns": 78,
        "keywords_in_top_10": 4200,
        "average_rank": 8.3,
        "content_pieces_published": 1560,
        "backlinks_acquired": 3200,
        "organic_traffic_growth": 28.5,
        "conversion_rate": 4.2,
        "client_retention_rate": 94.7,
        "average_session_duration_minutes": 4.8,
        "bounce_rate": 38.2,
        "roi_average": 320,
        "new_clients_this_month": 5,
        "churned_clients_this_month": 1,
        "revenue_growth_percent": 18.3,
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

@app.get("/api/stats")
async def stats():
    return {
        "daily_active_clients": 38,
        "campaigns_in_progress": 52,
        "keywords_discovered_this_week": 340,
        "content_pieces_created_this_week": 24,
        "backlinks_pending_verification": 18,
        "tasks_completed_today": 145,
        "avg_campaign_performance_score": 82.5,
        "client_satisfaction_score": 4.8,
        "support_tickets_open": 3,
        "uptime_percentage": 99.97
    }

@app.get("/api/recent-activity")
async def recent_activity():
    activities = [
        {"id": "act1", "type": "keyword_gain", "description": "EcoVibe Naturals moved to #3 for 'organic skincare routine'", "timestamp": "2025-03-30T09:45:00Z", "client": "EcoVibe Naturals", "severity": "positive"},
        {"id": "act2", "type": "content_published", "description": "New blog post 'Smartwatch vs Traditional Watch' published for GadgetFlow", "timestamp": "2025-03-30T08:30:00Z", "client": "GadgetFlow", "severity": "info"},
        {"id": "act3", "type": "link_acquired", "description": "Guest post published on Forbes linking to UrbanThreads", "timestamp": "2025-03-29T14:20:00Z", "client": "UrbanThreads", "severity": "positive"},
        {"id": "act4", "type": "rank_drop", "description": "FitFuel dropped 2 positions for 'pre workout supplement'", "timestamp": "2025-03-29T12:10:00Z", "client": "FitFuel", "severity": "negative"},
        {"id": "act5", "type": "campaign_completed", "description": "Technical SEO audit completed for all clients", "timestamp": "2025-03-28T16:00:00Z", "client": "Multiple", "severity": "info"},
        {"id": "act6", "type": "new_client", "description": "New client 'Organic Bark' onboarded - Pet Care industry", "timestamp": "2025-03-28T10:00:00Z", "client": "Organic Bark", "severity": "positive"},
        {"id": "act7", "type": "keyword_discovery", "description": "120 new keywords discovered for HomeBloom campaign", "timestamp": "2025-03-27T15:45:00Z", "client": "HomeBloom", "severity": "info"},
        {"id": "act8", "type": "system_alert", "description": "Content generation queue at 85% capacity", "timestamp": "2025-03-27T11:30:00Z", "client": "System", "severity": "warning"},
    ]
    return activities

@app.get("/api/chart-data")
async def chart_data(period: str = Query("30d", regex="^(7d|30d|90d|1y)$")):
    days = {"7d": 7, "30d": 30, "90d": 90, "1y": 365}[period]
    start_date = datetime.now() - timedelta(days=days)
    
    chart_data = []
    current_date = start_date
    while current_date <= datetime.now():
        chart_data.append({
            "date": current_date.strftime("%Y-%m-%d"),
            "organic_traffic": random.randint(8000, 30000),
            "referral_traffic": random.randint(2000, 8000),
            "direct_traffic": random.randint(3000, 10000),
            "social_traffic": random.randint(1000, 5000),
            "keywords_in_top_10": random.randint(3000, 4500),
            "content_published": random.randint(0, 5),
            "backlinks_acquired": random.randint(1, 10),
            "conversions": random.randint(50, 300)
        })
        current_date += timedelta(days=1)
    
    return chart_data

@app.get("/api/keywords")
async def get_keywords(client_id: Optional[str] = Query(None)):
    if client_id:
        return [k for k in MOCK_KEYWORDS if k.client_id == client_id]
    return MOCK_KEYWORDS

@app.get("/api/keywords/{keyword_id}")
async def get_keyword(keyword_id: str):
    keyword = next((k for k in MOCK_KEYWORDS if k.id == keyword_id), None)
    if not keyword:
        raise HTTPException(status_code=404, detail="Keyword not found")
    return keyword

@app.get("/api/content")
async def get_content(client_id: Optional[str] = Query(None), status: Optional[str] = Query(None)):
    result = MOCK_CONTENT
    if client_id:
        result = [c for c in result if c.client_id == client_id]
    if status:
        result = [c for c in result if c.status == status]
    return result

@app.get("/api/content/{content_id}")
async def get_content_item(content_id: str):
    content = next((c for c in MOCK_CONTENT if c.id == content_id), None)
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    return content

@app.get("/api/links")
async def get_links(client_id: Optional[str] = Query(None), status: Optional[str] = Query(None)):
    result = MOCK_LINKS
    if client_id:
        result = [l for l in result if l.client_id == client_id]
    if status:
        result = [l for l in result if l.status == status]
    return result

@app.get("/api/links/{link_id}")
async def get_link(link_id: str):
    link = next((l for l in MOCK_LINKS if l.id == link_id), None)
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")
    return link

@app.get("/api/campaigns")
async def get_campaigns(client_id: Optional[str] = Query(None), status: Optional[str] = Query(None)):
    result = MOCK_CAMPAIGNS
    if client_id:
        result = [c for c in result if c.client_id == client_id]
    if status:
        result = [c for c in result if c.status == status]
    return result

@app.get("/api/campaigns/{campaign_id}")
async def get_campaign(campaign_id: str):
    campaign = next((c for c in MOCK_CAMPAIGNS if c.id == campaign_id), None)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return campaign

@app.get("/api/analytics")
async def get_analytics(client_id: Optional[str] = Query(None), days: int = Query(7, ge=1, le=90)):
    result = MOCK_ANALYTICS
    if client_id:
        result = [a for a in result if a.client_id == client_id]
    # Return last N days
    return sorted(result, key=lambda x: x.date, reverse=True)[:days]

@app.get("/api/analytics/{analytics_id}")
async def get_analytics_item(analytics_id: str):
    analytics = next((a for a in MOCK_ANALYTICS if a.id == analytics_id), None)
    if not analytics:
        raise HTTPException(status_code=404, detail="Analytics not found")
    return analytics

@app.get("/api/users")
async def get_users():
    return MOCK_USERS

@app.get("/api/users/{user_id}")
async def get_user(user_id: str):
    user = next((u for u in MOCK_USERS if u.id == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.get("/api/clients")
async def get_clients():
    return MOCK_CLIENTS

@app.get("/api/clients/{client_id}")
async def get_client(client_id: str):
    client = next((c for c in MOCK_CLIENTS if c.id == client_id), None)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client

@app.post("/api/keywords")
async def add_keyword(keyword: Keyword):
    MOCK_KEYWORDS.append(keyword)
    return keyword

@app.post("/api/content")
async def add_content(content: Content):
    MOCK_CONTENT.append(content)
    return content

@app.post("/api/links")
async def add_link(link: Link):
    MOCK_LINKS.append(link)
    return link

@app.post("/api/campaigns")
async def add_campaign(campaign: Campaign):
    MOCK_CAMPAIGNS.append(campaign)
    return campaign

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=PORT, reload=True)