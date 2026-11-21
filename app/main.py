"""FastAPI app for the Veloria technical support assistant.

POST /ask takes {"question": "..."} and returns the assistant's answer, its outcome
(answered, escalate or decline) and the sources it used. GET /health reports whether the
search index and API key are ready.
"""
import logging
import time
from collections.abc import Callable
from contextlib import asynccontextmanager
from pathlib import Path

import anthropic
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.concurrency import run_in_threadpool
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field, field_validator

from app.config import settings
from app.rag_chain import answer_question
from app.retrieval import get_retriever
from app.schema import SupportResponse

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
logger = logging.getLogger("support_assistant")
FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"


def warm_up() -> None:
    """Load the embedding model and search indexes so the first question is not slow."""
    get_retriever()


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.startup_error = None
    if not settings.anthropic_api_key:
        logger.warning("ANTHROPIC_API_KEY is not set in .env; the SDK will look in the environment.")
    started = time.perf_counter()
    try:
        await run_in_threadpool(warm_up)
        logger.info("Search index ready in %.1fs", time.perf_counter() - started)
    except Exception as error:  # keep serving /health so the problem is visible
        logger.exception("Could not load the search index")
        app.state.startup_error = f"{type(error).__name__}: {error}"
    yield


app = FastAPI(
    title="Veloria Technical Support Assistant",
    description="Answers customer questions from Veloria's knowledge base, manuals and past tickets.",
    version="0.1.0",
    lifespan=lifespan,
)


class AskRequest(BaseModel):
    question: str = Field(
        min_length=1,
        max_length=settings.max_question_length,
        examples=["VeloSync shows error VS-1042. What should I do?"],
    )

    @field_validator("question")
    @classmethod
    def not_blank(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Question must not be empty.")
        return value


class ErrorResponse(BaseModel):
    detail: str


def get_answerer() -> Callable[[str], SupportResponse]:
    """The function that answers a question. Tests replace it with a fake."""
    return answer_question


@app.get("/health", tags=["Health"])
async def health(request: Request):
    error = request.app.state.startup_error
    body = {
        "status": "degraded" if error else "ok",
        "model": settings.llm_model,
        "api_key_configured": bool(settings.anthropic_api_key),
        "search_index": "error" if error else "ready",
    }
    if error:
        body["error"] = error
    return JSONResponse(body, status_code=503 if error else 200)


@app.post(
    "/ask",
    tags=["Ask"],
    response_model=SupportResponse,
    responses={502: {"model": ErrorResponse}, 503: {"model": ErrorResponse}},
)
def ask(
    body: AskRequest,
    request: Request,
    answerer: Callable[[str], SupportResponse] = Depends(get_answerer),
) -> SupportResponse:
    # A plain def: answering blocks on retrieval and the Claude call, so FastAPI runs it in a thread.
    if request.app.state.startup_error:
        raise HTTPException(503, "The assistant is not ready: the search index failed to load.")

    started = time.perf_counter()
    try:
        response = answerer(body.question)
    except (anthropic.RateLimitError, anthropic.InternalServerError, anthropic.APIConnectionError) as error:
        logger.warning("Claude unavailable: %r", error)
        raise HTTPException(503, "The assistant is busy right now. Please try again in a minute.") from error
    except anthropic.APIError as error:
        logger.error("Claude API error: %r", error)
        raise HTTPException(502, "The assistant could not answer because of an upstream error.") from error
    except RuntimeError as error:  # Claude returned no parsable answer
        logger.error("No answer: %s", error)
        raise HTTPException(502, "The assistant could not produce an answer. Please try again.") from error

    # Log the outcome and sources, not the question text, which may hold personal details.
    logger.info(
        "ask outcome=%s sources=%s chars=%d latency=%.2fs",
        response.outcome, [s.id for s in response.sources], len(body.question),
        time.perf_counter() - started,
    )
    return response


class FrontendFiles(StaticFiles):
    """Static files that browsers must revalidate on every load (cheap: a 304 when unchanged).

    Without a Cache-Control header, browsers guess how long to cache a file, and can keep
    serving an old style.css or app.js after it changes.
    """

    def file_response(self, *args, **kwargs):
        response = super().file_response(*args, **kwargs)
        response.headers["Cache-Control"] = "no-cache"
        return response


# Serves index.html at / and its style.css and app.js. Mounted last so API routes win.
app.mount("/", FrontendFiles(directory=FRONTEND_DIR, html=True), name="frontend")
