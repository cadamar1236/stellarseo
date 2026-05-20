from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import uvicorn
import os
import uuid
from datetime import datetime, timedelta
import random

app = FastAPI(title="StellarSEO", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mock Data
users = [
    {"id": "usr_001", "name": "Sarah Chen", "email": "sarah@ecobloom.com", "role": "admin", "plan": "enterprise", "joined": "2024-09-15"},
    {"id": "usr_002", "name": "Marcus Johnson", "email": "marcus@fitsphere.com", "role": "owner", "plan": "pro", "joined": "2024-10-02"},
    {"id": "usr_003", "name": "Emily Rodriguez", "email": "emily@luxecandle.com", "role": "owner", "plan": "growth", "joined": "2024-10-20"},
    {"id": "usr_004", "name": "David Kim", "email": "david@techgearpro.com", "role": "manager", "plan": "pro", "joined": "2024-11-05"},
    {"id": "usr_005", "name": "Lisa Thompson", "email": "lisa@pureorganics.com", "role": "owner", "plan": "enterprise", "joined": "2024-08-10"},
    {"id": "usr_006", "name": "James Wilson", "email": "james@petparadise.com", "role": "manager", "plan": "growth", "joined": "2024-11-25"},
    {"id": "usr_007", "name": "Anna Martinez", "email": "anna@stylevault.com", "role": "viewer", "plan": "starter", "joined": "2025-01-08"},
    {"id": "usr_008", "name": "Chris Patel", "email": "chris@homebloom.com", "role": "owner", "plan": "pro", "joined": "2024-12-15"},
]

projects = [
    {"id": "proj_001", "name": "EcoBloom Organic", "user_id": "usr_001", "industry": "Health & Beauty", "target_keywords": 45, "domain_authority": 32, "created": "2024-09-20", "status": "active"},
    {"id": "proj_002", "name": "FitSphere Equipment", "user_id": "usr_002", "industry": "Fitness", "target_keywords": 38, "domain_authority": 28, "created": "2024-10-10", "status": "active"},
    {"id": "proj_003", "name": "LuxeCandle Co.", "user_id": "usr_003", "industry": "Home Decor", "target_keywords": 52, "domain_authority": 41, "created": "2024-10-25", "status": "growing"},
    {"id": "proj_004", "name": "TechGear Pro", "user_id": "usr_004", "industry": "Electronics", "target_keywords": 67, "domain_authority": 55, "created": "2024-11-10", "status": "active"},
    {"id": "proj_005", "name": "Pure Organics Skincare", "user_id": "usr_005", "industry": "Beauty", "target_keywords": 73, "domain_authority": 61, "created": "2024-08-20", "status": "scaling"},
    {"id": "proj_006", "name": "Pet Paradise Supplies", "user_id": "usr_006", "industry": "Pets", "target_keywords": 29, "domain_authority": 22, "created": "2024-12-01", "status": "active"},
    {"id": "proj_007", "name": "StyleVault Fashion", "user_id": "usr_007", "industry": "Fashion", "target_keywords": 41, "domain_authority": 19, "created": "2025-01-16", "status": "onboarding"},
    {"id": "proj_008", "name": "HomeBloom Decor", "user_id": "usr_008", "industry": "Home & Garden", "target_keywords": 56, "domain_authority": 37, "created": "2024-12-30", "status": "growing"},
]

keywords = [
    {"id": "kw_001", "keyword": "organic skincare routine", "volume": 14200, "difficulty": 67, "cpc": 3.45, "project_id": "proj_001", "position": 4, "change": 2, "traffic": 2180},
    {"id": "kw_002", "keyword": "best home gym equipment 2025", "volume": 8900, "difficulty": 72, "cpc": 4.12, "project_id": "proj_002", "position": 7, "change": -1, "traffic": 1450},
    {"id": "kw_003", "keyword": "soy candles bulk", "volume": 5400, "difficulty": 34, "cpc": 1.89, "project_id": "proj_003", "position": 2, "change": 1, "traffic": 3100},
    {"id": "kw_004", "keyword": "wireless earbuds noise cancelling", "volume": 22300, "difficulty": 85, "cpc": 5.78, "project_id": "proj_004", "position": 11, "change": -3, "traffic": 890},
    {"id": "kw_005", "keyword": "vegan face moisturizer", "volume": 11800, "difficulty": 58, "cpc": 2.91, "project_id": "proj_005", "position": 3, "change": 1, "traffic": 2750},
    {"id": "kw_006", "keyword": "interactive cat toys", "volume": 7600, "difficulty": 42, "cpc": 2.33, "project_id": "proj_006", "position": 5, "change": 2, "traffic": 1850},
    {"id": "kw_007", "keyword": "sustainable fashion brands", "volume": 13500, "difficulty": 63, "cpc": 3.87, "project_id": "proj_007", "position": 8, "change": 0, "traffic": 1200},
    {"id": "kw_008", "keyword": "indoor plant decor ideas", "volume": 9700, "difficulty": 48, "cpc": 2.15, "project_id": "proj_008", "position": 6, "change": 1, "traffic": 1640},
]

contents = [
    {"id": "cnt_001", "title": "10 Organic Skincare Tips for Glowing Skin", "project_id": "proj_001", "type": "blog", "word_count": 2150, "status": "published", "score": 87, "published": "2025-01-10", "views": 4500},
    {"id": "cnt_002", "title": "Best Home Gym Setup Under $500", "project_id": "proj_002", "type": "guide", "word_count": 3100, "status": "published", "score": 92, "published": "2025-01-05", "views": 3200},
    {"id": "cnt_003", "title": "Complete Guide to Soy Candle Making", "project_id": "proj_003", "type": "tutorial", "word_count": 2800, "status": "draft", "score": 78, "published": None, "views": 0},
    {"id": "cnt_004", "title": "Top 10 Wireless Earbuds for 2025", "project_id": "proj_004", "type": "roundup", "word_count": 3500, "status": "published", "score": 90, "published": "2025-01-15", "views": 5800},
    {"id": "cnt_005", "title": "Why Vegan Skincare is Better for Your Skin", "project_id": "proj_005", "type": "blog", "word_count": 1950, "status": "published", "score": 84, "published": "2025-01-08", "views": 3900},
    {"id": "cnt_006", "title": "Interactive Cat Toys That Actually Work", "project_id": "proj_006", "type": "review", "word_count": 1700, "status": "review", "score": 75, "published": None, "views": 0},
    {"id": "cnt_007", "title": "Sustainable Fashion: A Complete Guide", "project_id": "proj_007", "type": "guide", "word_count": 4200, "status": "planning", "score": 65, "published": None, "views": 0},
    {"id": "cnt_008", "title": "DIY Indoor Plant Decor on a Budget", "project_id": "proj_008", "type": "tutorial", "word_count": 2300, "status": "published", "score": 81, "published": "2025-01-12", "views": 2700},
]

backlinks = [
    {"id": "bl_001", "source": "beautyblog.com", "target": "ecobloom.com", "domain_authority": 45, "type": "dofollow", "trust_flow": 38, "added": "2025-01-10", "status": "active"},
    {"id": "bl_002", "source": "fitnessmagazine.net", "target": "fitsphere.com", "domain_authority": 52, "type": "dofollow", "trust_flow": 44, "added": "2025-01-08", "status": "active"},
    {"id": "bl_003", "source": "homedecorideas.com", "target": "luxecandle.com", "domain_authority": 38, "type": "nofollow", "trust_flow": 29, "added": "2025-01-05", "status": "active"},
    {"id": "bl_004", "source": "techreviewer.io", "target": "techgearpro.com", "domain_authority": 61, "type": "dofollow", "trust_flow": 55, "added": "2025-01-15", "status": "active"},
    {"id": "bl_005", "source": "skincareexperts.com", "target": "pureorganics.com", "domain_authority": 49, "type": "dofollow", "trust_flow": 42, "added": "2025-01-12", "status": "active"},
    {"id": "bl_006", "source": "pettipsdaily.com", "target": "petparadise.com", "domain_authority": 33, "type": "nofollow", "trust_flow": 25, "added": "2025-01-03", "status": "pending"},
    {"id": "bl_007", "source": "styleinsider.net", "target": "stylevault.com", "domain_authority": 42, "type": "dofollow", "trust_flow": 36, "added": "2025-01-18", "status": "pending"},
    {"id": "bl_008", "source": "gardeningworld.com", "target": "homebloom.com", "domain_authority": 47, "type": "dofollow", "trust_flow": 40, "added": "2025-01-14", "status": "active"},
]

# Pydantic Models
class UserCreate(BaseModel):
    name: str
    email: str
    role: str = "viewer"
    plan: str = "starter"

class ProjectCreate(BaseModel):
    name: str
    user_id: str
    industry: str
    target_keywords: int = 0

class KeywordCreate(BaseModel):
    keyword: str
    volume: int = 0
    difficulty: int = 0
    cpc: float = 0.0
    project_id: str

class ContentCreate(BaseModel):
    title: str
    project_id: str
    type: str = "blog"
    word_count: int = 1000

class BacklinkCreate(BaseModel):
    source: str
    target: str
    domain_authority: int = 0
    type: str = "dofollow"

# Health
@app.get("/health")
def health():
    return {"status": "ok", "app": "StellarSEO", "version": "1.0.0"}

# Info
@app.get("/api/info")
def info():
    return {
        "name": "StellarSEO",
        "tagline": "AI-Powered SEO for E-Commerce Brands",
        "founded": "2024",
        "team_size": 42,
        "headquarters": "San Francisco, CA",
        "clients_served": 128,
        "avg_position_improvement": "47%",
        "total_keywords_tracked": 28400,
        "mission": "Help e-commerce brands rank #1 on Google through automated keyword research, content generation, and link building."
    }

# Metrics
@app.get("/api/metrics")
def metrics():
    return {
        "total_users": len(users),
        "active_projects": len([p for p in projects if p["status"] in ["active", "growing", "scaling"]]),
        "keywords_tracked": sum(p["target_keywords"] for p in projects),
        "content_pieces": len([c for c in contents if c["status"] == "published"]),
        "backlinks_built": len([b for b in backlinks if b["status"] == "active"]),
        "avg_domain_authority": round(sum(p["domain_authority"] for p in projects) / len(projects), 1),
        "total_organic_traffic": sum(k["traffic"] for k in keywords),
        "monthly_recurring_revenue": 78450,
        "churn_rate": "2.3%",
        "avg_ranking_position": round(sum(k["position"] for k in keywords) / len(keywords), 1),
    }

# Dashboard-specific endpoints
@app.get("/api/stats")
def stats():
    weekly_data = []
    for i in range(7):
        day = (datetime.now() - timedelta(days=6-i)).strftime("%Y-%m-%d")
        weekly_data.append({
            "date": day,
            "organic_traffic": random.randint(3500, 5500),
            "keyword_discoveries": random.randint(15, 40),
            "content_published": random.randint(1, 4),
            "backlinks_acquired": random.randint(2, 8),
        })
    return {
        "weekly_trend": weekly_data,
        "monthly_comparison": {
            "current_month": {"traffic": 124500, "keywords": 3200, "content": 28, "backlinks": 65},
            "previous_month": {"traffic": 108200, "keywords": 2750, "content": 22, "backlinks": 52},
            "growth_percentage": 15.1,
        },
        "top_performing_projects": sorted(projects, key=lambda p: p["domain_authority"], reverse=True)[:3],
        "total_rankings_improved": 183,
        "rankings_declined": 47,
    }

@app.get("/api/recent-activity")
def recent_activity():
    activities = [
        {"id": "act_001", "type": "ranking_change", "message": "EcoBloom 'organic skincare routine' moved from #6 to #4", "timestamp": (datetime.now() - timedelta(hours=2)).isoformat(), "severity": "positive"},
        {"id": "act_002", "type": "content_published", "message": "New guide 'Best Home Gym Setup' published for FitSphere", "timestamp": (datetime.now() - timedelta(hours=5)).isoformat(), "severity": "info"},
        {"id": "act_003", "type": "backlink_acquired", "message": "New dofollow backlink from beautyblog.com to ecobloom.com", "timestamp": (datetime.now() - timedelta(hours=8)).isoformat(), "severity": "positive"},
        {"id": "act_004", "type": "keyword_discovery", "message": "23 new keywords found for LuxeCandle Co. - 'scented candles''", "timestamp": (datetime.now() - timedelta(hours=12)).isoformat(), "severity": "info"},
        {"id": "act_005", "type": "ranking_decline", "message": "TechGear 'wireless earbuds' dropped from #8 to #11", "timestamp": (datetime.now() - timedelta(days=1)).isoformat(), "severity": "negative"},
        {"id": "act_006", "type": "project_onboarded", "message": "StyleVault Fashion successfully onboarded with 41 keywords", "timestamp": (datetime.now() - timedelta(days=2)).isoformat(), "severity": "info"},
        {"id": "act_007", "type": "content_review", "message": "Pet Paradise review piece needs revisions", "timestamp": (datetime.now() - timedelta(days=3)).isoformat(), "severity": "warning"},
    ]
    return activities

@app.get("/api/chart-data")
def chart_data(period: str = "30d"):
    data = []
    days = 30 if period == "30d" else 7
    for i in range(days):
        date = (datetime.now() - timedelta(days=days-1-i)).strftime("%Y-%m-%d")
        data.append({
            "date": date,
            "organic_traffic": random.randint(3000, 6000),
            "paid_traffic": random.randint(500, 1200),
            "social_traffic": random.randint(200, 800),
            "direct_traffic": random.randint(800, 1800),
        })
    return {
        "period": period,
        "traffic_sources": data,
        "summary": {
            "organic_traffic_total": sum(d["organic_traffic"] for d in data),
            "avg_daily_traffic": round(sum(d["organic_traffic"] for d in data) / len(data), 0),
            "best_day": max(data, key=lambda x: x["organic_traffic"])["date"],
        }
    }

# Users CRUD
@app.get("/api/users")
def get_users():
    return users

@app.post("/api/users")
def create_user(user: UserCreate):
    new_user = {
        "id": f"usr_{uuid.uuid4().hex[:6]}",
        "name": user.name,
        "email": user.email,
        "role": user.role,
        "plan": user.plan,
        "joined": datetime.now().strftime("%Y-%m-%d"),
    }
    users.append(new_user)
    return new_user

@app.get("/api/users/{user_id}")
def get_user(user_id: str):
    for user in users:
        if user["id"] == user_id:
            return user
    raise HTTPException(404, "User not found")

# Projects CRUD
@app.get("/api/projects")
def get_projects():
    return projects

@app.post("/api/projects")
def create_project(project: ProjectCreate):
    new_project = {
        "id": f"proj_{uuid.uuid4().hex[:6]}",
        "name": project.name,
        "user_id": project.user_id,
        "industry": project.industry,
        "target_keywords": project.target_keywords,
        "domain_authority": random.randint(15, 40),
        "created": datetime.now().strftime("%Y-%m-%d"),
        "status": "onboarding",
    }
    projects.append(new_project)
    return new_project

@app.get("/api/projects/{project_id}")
def get_project(project_id: str):
    for project in projects:
        if project["id"] == project_id:
            return project
    raise HTTPException(404, "Project not found")

# Keywords CRUD
@app.get("/api/keywords")
def get_keywords(project_id: Optional[str] = None):
    if project_id:
        return [k for k in keywords if k["project_id"] == project_id]
    return keywords

@app.post("/api/keywords")
def create_keyword(keyword: KeywordCreate):
    new_keyword = {
        "id": f"kw_{uuid.uuid4().hex[:6]}",
        "keyword": keyword.keyword,
        "volume": keyword.volume,
        "difficulty": keyword.difficulty,
        "cpc": keyword.cpc,
        "project_id": keyword.project_id,
        "position": random.randint(1, 15),
        "change": random.choice([-2, -1, 0, 1, 2]),
        "traffic": random.randint(500, 3000),
    }
    keywords.append(new_keyword)
    return new_keyword

# Contents CRUD
@app.get("/api/contents")
def get_contents(project_id: Optional[str] = None, status: Optional[str] = None):
    result = contents
    if project_id:
        result = [c for c in result if c["project_id"] == project_id]
    if status:
        result = [c for c in result if c["status"] == status]
    return result

@app.post("/api/contents")
def create_content(content: ContentCreate):
    new_content = {
        "id": f"cnt_{uuid.uuid4().hex[:6]}",
        "title": content.title,
        "project_id": content.project_id,
        "type": content.type,
        "word_count": content.word_count,
        "status": "planning",
        "score": random.randint(60, 80),
        "published": None,
        "views": 0,
    }
    contents.append(new_content)
    return new_content

@app.get("/api/contents/{content_id}")
def get_content(content_id: str):
    for content in contents:
        if content["id"] == content_id:
            return content
    raise HTTPException(404, "Content not found")

# Backlinks CRUD
@app.get("/api/backlinks")
def get_backlinks(project_slug: Optional[str] = None):
    if project_slug:
        target_map = {
            "ecobloom": "ecobloom.com",
            "fitsphere": "fitsphere.com",
            "luxecandle": "luxecandle.com",
            "techgearpro": "techgearpro.com",
            "pureorganics": "pureorganics.com",
            "petparadise": "petparadise.com",
            "stylevault": "stylevault.com",
            "homebloom": "homebloom.com",
        }
        domain = target_map.get(project_slug)
        if domain:
            return [b for b in backlinks if b["target"] == domain]
        return []
    return backlinks

@app.post("/api/backlinks")
def create_backlink(backlink: BacklinkCreate):
    new_backlink = {
        "id": f"bl_{uuid.uuid4().hex[:6]}",
        "source": backlink.source,
        "target": backlink.target,
        "domain_authority": backlink.domain_authority,
        "type": backlink.type,
        "trust_flow": random.randint(20, 50),
        "added": datetime.now().strftime("%Y-%m-%d"),
        "status": "pending",
    }
    backlinks.append(new_backlink)
    return new_backlink

# Analytics endpoint
@app.get("/api/analytics")
def analytics(project_id: Optional[str] = None):
    base = projects
    if project_id:
        base = [p for p in projects if p["id"] == project_id]
        if not base:
            raise HTTPException(404, "Project not found")
    
    project_keywords = [k for k in keywords if k["project_id"] == project_id] if project_id else keywords
    project_contents = [c for c in contents if c["project_id"] == project_id] if project_id else contents
    
    ranked_keywords = [k for k in project_keywords if k["position"] <= 10]
    top3 = [k for k in project_keywords if k["position"] <= 3]
    improving = [k for k in project_keywords if k["change"] > 0]
    declining = [k for k in project_keywords if k["change"] < 0]
    
    return {
        "overview": {
            "projects_tracked": len(base) if not project_id else 1,
            "total_keywords": len(project_keywords),
            "keywords_in_top_10": len(ranked_keywords),
            "keywords_in_top_3": len(top3),
            "improving_keywords": len(improving),
            "declining_keywords": len(declining),
            "avg_rank": round(sum(k["position"] for k in project_keywords) / len(project_keywords), 1) if project_keywords else 0,
            "total_traffic": sum(k["traffic"] for k in project_keywords),
        },
        "content_performance": {
            "total_pieces": len(project_contents),
            "published": len([c for c in project_contents if c["status"] == "published"]),
            "total_views": sum(c["views"] for c in project_contents),
            "avg_quality_score": round(sum(c["score"] for c in project_contents) / len(project_contents), 1) if project_contents else 0,
        },
        "backlink_profile": {
            "total_backlinks": len(backlinks),
            "active_backlinks": len([b for b in backlinks if b["status"] == "active"]),
            "avg_domain_authority": round(sum(b["domain_authority"] for b in backlinks) / len(backlinks), 1),
            "dofollow_ratio": round(len([b for b in backlinks if b["type"] == "dofollow"]) / len(backlinks) * 100, 1),
        },
    }

if __name__ == "__main__":
    PORT = int(os.environ.get("COMPANY_PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=PORT, reload=True)