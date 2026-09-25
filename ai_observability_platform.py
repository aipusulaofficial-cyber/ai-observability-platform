"""AI observability: trace events, latency/token accounting and SLO-friendly aggregates."""
from dataclasses import dataclass
@dataclass(frozen=True)
class Event:
 trace_id:str; span_id:str; name:str; latency_ms:float; tokens:int=0; cost:float=0.0; status:str="ok"
class ObservabilityStore:
 def __init__(self): self.events=[]
 def record(self,e):
  if e.latency_ms<0 or e.tokens<0 or e.cost<0: raise ValueError("metrics cannot be negative")
  self.events.append(e)
 def summary(self):
  if not self.events:return {"count":0,"error_rate":0.0,"p95_latency_ms":0.0,"tokens":0,"cost":0.0}
  xs=sorted(e.latency_ms for e in self.events); idx=min(len(xs)-1,max(0,int(.95*len(xs))-1))
  return {"count":len(xs),"error_rate":sum(e.status!="ok" for e in self.events)/len(xs),"p95_latency_ms":xs[idx],"tokens":sum(e.tokens for e in self.events),"cost":round(sum(e.cost for e in self.events),8)}
def main():
 s=ObservabilityStore(); s.record(Event("t1","s1","inference",42,120,.003)); print(s.summary())
if __name__=="__main__":main()
