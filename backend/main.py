import os
from sqlalchemy import create_engine, Column, String, Integer, Float, DateTime, Text, Boolean
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from datetime import datetime, timedelta
from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import random

DATABASE_URL = os.environ.get("DATABASE_URL", "")
COMPANY_SLUG = os.environ.get("COMPANY_SLUG", "stellar_seo")
PORT = int(os.environ.get("COMPANY_PORT", 8000))

db_engine = None
SessionLocal = None

class Base(DeclarativeBase):
    pass

if DATABASE_URL:
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    db_engine = create_engine(DATABASE_URL, pool_pre_ping=True)
    SessionLocal = sessionmaker(bind=db_engine)

tablename = lambda name: f"{COMPANY_SLUG}_{name}"

class ClientDB(Base):
    __tablename__ = tablename("clients")
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    domain = Column(String, nullable=False)
    industry = Column(String, nullable=False)
    monthly_budget = Column(Float, default=0.0)
    status = Column(String, default="active")
    created_at = Column(DateTime, default=datetime.utcnow)

class CampaignDB(Base):
    __tablename__ = tablename("campaigns")
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    target_keyword = Column(String, nullable=False)
    current_rank = Column(Integer, default=0)
    target_rank = Column(Integer, default=1)
    progress = Column(Float, default=0.0)
    status = Column(String, default="active")
    created_at = Column(DateTime, default=datetime.utcnow)

class KeywordDB(Base):
    __tablename__ = tablename("keywords")
    id = Column(Integer, primary_key=True, index=True)
    campaign_id = Column(Integer, nullable=False)
    keyword = Column(String, nullable=False)
    search_volume = Column(Integer, default=0)
    difficulty = Column(Float, default=0.0)
    current_position = Column(Integer, default=0)
    best_position = Column(Integer, default=0)

class ContentDB(Base):
    __tablename__ = tablename("content")
    id = Column(Integer, primary_key=True, index=True)
    campaign_id = Column(Integer, nullable=False)
    title = Column(String, nullable=False)
    content_type = Column(String, nullable=False)
    word_count = Column(Integer, default=0)
    status = Column(String, default="draft")
    created_at = Column(DateTime, default=datetime.utcnow)

class BacklinkDB(Base):
    __tablename__ = tablename("backlinks")
    id = Column(Integer, primary_key=True, index=True)
    campaign_id = Column(Integer, nullable=False)
    source_domain = Column(String, nullable=False)
    target_url = Column(String, nullable=False)
    domain_authority = Column(Float, default=0.0)
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)

class ReportDB(Base):
    __tablename__ = tablename("reports")
    id = Column(Integer, primary_key=True, index=True)
    campaign_id = Column(Integer, nullable=False)
    report_type = Column(String, nullable=False)
    data = Column(Text, default="{}")
    generated_at = Column(DateTime, default=datetime.utcnow)

MOCK_CLIENTS = [
    {"id": 1, "name": "FashionNova Boutique", "domain": "fashionnovaboutique.com", "industry": "Fashion", "monthly_budget": 5000.0, "status": "active", "created_at": "2024-01-15T10:00:00Z"},
    {"id": 2, "name": "TechGadget Hub", "domain": "techgadgethub.com", "industry": "Electronics", "monthly_budget": 8000.0, "status": "active", "created_at": "2024-02-20T14:30:00Z"},
    {"id": 3, "name": "HomeDecor Pro", "domain": "homedecorpro.com", "industry": "Home & Garden", "monthly_budget": 3500.0, "status": "active", "created_at": "2024-03-10T09:15:00Z"},
    {"id": 4, "name": "Organic Bliss", "domain": "organicbliss.com", "industry": "Health & Wellness", "monthly_budget": 6000.0, "status": "active", "created_at": "2024-01-05T11:45:00Z"},
    {"id": 5, "name": "Pet Paradise", "domain": "petparadise.com", "industry": "Pet Supplies", "monthly_budget": 4000.0, "status": "active", "created_at": "2024-04-01T08:00:00Z"},
    {"id": 6, "name": "Gourmet Kitchen", "domain": "gourmetkitchen.com", "industry": "Food & Beverage", "monthly_budget": 5500.0, "status": "active", "created_at": "2024-05-12T16:20:00Z"},
    {"id": 7, "name": "FitLife Gear", "domain": "fitlifegear.com", "industry": "Fitness", "monthly_budget": 4500.0, "status": "active", "created_at": "2024-06-18T12:10:00Z"},
    {"id": 8, "name": "EcoHome Solutions", "domain": "ecohomesolutions.com", "industry": "Sustainable Products", "monthly_budget": 7000.0, "status": "active", "created_at": "2024-07-22T15:30:00Z"},
]

