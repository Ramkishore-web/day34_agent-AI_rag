
from urllib.parse import urlparse

from src.workflow.schemas import ResearchResult


def validate_result(result: ResearchResult) -> bool:
    """Reject results without valid HTTPS source URLs."""

    if not result.answer.strip():
        return False

    for url in result.evidence_urls:
        parsed = urlparse(url)

        if parsed.scheme != "https" or not parsed.netloc:
            return False

    return True
