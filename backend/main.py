import os
from sqlalchemy import create_engine, Column, String, Integer, Float, DateTime, Text, Boolean, JSON, ForeignKey
from sqlalchemy.orm import DeclarativeBase, sessionmaker, relationship
from datetime import datetime, timedelta
from typing import Optional, List
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random
import uuid

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

class User(Base):
    __tablename__ = f"{COMPANY_SLUG}_users"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    role = Column(String, default="client")
    created_at = Column(DateTime, default=datetime.utcnow)

class Client(Base):
    __tablename__ = f"{COMPANY_SLUG}_clients"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey(f"{COMPANY_SLUG}_users.id"))
    company_name = Column(String, nullable=False)
    website = Column(String)
    industry = Column(String)
    monthly_budget = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)

class Project(Base):
    __tablename__ = f"{COMPANY_SLUG}_projects"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    client_id = Column(String, ForeignKey(f"{COMPANY_SLUG}_clients.id"))
    name = Column(String, nullable=False)
    target_keywords = Column(Text)
    status = Column(String, default="active")
    created_at = Column(DateTime, default=datetime.utcnow)

class Keyword(Base):
    __tablename__ = f"{COMPANY_SLUG}_keywords"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = Column(String, ForeignKey(f"{COMPANY_SLUG}_projects.id"))
    keyword = Column(String, nullable=False)
    volume = Column(Integer, default=0)
    difficulty = Column(Float, default=0.0)
    current_position = Column(Integer, default=0)
    target_position = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)

class Content(Base):
    __tablename__ = f"{COMPANY_SLUG}_contents"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = Column(String, ForeignKey(f"{COMPANY_SLUG}_projects.id"))
    title = Column(String, nullable=False)
    content_type = Column(String, default="blog_post")
    word_count = Column(Integer, default=0)
    status = Column(String, default="draft")
    generated_at = Column(DateTime, default=datetime.utcnow)

class LinkBuilding(Base):
    __tablename__ = f"{COMPANY_SLUG}_link_buildings"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = Column(String, ForeignKey(f"{COMPANY_SLUG}_projects.id"))
    target_url = Column(String, nullable=False)
    source_domain = Column(String)
    link_type = Column(String, default="guest_post")
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)

class RankingHistory(Base):
    __tablename__ = f"{COMPANY_SLUG}_ranking_histories"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    keyword_id = Column(String, ForeignKey(f"{COMPANY_SLUG}_keywords.id"))
    position = Column(Integer, nullable=False)
    date = Column(DateTime, default=datetime.utcnow)

class Report(Base):
    __tablename__ = f"{COMPANY_SLUG}_reports"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = Column(String, ForeignKey(f"{COMPANY_SLUG}_projects.id"))
    type = Column(String, default="weekly")
    metrics = Column(JSON)
    generated_at = Column(DateTime, default=datetime.utcnow)

if db_engine:
    Base.metadata.create_all(db_engine)

MOCK_USERS = [
    {"id": "u1", "email": "elena@stellar.com", "name": "Elena Vasquez", "role": "admin", "created_at": "2024-01-15T08:00:00Z"},
    {"id": "u2", "email": "marcus@stellar.com", "name": "Marcus Chen", "role": "manager", "created_at": "2024-02-01T10:30:00Z"},
    {"id": "u3", "email": "sarah@shopify.com", "name": "Sarah Johnson", "role": "client", "created_at": "2024-03-10T14:00:00Z"},
    {"id": "u4", "email": "david@etsy.com", "name": "David Park", "role": "client", "created_at": "2024-04-05T09:15:00Z"},
    {"id": "u5", "email": "lina@amazon.com", "name": "Lina Patel", "role": "client", "created_at": "2024-05-20T16:45:00Z"},
    {"id": "u6", "email": "james@bigcommerce.com", "name": "James Wilson", "role": "client", "created_at": "2024-06-01T11:00:00Z"}
]

