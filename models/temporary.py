from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, EmailStr, Field


class TemporarySchemaBase(BaseModel):
    """Shared base model for temporary schema contracts."""


class TemporarySkillLevel(str, Enum):
    BEGINNER = "Beginner"
    INTERMEDIATE = "Intermediate"
    ADVANCED = "Advanced"
    EXPERT = "Expert"


class TemporaryLanguageProficiency(str, Enum):
    BASIC = "Basic"
    CONVERSATIONAL = "Conversational"
    FLUENT = "Fluent"
    NATIVE = "Native"


class TemporaryAvailabilityStatus(str, Enum):
    AVAILABLE = "Available"
    OPEN = "Open to Opportunities"
    NOT_AVAILABLE = "Not Available"


class TemporaryAvailabilityType(str, Enum):
    FULL_TIME = "Full-time"
    PART_TIME = "Part-time"
    CONTRACT = "Contract"


class TemporarySkill(TemporarySchemaBase):
    name: str
    level: TemporarySkillLevel
    yearsOfExperience: float | None = None


class TemporaryLanguage(TemporarySchemaBase):
    name: str
    proficiency: TemporaryLanguageProficiency


class TemporaryExperience(TemporarySchemaBase):
    company: str
    role: str
    startDate: str
    endDate: str | None = None
    description: str | None = None
    technologies: list[str] | None = Field(default_factory=list)
    isCurrent: bool = False


class TemporaryEducation(TemporarySchemaBase):
    institution: str
    degree: str
    fieldOfStudy: str
    startYear: int
    endYear: int | None = None


class TemporaryCertification(TemporarySchemaBase):
    name: str
    issuer: str
    issueDate: str | None = None


class TemporaryProject(TemporarySchemaBase):
    name: str
    description: str | None = None
    technologies: list[str] | None = Field(default_factory=list)
    role: str | None = None
    link: str | None = None
    startDate: str | None = None
    endDate: str | None = None


class TemporaryAvailability(TemporarySchemaBase):
    status: TemporaryAvailabilityStatus
    type: TemporaryAvailabilityType | None = None
    startDate: str | None = None


class TemporarySocialLinks(TemporarySchemaBase):
    linkedin: str | None = None
    github: str | None = None
    portfolio: str | None = None


class TemporaryTalentProfile(TemporarySchemaBase):
    id: str | None = None
    firstName: str
    lastName: str
    email: EmailStr
    headline: str
    bio: str | None = None
    location: str
    skills: list[TemporarySkill]
    languages: list[TemporaryLanguage] | None = Field(default_factory=list)
    experience: list[TemporaryExperience]
    education: list[TemporaryEducation]
    certifications: list[TemporaryCertification] | None = Field(default_factory=list)
    projects: list[TemporaryProject]
    availability: TemporaryAvailability
    socialLinks: TemporarySocialLinks | None = None


class TemporaryJobDescription(TemporarySchemaBase):
    title: str
    description: str


class TemporaryScoreBreakdown(TemporarySchemaBase):
    skills: float
    projects: float
    experience: float
    education: float
    bonus: float
    total: float


class TemporaryRankedCandidate(TemporarySchemaBase):
    rank: int
    candidateId: str | None = None
    name: str
    email: str
    headline: str
    location: str
    score: TemporaryScoreBreakdown
    evidenceMultiplier: float
    explanation: str


class TemporaryScreeningRequest(TemporarySchemaBase):
    job: TemporaryJobDescription
    candidates: list[TemporaryTalentProfile]


class TemporaryScreeningResponse(TemporarySchemaBase):
    jobTitle: str
    totalCandidates: int
    shortlisted: int
    results: list[TemporaryRankedCandidate]