MOCK_CAMPAIGNS = [
    {"id": 1, "client_id": 1, "name": "Summer Collection SEO", "target_keyword": "summer dresses 2024", "current_rank": 12, "target_rank": 1, "progress": 75.5, "status": "active", "created_at": "2024-06-01T08:00:00Z"},
    {"id": 2, "client_id": 1, "name": "Accessories Boost", "target_keyword": "affordable jewelry online", "current_rank": 8, "target_rank": 1, "progress": 60.2, "status": "active", "created_at": "2024-06-15T09:30:00Z"},
    {"id": 3, "client_id": 2, "name": "Smartphone Domination", "target_keyword": "best budget smartphones 2024", "current_rank": 5, "target_rank": 1, "progress": 88.0, "status": "active", "created_at": "2024-05-20T10:00:00Z"},
    {"id": 4, "client_id": 2, "name": "Gadget Gift Guide", "target_keyword": "tech gifts for men", "current_rank": 15, "target_rank": 3, "progress": 45.8, "status": "active", "created_at": "2024-07-10T11:00:00Z"},
    {"id": 5, "client_id": 3, "name": "Home Makeover SEO", "target_keyword": "home decor trends 2024", "current_rank": 10, "target_rank": 1, "progress": 70.3, "status": "active", "created_at": "2024-04-01T12:00:00Z"},
    {"id": 6, "client_id": 4, "name": "Wellness Warriors", "target_keyword": "organic supplements online", "current_rank": 6, "target_rank": 1, "progress": 82.1, "status": "active", "created_at": "2024-03-15T13:00:00Z"},
    {"id": 7, "client_id": 5, "name": "Pet Supplies Push", "target_keyword": "natural dog food brands", "current_rank": 20, "target_rank": 5, "progress": 35.6, "status": "active", "created_at": "2024-08-01T14:00:00Z"},
    {"id": 8, "client_id": 6, "name": "Gourmet Reach", "target_keyword": "premium kitchen tools", "current_rank": 3, "target_rank": 1, "progress": 95.0, "status": "active", "created_at": "2024-02-10T15:00:00Z"},
]

MOCK_KEYWORDS = [
    {"id": 1, "campaign_id": 1, "keyword": "summer dresses 2024", "search_volume": 45000, "difficulty": 62.5, "current_position": 12, "best_position": 8},
    {"id": 2, "campaign_id": 1, "keyword": "casual summer outfits", "search_volume": 32000, "difficulty": 45.2, "current_position": 9, "best_position": 6},
    {"id": 3, "campaign_id": 2, "keyword": "affordable jewelry online", "search_volume": 28000, "difficulty": 38.9, "current_position": 8, "best_position": 5},
    {"id": 4, "campaign_id": 3, "keyword": "best budget smartphones", "search_volume": 55000, "difficulty": 71.3, "current_position": 5, "best_position": 3},
    {"id": 5, "campaign_id": 3, "keyword": "smartphone deals 2024", "search_volume": 41000, "difficulty": 58.7, "current_position": 7, "best_position": 4},
    {"id": 6, "campaign_id": 5, "keyword": "home decor trends", "search_volume": 38000, "difficulty": 50.1, "current_position": 10, "best_position": 7},
    {"id": 7, "campaign_id": 6, "keyword": "organic supplements", "search_volume": 33000, "difficulty": 42.8, "current_position": 6, "best_position": 3},
    {"id": 8, "campaign_id": 7, "keyword": "natural dog food", "search_volume": 25000, "difficulty": 55.4, "current_position": 20, "best_position": 15},
]

