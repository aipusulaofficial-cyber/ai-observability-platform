from fastapi import FastAPI
from pydantic import BaseModel
from opentelemetry import trace
try:
 from opentelemetry.sdk.resources import Resource
 from opentelemetry.sdk.trace import TracerProvider
 from opentelemetry.sdk.trace.export import BatchSpanProcessor,ConsoleSpanExporter
 p=TracerProvider(resource=Resource.create({"service.name":"ai-observability-platform"}));p.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()));trace.set_tracer_provider(p)
except Exception: pass
tracer=trace.get_tracer("ai-observability-platform");app=FastAPI(title="ai-observability-platform",version="1.0.0")
class Request(BaseModel): key:str; payload:dict={}
@app.get("/health/live")
def live():return {"status":"ok"}
@app.get("/health/ready")
def ready():return {"status":"ready"}
@app.post("/v1/observability")
def handle(r:Request):
 with tracer.start_as_current_span("observability") as s:s.set_attribute("request.key",r.key)
 return {"status":"accepted","key":r.key}
