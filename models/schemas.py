from pydantic import BaseModel, EmailStr
from typing import Optional, List
from enum import Enum

class SkillLevel(str, Enum):
    BEGINNER = "Beginner"
    INTERMEDIATE = "Intermediate"
    ADVANCED = "Advanced"
    EXPERT = "Expert"

class LanguageProficiency(str, Enum):
    BASIC = "Basic"
    CONVERSATIONAL = "Conversational"
    FLUENT = "Fluent"
    NATIVE = "Native"

class AvailabilityStatus(str, Enum):
    AVAILABLE = "Available"
    OPEN = "Open to Opportunities"
    NOT_AVAILABLE = "Not Available"

class AvailabilityType(str, Enum):
    FULL_TIME = "Full-time"
    PART_TIME = "Part-time"
    CONTRACT = "Contract"
class Skill(BaseModel):
    name: str
    level: SkillLevel
    yearsOfExperience: Optional[float] = None

class Language(BaseModel):
    name: str
    proficiency: LanguageProficiency

class Experience(BaseModel):
    company: str
    role: str
    startDate: str                        
    endDate: Optional[str] = None
    description: Optional[str] = None     
    technologies: Optional[List[str]] = []
    isCurrent: Optional[bool] = False

class Education(BaseModel):
    institution: str
    degree: str
    fieldOfStudy: str
    startYear: int
    endYear: Optional[int] = None

class Certification(BaseModel):
    name: str
    issuer: str
    issueDate: Optional[str] = None 

class Project(BaseModel):
    name: str
    description: Optional[str] = None
    technologies: Optional[List[str]] = []
    role: Optional[str] = None
    link: Optional[str] = None            
    startDate: Optional[str] = None
    endDate: Optional[str] = None

class Availability(BaseModel):
    status: AvailabilityStatus
    type: Optional[AvailabilityType] = None
    startDate: Optional[str] = None 

class SocialLinks(BaseModel):
    linkedin: Optional[str] = None
    github: Optional[str] = None          
    portfolio: Optional[str] = None

class TalentProfile(BaseModel):

    id: Optional[str] = None              
    firstName: str
    lastName: str
    email: EmailStr                        
    headline: str
    bio: Optional[str] = None                        
    location: str
 
   
    skills: List[Skill]
    languages: Optional[List[Language]] = []
    experience: List[Experience]
    education: List[Education]
    certifications: Optional[List[Certification]] = []
    projects: List[Project]
    availability: Availability
    socialLinks: Optional[SocialLinks] = None

class JobDescription(BaseModel):
    title: str                            
    description: str

class ScoreBreakdown(BaseModel):
    skills: float       # Out of 45
    projects: float     # Out of 25
    experience: float   # Out of 15
    education: float    # Out of 10
    bonus: float        # Out of 5
    total: float        # Out of 100 (after evidence multiplier applied)     

class RankedCandidate(BaseModel):
    rank: int                              
    candidateId: Optional[str] = None
    name: str
    email: str                         
    headline: str
    location: str
    score: ScoreBreakdown
    evidenceMultiplier: float
    explanation: str 

class ScreeningRequest(BaseModel):
    job: JobDescription
    candidates: List[TalentProfile] 

class ScreeningResponse(BaseModel):
    jobTitle: str
    totalCandidates: int                  
    shortlisted: int                       
    results: List[RankedCandidate]       
 
