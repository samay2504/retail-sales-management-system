"""Middleware for request tracking, rate limiting, and security."""
import time
import uuid
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Callable
from fastapi import Request, Response, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from src.utils.logging import get_logger

logger = get_logger(__name__)


class RequestIDMiddleware(BaseHTTPMiddleware):
    """Add unique request ID to each request."""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id
        
        # Add to logging context
        logger.info(
            "Request started",
            extra={
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
                "client": request.client.host if request.client else None,
            },
        )
        
        start_time = time.time()
        response = await call_next(request)
        duration = time.time() - start_time
        
        # Add request ID to response headers
        response.headers["X-Request-ID"] = request_id
        
        logger.info(
            "Request completed",
            extra={
                "request_id": request_id,
                "duration": f"{duration:.3f}s",
                "status_code": response.status_code,
            },
        )
        
        return response


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Simple rate limiting middleware."""
    
    def __init__(self, app: ASGIApp, requests_per_minute: int = 60):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self.requests: dict = defaultdict(list)
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Get client IP
        client_ip = request.client.host if request.client else "unknown"
        
        # Clean old requests
        now = datetime.utcnow()
        cutoff = now - timedelta(minutes=1)
        self.requests[client_ip] = [
            req_time for req_time in self.requests[client_ip] if req_time > cutoff
        ]
        
        # Check rate limit
        if len(self.requests[client_ip]) >= self.requests_per_minute:
            logger.warning(f"Rate limit exceeded for IP: {client_ip}")
            raise HTTPException(
                status_code=429,
                detail="Too many requests. Please try again later.",
            )
        
        # Add current request
        self.requests[client_ip].append(now)
        
        response = await call_next(request)
        
        # Add rate limit headers
        response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
        response.headers["X-RateLimit-Remaining"] = str(
            self.requests_per_minute - len(self.requests[client_ip])
        )
        
        return response


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Add security headers to responses."""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        response = await call_next(request)
        
        # Security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        
        # Cache headers for API responses
        if request.url.path.startswith("/api/"):
            response.headers["Cache-Control"] = "public, max-age=30"
            # Only add ETag for non-streaming responses
            if hasattr(response, "body"):
                response.headers["ETag"] = f'"{hash(str(response.body))}"'
        
        return response
