
## Day 2 — Tool Execution Safety and Resilience

### Implemented
- Async tool execution with configurable timeout.
- Bounded retries for timeout and execution failures.
- Output validation before accepting tool results.
- In-process idempotency cache for successful results.
- Workflow CANCELLED terminal state.
- Automated tests for success, timeout, malformed output,
  cached results, and invalid state transitions.

### Run tests
```powershell
python -m pytest -v
```

### Limitations
- Idempotency cache is in-memory and does not survive restarts.
- Concurrent duplicate calls are not fully coordinated.
- Cancellation requires explicit integration with the workflow.
- Tools with external side effects need their own idempotency
  mechanism and safe cancellation strategy.


## Day 3 — Evidence-Grounded Outputs and Persistence

### Objective
Validate research inputs, preserve evidence provenance, and persist workflow results consistently.

### Implementation
- Validate evidence URLs before research execution.
- Reject candidates without valid HTTPS evidence and supporting excerpts.
- Require explicit approval before marking outreach as sent.
- Persist successful, failed, and cancelled workflow snapshots.
- Record workflow state transitions and timestamps in the trace.
- Use atomic JSON file replacement for persisted records.

### Run the Workflow
```powershell
python -m src.workflow.main
```

### Run Tests
```powershell
python -m pytest -v
```

### Persistence Location
Workflow records are stored in `data/runs/` as JSON files.

### Known Limitations
- URL validation does not fetch webpages or prove that a source supports a claim.
- Candidate excerpts are not yet verified against the original webpage.
- Outreach updates local state only; no email or external message is sent.
- JSON file persistence is suitable for this project stage, not concurrent multi-server production use.
- Tool result caching is process-local.

### Security and Safety
- Candidates without evidence are rejected.
- Outreach requires explicit approval.
- Workflow snapshots preserve status, evidence URLs, and execution traces.


## Day 4 — Observability, Metrics, and Evaluation

### Implemented
- Workflow traces with state transitions and timestamps.
- Correlation ID and run ID tracking.
- Metrics for latency, tool calls, tool failures, and workflow status.
- Regression evaluation dataset and report generation.
- Evaluation metrics for completion, duplicate outputs, failure handling, and evidence presence.

### Run Evaluation
```powershell
python scripts/run_evaluation.py
```

### Run Tests
```powershell
python -m pytest -q
```

### Known Limitations
- Evidence presence is only a grounding proxy; it does not verify factual correctness.
- Token usage and estimated cost are not populated unless connected to an actual model provider.
- Current runtime metrics do not represent production service-level monitoring.

## Day 5 — Agent Capstone and Recovery Drill

### Implemented
- Persistence tests for saving and loading workflow snapshots.
- Tests for invalid run IDs and malformed stored JSON.
- Simulated persistence failure and temporary-file cleanup checks.
- Tool failure and timeout retry tests.
- Invalid tool output validation tests.
- Successful-result cache verification.

### Run All Tests
```powershell
python -m pytest -v
```

### Run Evaluation
```powershell
python scripts/run_evaluation.py
```

### Recovery Scenarios
1. Happy path — verify successful workflow completion.
2. Source failure — verify bounded retries and error handling.
3. Duplicate candidate — verify duplicate validation behavior.
4. Invalid schema — verify malformed handoffs are rejected.
5. Persistence failure — verify save errors are handled and temporary files are cleaned up.

### Known Limitations
- Failure tests simulate errors; they do not prove recovery from every real infrastructure failure.
- The tool-result cache is in-memory and does not survive process restarts.
- Concurrent duplicate calls are not fully coordinated.
- JSON persistence is intended for a development project, not concurrent multi-server production workloads.
- Evidence URL validation does not prove that a source supports the generated answer.
- Token usage and model cost require provider integration.

## Final Validation Evidence

Run the following commands from the project root:

```powershell
python -m pytest -v
python scripts/run_evaluation.py
git status
```

Record the actual test results and evaluation report. Do not claim a scenario passed unless the corresponding test or workflow execution confirms it.

## Recovery Runbook

- **Tool timeout or source failure:** inspect the error, verify retry limits, and rerun with a safe test input.
- **Invalid handoff or output:** inspect schema validation errors; do not bypass validation.
- **Duplicate candidate:** inspect candidate identity and evidence before accepting the result.
- **Persistence failure:** check the storage directory, file permissions, disk space, and temporary-file cleanup.
- **Incorrect or unsupported research answer:** review evidence URLs and excerpts; do not treat URL presence alone as proof of correctness.
- **Sensitive data:** never commit API keys, credentials, personal data, or client-confidential information.