MOCK_CONTENT = [
    {"id": 1, "campaign_id": 1, "title": "Top 10 Summer Dresses for 2024: Your Ultimate Style Guide", "content_type": "blog_post", "word_count": 1500, "status": "published", "created_at": "2024-06-05T10:00:00Z"},
    {"id": 2, "campaign_id": 1, "title": "How to Style Casual Summer Outfits on a Budget", "content_type": "blog_post", "word_count": 1200, "status": "published", "created_at": "2024-06-12T14:00:00Z"},
    {"id": 3, "campaign_id": 2, "title": "Affordable Jewelry Trends That Look Expensive", "content_type": "product_roundup", "word_count": 1800, "status": "published", "created_at": "2024-06-20T09:30:00Z"},
    {"id": 4, "campaign_id": 3, "title": "Best Budget Smartphones of 2024: Expert Reviews", "content_type": "blog_post", "word_count": 2000, "status": "published", "created_at": "2024-05-25T11:00:00Z"},
    {"id": 5, "campaign_id": 3, "title": "Smartphone Deals: Where to Save Big This Year", "content_type": "buying_guide", "word_count": 1600, "status": "published", "created_at": "2024-06-01T08:00:00Z"},
    {"id": 6, "campaign_id": 5, "title": "2024 Home Decor Trends: Transform Your Space", "content_type": "blog_post", "word_count": 1400, "status": "published", "created_at": "2024-04-10T13:00:00Z"},
    {"id": 7, "campaign_id": 6, "title": "The Ultimate Guide to Organic Supplements", "content_type": "guide", "word_count": 2200, "status": "published", "created_at": "2024-03-20T15:00:00Z"},
    {"id": 8, "campaign_id": 7, "title": "Best Natural Dog Food Brands for Your Pup", "content_type": "blog_post", "word_count": 1300, "status": "draft", "created_at": "2024-08-05T10:00:00Z"},
]

MOCK_BACKLINKS = [
    {"id": 1, "campaign_id": 1, "source_domain": "fashionblogger.com", "target_url": "fashionnovaboutique.com/summer-dresses", "domain_authority": 45.0, "status": "active", "created_at": "2024-06-10T12:00:00Z"},
    {"id": 2, "campaign_id": 2, "source_domain": "jewelryreview.net", "target_url": "fashionnovaboutique.com/affordable-jewelry", "domain_authority": 38.0, "status": "active", "created_at": "2024-06-25T14:30:00Z"},
    {"id": 3, "campaign_id": 3, "source_domain": "techworld.com", "target_url": "techgadgethub.com/best-smartphones", "domain_authority": 62.0, "status": "active", "created_at": "2024-06-01T09:00:00Z"},
    {"id": 4, "campaign_id": 3, "source_domain": "gadgetreviews.org", "target_url": "techgadgethub.com/smartphone-deals", "domain_authority": 55.0, "status": "active", "created_at": "2024-06-15T11:00:00Z"},
    {"id": 5, "campaign_id": 5, "source_domain": "homedecormag.com", "target_url": "homedecorpro.com/trends-2024", "domain_authority": 50.0, "status": "active", "created_at": "2024-04-20T16:00:00Z"},
    {"id": 6, "campaign_id": 6, "source_domain": "wellnessblog.org", "target_url": "organicbliss.com/supplements-guide", "domain_authority": 42.0, "status": "active", "created_at": "2024-03-25T10:30:00Z"},
    {"id": 7, "campaign_id": 7, "source_domain": "petlovers.com", "target_url": "petparadise.com/natural-dog-food", "domain_authority": 35.0, "status": "pending", "created_at": "2024-08-10T08:00:00Z"},
    {"id": 8, "campaign_id": 8, "source_domain": "kitchenexpert.net", "target_url": "gourmetkitchen.com/premium-tools", "domain_authority": 48.0, "status": "active", "created_at": "2024-02-15T13:00:00Z"},
]

