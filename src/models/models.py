"""
Portfolio Data Models
Data structures for portfolio content (projects, skills, experience, etc.)
"""

from dataclasses import dataclass, field
from typing import List


@dataclass
class ProjectLink:
    """Project link model"""
    type: str  # 'live' or 'github'
    url: str
    label: str = field(default='')


@dataclass
class Project:  
    """Project model"""
    title: str
    description: str
    tags: List[str]
    links: List[ProjectLink]
    icon: str = 'fas fa-laptop-code'


@dataclass
class SkillCategory:
    """Skill category model"""
    title: str
    skills: List[str]


@dataclass
class ExperienceItem:
    """Experience item model"""
    period: str
    title: str
    company: str
    location: str
    description: List[str]
    tags: List[str]


@dataclass
class EducationItem:
    """Education item model"""
    period: str
    title: str
    institution: str
    location: str
    grade: str


@dataclass
class Certification:
    """Certification model"""
    title: str
    issuer: str
    description: str
    icon: str = 'fas fa-certificate'


@dataclass
class PortfolioStats:
    """Portfolio statistics model"""
    github_projects: int
    live_projects: int
    years_experience: int
