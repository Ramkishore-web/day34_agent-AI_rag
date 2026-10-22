
from src.workflow.state_machine import WorkflowState
from src.workflow.trace import WorkflowTrace


def test_trace_records_workflow_events():
    trace = WorkflowTrace(run_id="run-001")

    trace.record(WorkflowState.PLANNING, "Planning started")
    trace.record(WorkflowState.RESEARCHING, "Research started")
    trace.record(WorkflowState.COMPLETED, "Workflow completed")

    output = trace.to_dict()

    assert output["run_id"] == "run-001"
    assert len(output["events"]) == 3
    assert output["events"][0]["state"] == "planning"
    assert output["events"][-1]["state"] == "completed"
    assert output["events"][0]["timestamp"]
