from src.orchestration.retry_executor import RetryExecutor


def test_retry_executor_success():

    executor = RetryExecutor(max_retries=2)

    result = executor.execute(
        lambda: "Success"
    )

    assert result["success"] is True
    assert result["result"] == "Success"
    assert result["attempts"] == 1


def test_retry_executor_failure():

    executor = RetryExecutor(max_retries=2)

    def failing_operation():

        raise ValueError("Test failure")

    result = executor.execute(
        failing_operation
    )

    assert result["success"] is False
    assert result["attempts"] == 3
    assert "Test failure" in result["error"]