MOCK_REPORTS = [
    {"id": 1, "campaign_id": 1, "report_type": "ranking_progress", "data": '{"current_rank": 12, "improvement": "+3 positions", "period": "last_30_days"}', "generated_at": "2024-07-01T00:00:00Z"},
    {"id": 2, "campaign_id": 2, "report_type": "keyword_performance", "data": '{"total_keywords": 15, "top_10": 8, "top_3": 3}', "generated_at": "2024-07-01T00:00:00Z"},
    {"id": 3, "campaign_id": 3, "report_type": "backlink_audit", "data": '{"total_backlinks": 22, "new_backlinks": 5, "average_da": 54.3}', "generated_at": "2024-07-01T00:00:00Z"},
    {"id": 4, "campaign_id": 4, "report_type": "content_analysis", "data": '{"total_content": 12, "published": 10, "draft": 2}', "generated_at": "2024-07-01T00:00:00Z"},
    {"id": 5, "campaign_id": 5, "report_type": "ranking_progress", "data": '{"current_rank": 10, "improvement": "+5 positions", "period": "last_30_days"}', "generated_at": "2024-07-01T00:00:00Z"},
    {"id": 6, "campaign_id": 6, "report_type": "keyword_performance", "data": '{"total_keywords": 20, "top_10": 12, "top_3": 5}', "generated_at": "2024-07-01T00:00:00Z"},
    {"id": 7, "campaign_id": 7, "report_type": "backlink_audit", "data": '{"total_backlinks": 8, "new_backlinks": 3, "average_da": 38.5}', "generated_at": "2024-07-01T00:00:00Z"},
    {"id": 8, "campaign_id": 8, "report_type": "ranking_progress", "data": '{"current_rank": 3, "improvement": "+2 positions", "period": "last_30_days"}', "generated_at": "2024-07-01T00:00:00Z"},
]

app = FastAPI(title="StellarRank", version="1.0.0")

from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    if db_engine:
        Base.metadata.create_all(bind=db_engine)

class ClientCreate(BaseModel):
    name: str
    domain: str
    industry: str
    monthly_budget: float = 0.0
    status: str = "active"

class CampaignCreate(BaseModel):
    client_id: int
    name: str
    target_keyword: str
    current_rank: int = 0
    target_rank: int = 1
    progress: float = 0.0
    status: str = "active"

class KeywordCreate(BaseModel):
    campaign_id: int
    keyword: str
    search_volume: int = 0
    difficulty: float = 0.0
    current_position: int = 0
    best_position: int = 0

class ContentCreate(BaseModel):
    campaign_id: int
    title: str
    content_type: str
    word_count: int = 0
    status: str = "draft"

class BacklinkCreate(BaseModel):
    campaign_id: int
    source_domain: str
    target_url: str
    domain_authority: float = 0.0
    status: str = "pending"

class ReportCreate(BaseModel):
    campaign_id: int
    report_type: str
    data: str = "{}"

@app.get("/health")
def health():
    return {"status": "ok", "app": "StellarRank", "version": "1.0.0"}

@app.get("/api/info")
def info():
    return {
        "name": "StellarSEO",
        "app_name": "StellarRank",
        "tagline": "AI-Powered SEO for E-commerce Brands",
        "description": "Automated keyword research, content generation, and link building to rank #1 on Google",
        "founded": 2020,
        "team_size": 45,
        "clients_served": 150,
        "headquarters": "San Francisco, CA",
        "website": "https://stellarseo.com"
    }

@app.get("/api/metrics")
def metrics():
    return {
        "total_clients": 8,
        "active_campaigns": 8,
        "keywords_tracked": 85,
        "content_pieces": 48,
        "backlinks_built": 120,
        "average_ranking_improvement": "+4.2 positions",
        "monthly_recurring_revenue": 42500.0,
        "client_satisfaction_score": 4.8
    }

