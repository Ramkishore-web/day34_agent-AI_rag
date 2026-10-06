from datetime import datetime
from typing import Any, Dict, List, Optional


class ExecutionTracker:
    """
    Tracks execution of agents in the multi-agent workflow.
    """

    def __init__(self):
        self.history: List[Dict[str, Any]] = []

    def _now(self) -> str:
        return datetime.now().isoformat()

    # =====================================================
    # START AGENT
    # =====================================================

    def start_agent(
        self,
        agent_name: str
    ) -> Dict[str, Any]:

        event = {
            "agent": agent_name,
            "status": "started",
            "start_time": self._now(),
        }

        self.history.append(event)

        return event

    # =====================================================
    # COMPLETE AGENT
    # =====================================================

    def complete_agent(
        self,
        agent_name: str,
        start_time: Optional[str] = None
    ) -> Dict[str, Any]:

        end_time = self._now()

        event = {
            "agent": agent_name,
            "status": "completed",
            "start_time": start_time,
            "end_time": end_time,
        }

        if start_time:

            try:

                start = datetime.fromisoformat(
                    start_time
                )

                end = datetime.fromisoformat(
                    end_time
                )

                event["duration_seconds"] = (
                    end - start
                ).total_seconds()

            except Exception:

                event["duration_seconds"] = 0.0

        else:

            event["duration_seconds"] = 0.0

        self.history.append(event)

        return event

    # =====================================================
    # FAIL AGENT
    # =====================================================

    def fail_agent(
        self,
        agent_name: str,
        error: str,
        attempt: int = 1
    ) -> Dict[str, Any]:

        event = {
            "agent": agent_name,
            "status": "failed",
            "error": error,
            "attempt": attempt,
            "time": self._now(),
        }

        self.history.append(event)

        return event

    # =====================================================
    # GET EVENTS
    # =====================================================

    def get_events(
        self
    ) -> List[Dict[str, Any]]:

        return self.history

    # =====================================================
    # GET HISTORY
    # =====================================================

    def get_history(
        self
    ) -> List[Dict[str, Any]]:

        return self.history

    # =====================================================
    # CLEAR
    # =====================================================

    def clear(self):

        self.history.clear()


def create_execution_tracker():

    return ExecutionTracker()