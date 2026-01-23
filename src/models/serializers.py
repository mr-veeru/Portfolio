"""
Portfolio Serializers
Model-to-dictionary conversion utilities
"""

from typing import Dict, Any
from src.models.models import (
    Project, SkillCategory, ExperienceItem,
    EducationItem, Certification, PortfolioStats
)


class Serializers:
    """Utility class for serializing portfolio models to dictionaries"""

    @staticmethod
    def project_to_dict(project: Project) -> Dict[str, Any]:
        """Convert Project model to dictionary"""
        return {
            "title": project.title,
            "description": project.description,
            "tags": project.tags,
            "links": [{"type": link.type, "url": link.url, "label": link.label} for link in project.links],
            "icon": project.icon
        }

    @staticmethod
    def skill_category_to_dict(category: SkillCategory) -> Dict[str, Any]:
        """Convert SkillCategory model to dictionary"""
        return {
            "title": category.title,
            "skills": category.skills
        }

    @staticmethod
    def experience_to_dict(experience: ExperienceItem) -> Dict[str, Any]:
        """Convert ExperienceItem model to dictionary"""
        return {
            "period": experience.period,
            "title": experience.title,
            "company": experience.company,
            "location": experience.location,
            "description": experience.description,
            "tags": experience.tags
        }

    @staticmethod
    def education_to_dict(education: EducationItem) -> Dict[str, Any]:
        """Convert EducationItem model to dictionary"""
        return {
            "period": education.period,
            "title": education.title,
            "institution": education.institution,
            "location": education.location,
            "grade": education.grade
        }

    @staticmethod
    def certification_to_dict(certification: Certification) -> Dict[str, Any]:
        """Convert Certification model to dictionary"""
        return {
            "title": certification.title,
            "issuer": certification.issuer,
            "description": certification.description,
            "icon": certification.icon
        }

    @staticmethod
    def stats_to_dict(stats: PortfolioStats) -> Dict[str, Any]:
        """Convert PortfolioStats model to dictionary"""
        return {
            "github_projects": stats.github_projects,
            "live_projects": stats.live_projects,
            "years_experience": stats.years_experience
        }
