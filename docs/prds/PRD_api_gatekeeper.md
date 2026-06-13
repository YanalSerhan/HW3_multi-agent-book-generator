# PRD: API Gatekeeper Mechanism

## 1. Background
The CrewAI multi-agent pipeline makes hundreds of API calls to LLM providers (OpenAI) and Search tools (Serper, ArXiv) within a few minutes. To prevent HTTP 429 Rate Limit errors and maintain robust execution, a centralized API Gatekeeper is required.

## 2. Requirements
- **Centralized Execution**: All outbound API calls must pass through the `ApiGatekeeper.execute()` method. No direct `requests.get` or `openai.ChatCompletion.create` calls are allowed.
- **Config-Driven Limits**: The system must read rate limits (requests per minute, concurrent max) from `config/rate_limits.json`.
- **FIFO Queuing**: If the concurrent limit is reached, requests must be queued in a FIFO manner, not dropped.
- **Exponential Backoff**: Transient errors (e.g., HTTP 429, 502, 503) must trigger an automatic retry with exponential backoff (e.g., 2s, 4s, 8s).
- **Thread Safety**: The queuing and token bucket algorithm must be thread-safe using `threading.Lock` since agents execute concurrently.

## 3. Configuration Schema
`config/rate_limits.json` must contain:
```json
{
  "rate_limits": {
    "version": "1.00",
    "services": {
      "default": {
        "requests_per_minute": 30,
        "concurrent_max": 5,
        "max_retries": 3
      }
    }
  }
}
```

## 4. Edge Cases & Test Scenarios
- **Burst Traffic**: Simulate 50 concurrent requests. Verify the gatekeeper allows exactly 5 in parallel and queues the rest.
- **Persistent Failure**: Simulate a permanent 401 error. Verify the gatekeeper throws a fatal exception after `max_retries` rather than looping infinitely.
- **Timeout Management**: Ensure queued requests that wait too long eventually time out gracefully.
