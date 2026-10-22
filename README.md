
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
