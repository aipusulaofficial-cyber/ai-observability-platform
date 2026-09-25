from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from opentelemetry import trace
from observability_domain import *
try:
 from opentelemetry.sdk.resources import Resource
 from opentelemetry.sdk.trace import TracerProvider
 from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
 p=TracerProvider(resource=Resource.create({"service.name":"ai-observability-platform"}));p.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()));trace.set_tracer_provider(p)
except Exception: pass
app=FastAPI(title="ai-observability-platform",version="1.0.0");tracer=trace.get_tracer("ai-observability-platform")
class Request(BaseModel): key:str; payload:dict={}
@app.get("/health/live")
def live(): return {"status":"ok"}
@app.get("/health/ready")
def ready(): return {"status":"ready"}
@app.post("/v1/observability")
def handle(r:Request):
 with tracer.start_as_current_span("ai-observability-platform.domain"):
  try: x=aggregate([SpanMetric(r.key,float(r.payload.get("latency_ms",0)),bool(r.payload.get("error",False)),int(r.payload.get("tokens",0)),float(r.payload.get("cost",0))) ]); return x
  except (ValueError,KeyError) as e: raise HTTPException(status_code=400,detail=str(e)) from e
