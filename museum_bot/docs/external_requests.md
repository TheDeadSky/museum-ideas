# External Requests API

This document describes the external request endpoints that allow other services to send messages to users through the Telegram bot.

## Overview

The bot now supports external HTTP requests to send messages to users. This is useful for:
- Sending feedback responses to users
- Sending notifications
- Sending any custom messages from external services

## Endpoints

### 1. Send Feedback Response

**Endpoint:** `POST /api/send-feedback-response`

**Description:** Send a response to a user's feedback

**Request Body:**
```json
{
    "user_id": "123456789",
    "response_text": "Thank you for your feedback! We appreciate your input.",
    "feedback_id": "fb_12345"
}
```

**Parameters:**
- `user_id` (required): Telegram user ID to send the response to
- `response_text` (required): The response text to send
- `feedback_id` (optional): Original feedback ID for reference

**Response:**
```json
{
    "success": true,
    "message": "Feedback response sent successfully",
    "user_id": "123456789",
    "feedback_id": "fb_12345"
}
```

### 2. Send Generic Message

**Endpoint:** `POST /api/send-message`

**Description:** Send any message to a user

**Request Body:**
```json
{
    "user_id": "123456789",
    "message": "Hello! This is a test message."
}
```

**Parameters:**
- `user_id` (required): Telegram user ID to send the message to
- `message` (required): The message text to send

**Response:**
```json
{
    "success": true,
    "message": "Message sent successfully",
    "user_id": "123456789"
}
```

## Error Handling

Both endpoints return error responses in the following format:

```json
{
    "success": false,
    "error": "Error description"
}
```

Common error scenarios:
- Invalid user ID
- User has blocked the bot
- Network errors
- Invalid request format

## Usage Examples

### Python Example

```python
import aiohttp
import asyncio

async def send_feedback_response():
    payload = {
        "user_id": "123456789",
        "response_text": "Thank you for your feedback!",
        "feedback_id": "fb_12345"
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(
            "http://localhost:3000/api/send-feedback-response",
            json=payload
        ) as response:
            result = await response.json()
            print(result)

# Run the example
asyncio.run(send_feedback_response())
```

### cURL Example

```bash
# Send feedback response
curl -X POST http://localhost:3000/api/send-feedback-response \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "123456789",
    "response_text": "Thank you for your feedback!",
    "feedback_id": "fb_12345"
  }'

# Send generic message
curl -X POST http://localhost:3000/api/send-message \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "123456789",
    "message": "Hello from external service!"
  }'
```

## Integration with Existing Services

The bot also provides service functions in `services/api_service.py` for easier integration:

```python
from services.api_service import send_feedback_response_to_user, send_message_to_user

# Send feedback response
await send_feedback_response_to_user(
    user_id="123456789",
    response_text="Thank you for your feedback!",
    feedback_id="fb_12345"
)

# Send generic message
await send_message_to_user(
    user_id="123456789",
    message="Hello from service!"
)
```

## Security Considerations

- The endpoints are currently open and should be protected in production
- Consider adding authentication (API keys, JWT tokens, etc.)
- Validate user IDs to prevent abuse
- Rate limiting should be implemented for production use

## Configuration

The bot server runs on the port specified by the `WEBAPP_PORT` environment variable (default: 3000).

To change the base URL for external requests, update the `API_BASE_URL` environment variable in your service calls. 