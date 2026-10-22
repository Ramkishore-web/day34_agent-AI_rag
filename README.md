
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