MOCK_CLIENTS = [
    {"id": "c1", "user_id": "u3", "company_name": "Shopify Elite", "website": "shopifyelite.com", "industry": "ecommerce", "monthly_budget": 5000.0, "created_at": "2024-03-10T14:00:00Z"},
    {"id": "c2", "user_id": "u4", "company_name": "Etsy Handmade", "website": "etsyhandmade.com", "industry": "ecommerce", "monthly_budget": 3000.0, "created_at": "2024-04-05T09:15:00Z"},
    {"id": "c3", "user_id": "u5", "company_name": "Amazon Sellers Pro", "website": "amazonsellerspro.com", "industry": "ecommerce", "monthly_budget": 8000.0, "created_at": "2024-05-20T16:45:00Z"},
    {"id": "c4", "user_id": "u6", "company_name": "BigCommerce Brands", "website": "bigcommercebrands.com", "industry": "ecommerce", "monthly_budget": 4000.0, "created_at": "2024-06-01T11:00:00Z"},
    {"id": "c5", "user_id": "u1", "company_name": "Stellar Demo", "website": "stellardemo.com", "industry": "technology", "monthly_budget": 2000.0, "created_at": "2024-01-20T07:00:00Z"}
]

MOCK_PROJECTS = [
    {"id": "p1", "client_id": "c1", "name": "Shopify SEO Overhaul", "target_keywords": "organic skincare, natural beauty products", "status": "active", "created_at": "2024-03-15T08:00:00Z"},
    {"id": "p2", "client_id": "c1", "name": "Content Expansion", "target_keywords": "vegan makeup, cruelty-free cosmetics", "status": "active", "created_at": "2024-04-01T10:00:00Z"},
    {"id": "p3", "client_id": "c2", "name": "Etsy Ranking Boost", "target_keywords": "handmade jewelry, artisan gifts", "status": "active", "created_at": "2024-04-10T14:00:00Z"},
    {"id": "p4", "client_id": "c3", "name": "Amazon A+ Content", "target_keywords": "wireless earbuds, fitness tracker", "status": "active", "created_at": "2024-05-25T09:00:00Z"},
    {"id": "p5", "client_id": "c4", "name": "Brand Authority Build", "target_keywords": "smart home devices, home automation", "status": "paused", "created_at": "2024-06-05T11:00:00Z"},
    {"id": "p6", "client_id": "c3", "name": "Backlink Campaign", "target_keywords": "portable charger, phone accessories", "status": "active", "created_at": "2024-06-15T15:00:00Z"},
    {"id": "p7", "client_id": "c5", "name": "Demo Project", "target_keywords": "seo tools, marketing analytics", "status": "archived", "created_at": "2024-01-25T08:30:00Z"}
]

MOCK_KEYWORDS = [
    {"id": "k1", "project_id": "p1", "keyword": "organic skincare", "volume": 45000, "difficulty": 65.2, "current_position": 8, "target_position": 1, "created_at": "2024-03-15T08:00:00Z"},
    {"id": "k2", "project_id": "p1", "keyword": "natural beauty products", "volume": 32000, "difficulty": 58.7, "current_position": 12, "target_position": 1, "created_at": "2024-03-15T08:00:00Z"},
    {"id": "k3", "project_id": "p1", "keyword": "vegan makeup brands", "volume": 18500, "difficulty": 42.1, "current_position": 5, "target_position": 1, "created_at": "2024-03-15T08:00:00Z"},
    {"id": "k4", "project_id": "p1", "keyword": "cruelty-free cosmetics", "volume": 27000, "difficulty": 51.3, "current_position": 9, "target_position": 1, "created_at": "2024-03-15T08:00:00Z"},
    {"id": "k5", "project_id": "p2", "keyword": "vegan makeup", "volume": 22000, "difficulty": 48.9, "current_position": 6, "target_position": 1, "created_at": "2024-04-01T10:00:00Z"},
    {"id": "k6", "project_id": "p3", "keyword": "handmade jewelry", "volume": 35000, "difficulty": 55.6, "current_position": 10, "target_position": 1, "created_at": "2024-04-10T14:00:00Z"},
    {"id": "k7", "project_id": "p3", "keyword": "artisan gifts", "volume": 15000, "difficulty": 38.4, "current_position": 4, "target_position": 1, "created_at": "2024-04-10T14:00:00Z"},
    {"id": "k8", "project_id": "p4", "keyword": "wireless earbuds", "volume": 68000, "difficulty": 72.8, "current_position": 15, "target_position": 1, "created_at": "2024-05-25T09:00:00Z"},
    {"id": "k9", "project_id": "p4", "keyword": "fitness tracker", "volume": 55000, "difficulty": 68.4, "current_position": 11, "target_position": 1, "created_at": "2024-05-25T09:00:00Z"},
    {"id": "k10", "project_id": "p5", "keyword": "smart home devices", "volume": 72000, "difficulty": 75.1, "current_position": 20, "target_position": 1, "created_at": "2024-06-05T11:00:00Z"}
]

