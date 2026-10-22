
from pydantic import BaseModel, ConfigDict, Field, HttpUrl
from urllib.parse import urlparse


class EvidenceSource(BaseModel):
    model_config = ConfigDict(extra="forbid")

    url: str = Field(min_length=1)
    supporting_excerpt: str = Field(min_length=1)


class ResearchCandidate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    candidate_id: str = Field(min_length=1)
    description: str = Field(min_length=1)
    evidence: list[EvidenceSource] = Field(default_factory=list)
    approved: bool = False
    outreach_sent: bool = False


def validate_candidate(candidate: ResearchCandidate) -> bool:
    """Reject candidates without usable source URLs and supporting excerpts."""
    if not candidate.description.strip() or not candidate.evidence:
        return False

    for source in candidate.evidence:
        parsed = urlparse(source.url)

        if (
            parsed.scheme != "https"
            or not parsed.netloc
            or not parsed.hostname
            or not source.supporting_excerpt.strip()
        ):
            return False

    return True


def approve_candidate(candidate: ResearchCandidate) -> ResearchCandidate:
    """Approve only candidates that pass evidence validation."""
    if not validate_candidate(candidate):
        raise ValueError("Cannot approve a candidate without valid evidence")

    return candidate.model_copy(update={"approved": True})


def send_outreach(candidate: ResearchCandidate) -> ResearchCandidate:
    """Enforce approval before marking outreach as sent."""
    if not candidate.approved:
        raise ValueError("Approval is required before outreach")

    if not validate_candidate(candidate):
        raise ValueError("Cannot send outreach for an unsupported candidate")

    return candidate.model_copy(update={"outreach_sent": True})
