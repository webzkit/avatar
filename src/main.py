from fastapi import HTTPException, Request
from starlette.middleware.cors import CORSMiddleware
from typing import Any, Dict

from config import settings
from apis.api import api_router
from core.setup import create_application
from core.trace.jaeger import tracing

from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.sampling import ParentBasedTraceIdRatio
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.propagate import extract
from opentelemetry.trace.status import Status, StatusCode
import logging
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

# Configure tracing with sampling
"""
sampler = ParentBasedTraceIdRatio(0.3)
trace.set_tracer_provider(
    TracerProvider(
        resource=Resource.create(
            {
                "service.name": "avatar",
                "service.version": "0.1.0",
                "deployment.environment": "development",
            }
        ),
        sampler=sampler,
    )
)
jaeger_exporter = JaegerExporter(agent_host_name="jaeger", agent_port=6831)
trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(jaeger_exporter))
"""

resource = Resource(attributes={"service.name": "fastapi-service"})
tracer_provider = TracerProvider(resource=resource)
trace.set_tracer_provider(tracer_provider)
# Set up OTLP exporter for traces
otlp_exporter = OTLPSpanExporter(endpoint="otel-collector:4317", insecure=True)
span_processor = BatchSpanProcessor(otlp_exporter)
tracer_provider.add_span_processor(span_processor)
# Set up logging
logging.basicConfig(
    filename="app.log",
    filemode="a",
    format="%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s",
    datefmt="%H:%M:%S",
    level=logging.DEBUG,
)
logger = logging.getLogger(__name__)


# Init application
app = create_application(router=api_router, settings=settings)

# FastAPIInstrumentor.instrument_app(app)
# RequestsInstrumentor().instrument()
FastAPIInstrumentor.instrument_app(app)
# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        # allow_origins=[str(origin)
        #               for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.get("/check_health")
# @tracing()
async def check(request: Request) -> Any:
    logger.info("Root endpoint accessed")
    result: Dict[Any, Any] = {
        "status": "Check Healt",
        "message": f"Your {settings.APP_NAME} endpoint is working",
    }

    return result


"""
@app.get("/health")
async def root(request: Request) -> Any:
    context = extract(request.headers)
    tracer = trace.get_tracer(__name__)
    print(tracer)

    with tracer.start_as_current_span("process_request", context=context) as span:
        try:
            span.set_attributes({"endpoint": "/health", "processing.type": "standard"})

            result: Dict[Any, Any] = {
                "status": "Healthy",
                "message": f"Your {settings.APP_NAME} endpoint is working",
            }

            span.set_attributes(
                {"processing.success": True, "result.size": len(str(result))}
            )

            return result
        except Exception as e:
            span.set_status(Status(StatusCode.ERROR))
            span.record_exception(e)
            raise HTTPException(status_code=500, detail="Internal Server Error")
"""