MOCK_CONTENT = [
    {"id": "ct1", "project_id": "p1", "title": "Ultimate Guide to Organic Skincare Routines", "content_type": "blog_post", "word_count": 2500, "status": "published", "generated_at": "2024-04-10T08:00:00Z"},
    {"id": "ct2", "project_id": "p1", "title": "Top 10 Natural Beauty Products for Glowing Skin", "content_type": "blog_post", "word_count": 1800, "status": "published", "generated_at": "2024-04-20T10:00:00Z"},
    {"id": "ct3", "project_id": "p1", "title": "Why Cruelty-Free Cosmetics Matter", "content_type": "blog_post", "word_count": 1500, "status": "draft", "generated_at": "2024-05-05T14:00:00Z"},
    {"id": "ct4", "project_id": "p2", "title": "Best Vegan Makeup Brands in 2024", "content_type": "blog_post", "word_count": 2000, "status": "published", "generated_at": "2024-05-15T09:00:00Z"},
    {"id": "ct5", "project_id": "p3", "title": "How to Sell Handmade Jewelry on Etsy", "content_type": "blog_post", "word_count": 2200, "status": "published", "generated_at": "2024-05-20T11:00:00Z"},
    {"id": "ct6", "project_id": "p4", "title": "Wireless Earbuds vs. Wired: Which is Better?", "content_type": "blog_post", "word_count": 1200, "status": "draft", "generated_at": "2024-06-01T13:00:00Z"},
    {"id": "ct7", "project_id": "p4", "title": "Top Fitness Trackers for 2024 Reviews", "content_type": "product_review", "word_count": 3000, "status": "published", "generated_at": "2024-06-10T10:00:00Z"},
    {"id": "ct8", "project_id": "p6", "title": "Best Portable Chargers for Travel", "content_type": "listicle", "word_count": 1600, "status": "draft", "generated_at": "2024-06-20T15:00:00Z"}
]

MOCK_LINK_BUILDINGS = [
    {"id": "l1", "project_id": "p1", "target_url": "shopifyelite.com/organic-skincare", "source_domain": "beautyblog.com", "link_type": "guest_post", "status": "completed", "created_at": "2024-04-05T08:00:00Z"},
    {"id": "l2", "project_id": "p1", "target_url": "shopifyelite.com/natural-beauty", "source_domain": "skincarehub.com", "link_type": "guest_post", "status": "completed", "created_at": "2024-04-12T10:00:00Z"},
    {"id": "l3", "project_id": "p1", "target_url": "shopifyelite.com/vegan-makeup", "source_domain": "cosmeticinsight.com", "link_type": "guest_post", "status": "pending", "created_at": "2024-05-01T14:00:00Z"},
    {"id": "l4", "project_id": "p3", "target_url": "etsyhandmade.com/jewelry", "source_domain": "craftsblog.net", "link_type": "guest_post", "status": "in_progress", "created_at": "2024-05-10T09:00:00Z"},
    {"id": "l5", "project_id": "p4", "target_url": "amazonsellerspro.com/earbuds", "source_domain": "techreview.com", "link_type": "guest_post", "status": "pending", "created_at": "2024-06-05T11:00:00Z"},
    {"id": "l6", "project_id": "p4", "target_url": "amazonsellerspro.com/fitness-tracker", "source_domain": "fitnessgear.com", "link_type": "guest_post", "status": "pending", "created_at": "2024-06-12T13:00:00Z"},
    {"id": "l7", "project_id": "p6", "target_url": "amazonsellerspro.com/charger", "source_domain": "gadgetguide.com", "link_type": "guest_post", "status": "in_progress", "created_at": "2024-06-22T15:00:00Z"}
]

