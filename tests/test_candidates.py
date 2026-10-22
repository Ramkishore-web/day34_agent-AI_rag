
import pytest

from src.workflow.candidates import (
    EvidenceSource,
    ResearchCandidate,
    validate_candidate,
    approve_candidate,
    send_outreach,
)


def make_candidate():
    return ResearchCandidate(
        candidate_id="candidate-001",
        description="Python documentation research candidate",
        evidence=[
            EvidenceSource(
                url="https://docs.python.org/3/",
                supporting_excerpt="Official Python documentation",
            )
        ],
    )


def test_candidate_with_evidence_is_valid():
    assert validate_candidate(make_candidate()) is True


def test_candidate_without_evidence_is_rejected():
    candidate = ResearchCandidate(
        candidate_id="candidate-002",
        description="Unsupported candidate",
        evidence=[],
    )
    assert validate_candidate(candidate) is False


def test_http_source_is_rejected():
    candidate = ResearchCandidate(
        candidate_id="candidate-003",
        description="Invalid source candidate",
        evidence=[
            EvidenceSource(
                url="http://example.com",
                supporting_excerpt="Example excerpt",
            )
        ],
    )
    assert validate_candidate(candidate) is False


def test_outreach_requires_approval():
    with pytest.raises(ValueError, match="Approval is required"):
        send_outreach(make_candidate())


def test_approved_candidate_can_be_marked_for_outreach():
    approved = approve_candidate(make_candidate())
    result = send_outreach(approved)

    assert approved.approved is True
    assert result.outreach_sent is True


def test_unsupported_candidate_cannot_be_approved():
    candidate = ResearchCandidate(
        candidate_id="candidate-004",
        description="No source available",
        evidence=[],
    )

    with pytest.raises(ValueError, match="valid evidence"):
        approve_candidate(candidate)