@app.get("/api/stats")
def stats():
    return {
        "total_keywords": 85,
        "keywords_top_10": 42,
        "keywords_top_3": 18,
        "content_published": 35,
        "content_in_draft": 13,
        "active_backlinks": 115,
        "pending_backlinks": 5,
        "campaigns_on_track": 6,
        "campaigns_needing_attention": 2
    }

@app.get("/api/recent-activity")
def recent_activity():
    activities = [
        {"id": 1, "type": "ranking_update", "description": "FashionNova: 'summer dresses' moved from #15 to #12", "timestamp": "2024-07-20T14:30:00Z"},
        {"id": 2, "type": "content_published", "description": "TechGadget: 'Smartphone Deals' guide published", "timestamp": "2024-07-20T10:15:00Z"},
        {"id": 3, "type": "backlink_acquired", "description": "OrganicBliss: New backlink from wellnessblog.org (DA 42)", "timestamp": "2024-07-19T16:45:00Z"},
        {"id": 4, "type": "campaign_completed", "description": "Gourmet Kitchen: 'premium kitchen tools' reached #3", "timestamp": "2024-07-19T09:00:00Z"},
        {"id": 5, "type": "new_client", "description": "EcoHome Solutions joined StellarSEO", "timestamp": "2024-07-18T11:30:00Z"},
        {"id": 6, "type": "keyword_added", "description": "Pet Paradise: Added 'natural dog food' to campaign", "timestamp": "2024-07-18T08:20:00Z"},
        {"id": 7, "type": "report_generated", "description": "HomeDecorPro: Monthly ranking report generated", "timestamp": "2024-07-17T15:00:00Z"},
        {"id": 8, "type": "alert", "description": "FitLife Gear: Campaign needs attention - keywords slipping", "timestamp": "2024-07-17T12:10:00Z"}
    ]
    return activities

@app.get("/api/chart-data")
def chart_data(period: str = "last_30_days"):
    if period == "last_7_days":
        labels = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        ranking_improvements = [1.2, 0.8, 1.5, 2.0, 1.8, 0.5, 1.0]
        new_backlinks = [2, 3, 1, 4, 2, 1, 3]
        content_published = [1, 2, 1, 0, 2, 1, 1]
    elif period == "last_90_days":
        labels = ["May", "Jun", "Jul"]
        ranking_improvements = [15.2, 18.5, 22.1]
        new_backlinks = [25, 30, 28]
        content_published = [12, 14, 9]
    else:
        labels = ["Week 1", "Week 2", "Week 3", "Week 4"]
        ranking_improvements = [4.5, 6.2, 5.8, 7.1]
        new_backlinks = [8, 12, 10, 14]
        content_published = [4, 5, 3, 6]
    return {
        "labels": labels,
        "datasets": [
            {"label": "Ranking Improvement (positions)", "data": ranking_improvements, "borderColor": "#4CAF50"},
            {"label": "New Backlinks", "data": new_backlinks, "borderColor": "#2196F3"},
            {"label": "Content Published", "data": content_published, "borderColor": "#FF9800"}
        ]
    }

@app.get("/api/clients")
def get_clients():
    if SessionLocal:
        db = SessionLocal()
        clients = db.query(ClientDB).all()
        db.close()
        return [{"id": c.id, "name": c.name, "domain": c.domain, "industry": c.industry, "monthly_budget": c.monthly_budget, "status": c.status, "created_at": c.created_at.isoformat()} for c in clients]
    return MOCK_CLIENTS

@app.post("/api/clients")
def create_client(client: ClientCreate):
    if SessionLocal:
        db = SessionLocal()
        db_client = ClientDB(name=client.name, domain=client.domain, industry=client.industry, monthly_budget=client.monthly_budget, status=client.status)
        db.add(db_client)
        db.commit()
        db.refresh(db_client)
        db.close()
        return {"id": db_client.id, "name": db_client.name, "domain": db_client.domain, "industry": db_client.industry, "monthly_budget": db_client.monthly_budget, "status": db_client.status, "created_at": db_client.created_at.isoformat()}
    new_client = client.dict()
    new_client["id"] = len(MOCK_CLIENTS) + 1
    new_client["created_at"] = datetime.utcnow().isoformat()
    MOCK_CLIENTS.append(new_client)
    return new_client

