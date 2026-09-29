from observability_domain import SpanMetric, aggregate
spans=[SpanMetric("api",100,False,100,0.01),SpanMetric("api",200,True,200,0.02),SpanMetric("worker",50,False,50,0.005)]
r=aggregate(spans); report={"count":r["count"],"error_rate":r["error_rate"],"p50_latency_ms":r["p50_latency_ms"],"tokens":r["tokens"],"cost":r["cost"]}
if report!={"count":3,"error_rate":1/3,"p50_latency_ms":100.0,"tokens":350,"cost":0.035}: raise SystemExit(report)
print(report)