MOCK_RANKING_HISTORIES = [
    {"id": "r1", "keyword_id": "k1", "position": 15, "date": "2024-03-20T08:00:00Z"},
    {"id": "r2", "keyword_id": "k1", "position": 12, "date": "2024-04-10T08:00:00Z"},
    {"id": "r3", "keyword_id": "k1", "position": 9, "date": "2024-05-01T08:00:00Z"},
    {"id": "r4", "keyword_id": "k1", "position": 8, "date": "2024-05-20T08:00:00Z"},
    {"id": "r5", "keyword_id": "k2", "position": 18, "date": "2024-03-25T10:00:00Z"},
    {"id": "r6", "keyword_id": "k2", "position": 15, "date": "2024-04-15T10:00:00Z"},
    {"id": "r7", "keyword_id": "k2", "position": 12, "date": "2024-05-05T10:00:00Z"},
    {"id": "r8", "keyword_id": "k3", "position": 7, "date": "2024-04-01T14:00:00Z"},
    {"id": "r9", "keyword_id": "k3", "position": 5, "date": "2024-05-10T14:00:00Z"},
    {"id": "r10", "keyword_id": "k6", "position": 14, "date": "2024-04-15T09:00:00Z"},
    {"id": "r11", "keyword_id": "k6", "position": 10, "date": "2024-05-15T09:00:00Z"},
    {"id": "r12", "keyword_id": "k8", "position": 20, "date": "2024-06-01T11:00:00Z"},
    {"id": "r13", "keyword_id": "k8", "position": 15, "date": "2024-06-15T11:00:00Z"}
]

MOCK_REPORTS = [
    {"id": "rp1", "project_id": "p1", "type": "weekly", "metrics": {"impressions": 45000, "clicks": 3200, "ctr": 7.1, "avg_position": 8.5}, "generated_at": "2024-06-24T08:00:00Z"},
    {"id": "rp2", "project_id": "p1", "type": "monthly", "metrics": {"impressions": 180000, "clicks": 12800, "ctr": 7.1, "avg_position": 8.2, "revenue_estimate": 45000}, "generated_at": "2024-06-01T08:00:00Z"},
    {"id": "rp3", "project_id": "p3", "type": "weekly", "metrics": {"impressions": 22000, "clicks": 1800, "ctr": 8.2, "avg_position": 6.5}, "generated_at": "2024-06-24T09:00:00Z"},
    {"id": "rp4", "project_id": "p4", "type": "weekly", "metrics": {"impressions": 35000, "clicks": 2100, "ctr": 6.0, "avg_position": 12.0}, "generated_at": "2024-06-24T11:00:00Z"},
    {"id": "rp5", "project_id": "p2", "type": "monthly", "metrics": {"impressions": 90000, "clicks": 6400, "ctr": 7.1, "avg_position": 7.8, "revenue_estimate": 22000}, "generated_at": "2024-06-01T10:00:00Z"}
]