@app.get("/api/campaigns")
def get_campaigns(client_id: Optional[int] = None):
    if SessionLocal:
        db = SessionLocal()
        query = db.query(CampaignDB)
        if client_id:
            query = query.filter(CampaignDB.client_id == client_id)
        campaigns = query.all()
        db.close()
        return [{"id": c.id, "client_id": c.client_id, "name": c.name, "target_keyword": c.target_keyword, "current_rank": c.current_rank, "target_rank": c.target_rank, "progress": c.progress, "status": c.status, "created_at": c.created_at.isoformat()} for c in campaigns]
    if client_id:
        return [c for c in MOCK_CAMPAIGNS if c["client_id"] == client_id]
    return MOCK_CAMPAIGNS

@app.post("/api/campaigns")
def create_campaign(campaign: CampaignCreate):
    if SessionLocal:
        db = SessionLocal()
        db_campaign = CampaignDB(client_id=campaign.client_id, name=campaign.name, target_keyword=campaign.target_keyword, current_rank=campaign.current_rank, target_rank=campaign.target_rank, progress=campaign.progress, status=campaign.status)
        db.add(db_campaign)
        db.commit()
        db.refresh(db_campaign)
        db.close()
        return {"id": db_campaign.id, "client_id": db_campaign.client_id, "name": db_campaign.name, "target_keyword": db_campaign.target_keyword, "current_rank": db_campaign.current_rank, "target_rank": db_campaign.target_rank, "progress": db_campaign.progress, "status": db_campaign.status, "created_at": db_campaign.created_at.isoformat()}
    new_campaign = campaign.dict()
    new_campaign["id"] = len(MOCK_CAMPAIGNS) + 1
    new_campaign["created_at"] = datetime.utcnow().isoformat()
    MOCK_CAMPAIGNS.append(new_campaign)
    return new_campaign

@app.get("/api/keywords")
def get_keywords(campaign_id: Optional[int] = None):
    if SessionLocal:
        db = SessionLocal()
        query = db.query(KeywordDB)
        if campaign_id:
            query = query.filter(KeywordDB.campaign_id == campaign_id)
        keywords = query.all()
        db.close()
        return [{"id": k.id, "campaign_id": k.campaign_id, "keyword": k.keyword, "search_volume": k.search_volume, "difficulty": k.difficulty, "current_position": k.current_position, "best_position": k.best_position} for k in keywords]
    if campaign_id:
        return [k for k in MOCK_KEYWORDS if k["campaign_id"] == campaign_id]
    return MOCK_KEYWORDS

@app.post("/api/keywords")
def create_keyword(keyword: KeywordCreate):
    if SessionLocal:
        db = SessionLocal()
        db_keyword = KeywordDB(campaign_id=keyword.campaign_id, keyword=keyword.keyword, search_volume=keyword.search_volume, difficulty=keyword.difficulty, current_position=keyword.current_position, best_position=keyword.best_position)
        db.add(db_keyword)
        db.commit()
        db.refresh(db_keyword)
        db.close()
        return {"id": db_keyword.id, "campaign_id": db_keyword.campaign_id, "keyword": db_keyword.keyword, "search_volume": db_keyword.search_volume, "difficulty": db_keyword.difficulty, "current_position": db_keyword.current_position, "best_position": db_keyword.best_position}
    new_keyword = keyword.dict()
    new_keyword["id"] = len(MOCK_KEYWORDS) + 1
    MOCK_KEYWORDS.append(new_keyword)
    return new_keyword

