from src.orchestration.execution_tracker import (
    ExecutionTracker
)


def test_execution_tracker_start():

    tracker = ExecutionTracker()

    event = tracker.start_agent(
        "Researcher"
    )

    assert event["agent"] == "Researcher"
    assert event["status"] == "started"

    assert len(
        tracker.get_events()
    ) == 1


def test_execution_tracker_complete():

    tracker = ExecutionTracker()

    started = tracker.start_agent(
        "RAG"
    )

    completed = tracker.complete_agent(
        "RAG",
        started["start_time"]
    )

    assert completed["agent"] == "RAG"
    assert completed["status"] == "completed"

    assert (
        completed["duration_seconds"] >= 0
    )


def test_execution_tracker_failure():

    tracker = ExecutionTracker()

    event = tracker.fail_agent(
        "Analyst",
        "Test failure",
        2
    )

    assert event["agent"] == "Analyst"
    assert event["status"] == "failed"
    assert event["attempt"] == 2


def test_execution_tracker_clear():

    tracker = ExecutionTracker()

    tracker.start_agent(
        "Writer"
    )

    assert len(
        tracker.get_events()
    ) == 1

    tracker.clear()

    assert len(
        tracker.get_events()
    ) == 0