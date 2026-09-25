from dataclasses import dataclass
from statistics import mean

@dataclass(frozen=True)
class SpanMetric:
    service:str; latency_ms:float; error:bool; tokens:int=0; cost:float=0.0

def aggregate(spans:list[SpanMetric])->dict:
    if not spans:return {"count":0,"error_rate":0.0,"p50_latency_ms":0.0,"tokens":0,"cost":0.0}
    lat=sorted(x.latency_ms for x in spans); mid=lat[(len(lat)-1)//2]
    return {"count":len(spans),"error_rate":sum(x.error for x in spans)/len(spans),"p50_latency_ms":mid,"tokens":sum(x.tokens for x in spans),"cost":round(sum(x.cost for x in spans),6)}
