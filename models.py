from pydantic import BaseModel, HttpUrl
from typing import List, Optional, Dict, Any



class Source(BaseModel):
    id: Optional[str] = "Unknown"
    name: Optional[str] = "Unknown"

class Article(BaseModel):
    source: Optional[Source]
    author: Optional[str]
    title: str
    description: Optional[str] = "Unavalible"
    url: HttpUrl
    urlToImage: Optional[HttpUrl] = None
    publishedAt: str
    content: str
    def __repr__(self):
        return f"【{self.title}】from {self.source.name}"

class Overview(BaseModel):
    status: str
    totalResults: int
    articles: List[Article]
    message: Optional[str] = None

class HeadlineSource(BaseModel):
    id: str
    name: str
    description: str
    url: HttpUrl
    category: str
    language: str
    country: str
    def __repr__(self):
        return f"{self.name} [{self.id}]"

class HeadlineOverview(BaseModel):
    status: str
    sources: List[HeadlineSource]