@app.get("/api/content")
def get_content(campaign_id: Optional[int] = None):
    if SessionLocal:
        db = SessionLocal()
        query = db.query(ContentDB)
        if campaign_id:
            query = query.filter(ContentDB.campaign_id == campaign_id)
        content = query.all()
        db.close()
        return [{"id": c.id, "campaign_id": c.campaign_id, "title": c.title, "content_type": c.content_type, "word_count": c.word_count, "status": c.status, "created_at": c.created_at.isoformat()} for c in content]
    if campaign_id:
        return [c for c in MOCK_CONTENT if c["campaign_id"] == campaign_id]
    return MOCK_CONTENT

@app.post("/api/content")
def create_content(content: ContentCreate):
    if SessionLocal:
        db = SessionLocal()
        db_content = ContentDB(campaign_id=content.campaign_id, title=content.title, content_type=content.content_type, word_count=content.word_count, status=content.status)
        db.add(db_content)
        db.commit()
        db.refresh(db_content)
        db.close()
        return {"id": db_content.id, "campaign_id": db_content.campaign_id, "title": db_content.title, "content_type": db_content.content_type, "word_count": db_content.word_count, "status": db_content.status, "created_at": db_content.created_at.isoformat()}
    new_content = content.dict()
    new_content["id"] = len(MOCK_CONTENT) + 1
    new_content["created_at"] = datetime.utcnow().isoformat()
    MOCK_CONTENT.append(new_content)
    return new_content

@app.get("/api/backlinks")
def get_backlinks(campaign_id: Optional[int] = None):
    if SessionLocal:
        db = SessionLocal()
        query = db.query(BacklinkDB)
        if campaign_id:
            query = query.filter(BacklinkDB.campaign_id == campaign_id)
        backlinks = query.all()
        db.close()
        return [{"id": b.id, "campaign_id": b.campaign_id, "source_domain": b.source_domain, "target_url": b.target_url, "domain_authority": b.domain_authority, "status": b.status, "created_at": b.created_at.isoformat()} for b in backlinks]
    if campaign_id:
        return [b for b in MOCK_BACKLINKS if b["campaign_id"] == campaign_id]
    return MOCK_BACKLINKS

@app.post("/api/backlinks")
def create_backlink(backlink: BacklinkCreate):
    if SessionLocal:
        db = SessionLocal()
        db_backlink = BacklinkDB(campaign_id=backlink.campaign_id, source_domain=backlink.source_domain, target_url=backlink.target_url, domain_authority=backlink.domain_authority, status=backlink.status)
        db.add(db_backlink)
        db.commit()
        db.refresh(db_backlink)
        db.close()
        return {"id": db_backlink.id, "campaign_id": db_backlink.campaign_id, "source_domain": db_backlink.source_domain, "target_url": db_backlink.target_url, "domain_authority": db_backlink.domain_authority, "status": db_backlink.status, "created_at": db_backlink.created_at.isoformat()}
    new_backlink = backlink.dict()
    new_backlink["id"] = len(MOCK_BACKLINKS) + 1
    new_backlink["created_at"] = datetime.utcnow().isoformat()
    MOCK_BACKLINKS.append(new_backlink)
    return new_backlink

@app.get("/api/reports")
def get_reports(campaign_id: Optional[int] = None):
    if SessionLocal:
        db = SessionLocal()
        query = db.query(ReportDB)
        if campaign_id:
            query = query.filter(ReportDB.campaign_id == campaign_id)
        reports = query.all()
        db.close()
        return [{"id": r.id, "campaign_id": r.campaign_id, "report_type": r.report_type, "data": r.data, "generated_at": r.generated_at.isoformat()} for r in reports]
    if campaign_id:
        return [r for r in MOCK_REPORTS if r["campaign_id"] == campaign_id]
    return MOCK_REPORTS

@app.post("/api/reports")
def create_report(report: ReportCreate):
    if SessionLocal:
        db = SessionLocal()
        db_report = ReportDB(campaign_id=report.campaign_id, report_type=report.report_type, data=report.data)
        db.add(db_report)
        db.commit()
        db.refresh(db_report)
        db.close()
        return {"id": db_report.id, "campaign_id": db_report.campaign_id, "report_type":