app = FastAPI(title="RankStellar", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserCreate(BaseModel):
    email: str
    name: str
    role: str = "client"

class ClientCreate(BaseModel):
    user_id: str
    company_name: str
    website: str = ""
    industry: str = ""
    monthly_budget: float = 0.0

class ProjectCreate(BaseModel):
    client_id: str
    name: str
    target_keywords: str = ""
    status: str = "active"

class KeywordCreate(BaseModel):
    project_id: str
    keyword: str
    volume: int = 0
    difficulty: float = 0.0
    current_position: int = 0
    target_position: int = 1

class ContentCreate(BaseModel):
    project_id: str
    title: str
    content_type: str = "blog_post"
    word_count: int = 0
    status: str = "draft"

class LinkBuildingCreate(BaseModel):
    project_id: str
    target_url: str
    source_domain: str = ""
    link_type: str = "guest_post"
    status: str = "pending"

class RankingHistoryCreate(BaseModel):
    keyword_id: str
    position: int
    date: datetime = datetime.utcnow()

class ReportCreate(BaseModel):
    project_id: str
    type: str = "weekly"
    metrics: dict = {}

@app.on_event("startup")
async def startup():
    if db_engine:
        Base.metadata.create_all(db_engine)

@app.get("/health")
async def health():
    return {"status": "ok", "app": "RankStellar", "version": "1.0.0"}

@app.get("/api/info")
async def info():
    return {
        "name": "RankStellar",
        "company": "StellarSEO",
        "tagline": "AI-Powered SEO for E-Commerce Brands",
        "founded": "2023",
        "team_size": 42,
        "clients_served": 150,
        "keywords_tracked": 25000,
        "avg_ranking_improvement": 65
    }

@app.get("/api/metrics")
async def metrics():
    return {
        "total_projects": 7,
        "active_projects": 5,
        "keywords_tracked": 10,
        "content_generated": 8,
        "backlinks_built": 7,
        "avg_keyword_position": 10.8,
        "impressions_this_month": 385000,
        "clicks_this_month": 27500,
        "ctr_avg": 7.14
    }

@app.get("/api/stats")
async def stats():
    return {
        "keyword_rankings": [
            {"keyword": "organic skincare", "current": 8, "target": 1, "change": -4},
            {"keyword": "natural beauty products", "current": 12, "target": 1, "change": -6},
            {"keyword": "vegan makeup brands", "current": 5, "target": 1, "change": -2},
            {"keyword": "cruelty-free cosmetics", "current": 9, "target": 1, "change": -3},
            {"keyword": "handmade jewelry", "current": 10, "target": 1, "change": -4}
        ],
        "content_performance": [
            {"title": "Ultimate Guide to Organic Skincare Routines", "views": 12500, "shares": 340},
            {"title": "Top 10 Natural Beauty Products for Glowing Skin", "views": 9800, "shares": 210},
            {"title": "Best Vegan Makeup Brands in 2024", "views": 7500, "shares": 180},
            {"title": "How to Sell Handmade Jewelry on Etsy", "views": 6200, "shares": 95},
            {"title": "Top Fitness Trackers for 2024 Reviews", "views": 4500, "shares": 120}
        ],
        "backlink_growth": [
            {"month": "Jan", "new_links": 2},
            {"month": "Feb", "new_links": 3},
            {"month": "Mar", "new_links": 5},
            {"month": "Apr", "new_links": 4},
            {"month": "May", "new_links": 6},
            {"month": "Jun", "new_links": 3}
        ]
    }

@app.get("/api/recent-activity")
async def recent_activity():
    return [
        {"id": "a1", "type": "ranking_improved", "message": "Keyword 'organic skincare' moved from position 12 to 8", "timestamp": "2024-06-23T14:30:00Z"},
        {"id": "a2", "type": "content_published", "message": "Content 'Top Fitness Trackers for 2024 Reviews' published", "timestamp": "2024-06-22T10:15:00Z"},
        {"id": "a3", "type": "backlink_added", "message": "New backlink from beautyblog.com to shopifyelite.com/organic-skincare", "timestamp": "2024-06-21T16:45:00Z"},
        {"id": "a4", "type": "new_project", "message": "Project 'Backlink Campaign' started for Amazon Sellers Pro", "timestamp": "2024-06-20T09:00:00Z"},
        {"id": "a5", "type": "keyword_added", "message": "Keyword 'portable charger' added to project 'Backlink Campaign'", "timestamp": "2024-06-19T11:30:00Z"},
        {"id": "a6", "type": "report_generated", "message": "Weekly report for Shopify Elite generated", "timestamp": "2024-06-18T08:00:00Z"},
        {"id": "a7", "type": "client_added", "message": "New client 'BigCommerce Brands' onboarded", "timestamp": "2024-06-05T11:00:00Z"}
    ]

@app.get("/api/chart-data")
async def chart_data():
    return {
        "keyword_positions_over_time": [
            {"date": "2024-03-20", "organic_skincare": 15, "natural_beauty": 18, "vegan_makeup": 10},
            {"date": "2024-04-10", "organic_skincare": 12, "natural_beauty": 15, "vegan_makeup": 8},
            {"date": "2024-05-01", "organic_skincare": 9, "natural_beauty": 12, "vegan_makeup": 7},
            {"date": "2024-05-20", "organic_skincare": 8, "natural_beauty": 12, "vegan_makeup": 5},
            {"date": "2024-06-10", "organic_skincare": 8, "natural_beauty": 12, "vegan_makeup": 5}
        ],
        "impressions_clicks": [
            {"month": "Jan", "impressions": 120000, "clicks": 8400},
            {"month": "Feb", "impressions": 145000, "clicks": 10150},
            {"month": "Mar", "impressions": 180000, "clicks": 12600},
            {"month": "Apr", "impressions": 220000, "clicks": 15840},
            {"month": "May", "impressions": 260000, "clicks": 18720},
            {"month": "Jun", "impressions": 385000, "clicks": 27500}
        ],
        "revenue_estimate": [
            {"month": "Jan", "revenue": 12000},
            {"month": "Feb", "revenue": 15000},
            {"month": "Mar", "revenue": 18000},
            {"month": "Apr", "revenue": 22000},
            {"month": "May", "revenue": 28000},
            {"month": "Jun", "revenue": 35000}
        ]
    }

@app.get("/api/users")
async def get_users():
    if SessionLocal:
        db = SessionLocal()
        users = db.query(User).all()
        db.close()
        return [{"id": u.id, "email": u.email, "name": u.name, "role": u.role, "created_at": u.created_at.isoformat()} for u in users]
    return MOCK_USERS

@app.post("/api/users")
async def create_user(user: UserCreate):
    if SessionLocal:
        db = SessionLocal()
        db_user = User(id=str(uuid.uuid4()), email=user.email, name=user.name, role=user.role)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        db.close()
        return {"id": db_user.id, "email": db_user.email, "name": db_user.name, "role": db_user.role, "created_at": db_user.created_at.isoformat()}
    new_user = {"id": str(uuid.uuid4()), "email": user.email, "name": user.name, "role": user.role, "created_at": datetime.utcnow().isoformat() + "Z"}
    MOCK_USERS.append(new_user)
    return new_user

@app.get("/api/clients")
async def get_clients():
    if SessionLocal:
        db = SessionLocal()
        clients = db.query(Client).all()
        db.close()
        return [{"id": c.id, "user_id": c.user_id, "company_name": c.company_name, "website": c.website, "industry": c.industry, "monthly_budget": c.monthly_budget, "created_at": c.created_at.isoformat()} for c in clients]
    return MOCK_CLIENTS

@app.post("/api/clients")
async def create_client(client: ClientCreate):
    if SessionLocal:
        db = SessionLocal()
        db_client = Client(id=str(uuid.uuid4()), user_id=client.user_id, company_name=client.company_name, website=client.website, industry=client.industry, monthly_budget=client.monthly_budget)
        db.add(db_client)
        db.commit()
        db.refresh(db_client)
        db.close()
        return {"id": db_client.id, "user_id": db_client.user_id, "company_name": db_client.company_name, "website": db_client.website, "industry": db_client.industry, "monthly_budget": db_client.monthly_budget, "created_at": db_client.created_at.isoformat()}
    new_client = {"id": str(uuid.uuid4()), "user_id": client.user_id, "company_name": client.company_name, "website": client.website, "industry": client.industry, "monthly_budget": client.monthly_budget, "created_at": datetime.utcnow().isoformat() + "Z"}
    MOCK_CLIENTS.append(new_client)
    return new_client

@app.get("/api/projects")
async def get_projects():
    if SessionLocal:
        db = SessionLocal()
        projects = db.query(Project).all()
        db.close()
        return [{"id": p.id, "client_id": p.client_id, "name": p.name, "target_keywords": p.target_keywords, "status": p.status, "created_at": p.created_at.isoformat()} for p in projects]
    return MOCK_PROJECTS

@app.post("/api/projects")
async def create_project(project: ProjectCreate):
    if SessionLocal:
        db = SessionLocal()
        db_project = Project(id=str(uuid.uuid4()), client_id=project.client_id, name=project.name, target_keywords=project.target_keywords, status=project.status)
        db.add(db_project)
        db.commit()
        db.refresh(db_project)
        db.close()
        return {"id": db_project.id, "client_id": db_project.client_id, "name": db_project.name, "target_keywords": db_project.target_keywords, "status": db_project.status, "created_at": db_project.created_at.isoformat()}
    new_project = {"id": str(uuid.uuid4()), "client_id": project.client_id, "name": project.name, "target_keywords": project.target_keywords, "status": project.status, "created_at": datetime.utcnow().isoformat() + "Z"}
    MOCK_PROJECTS.append(new_project)
    return new_project

@app.get("/api/keywords")
async def get_keywords(project_id: Optional[str] = Query(None)):
    if SessionLocal:
        db = SessionLocal()
        query = db.query(Keyword)
        if project_id:
            query = query.filter(Keyword.project_id == project_id)
        keywords = query.all()
        db.close()
        return [{"id": k.id, "project_id": k.project_id, "keyword": k.keyword, "volume": k.volume, "difficulty": k.difficulty, "current_position": k.current_position, "target_position": k.target_position, "created_at": k.created_at.isoformat()} for k in keywords]
    if project_id:
        return [k for k in MOCK_KEYWORDS if k["project_id"] == project_id]
    return MOCK_KEYWORDS

@app.post("/api/keywords")
async def create_keyword(keyword: KeywordCreate):
    if SessionLocal:
        db = SessionLocal()
        db_keyword = Keyword(id=str(uuid.uuid4()), project_id=keyword.project_id, keyword=keyword.keyword, volume=