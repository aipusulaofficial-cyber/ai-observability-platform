from ai_observability_platform import *
import pytest
def test_summary_aggregates_usage_and_errors():
 s=ObservabilityStore(); s.record(Event("t","1","x",10,100,.01)); s.record(Event("t","2","x",20,50,.02,"error"))
 x=s.summary(); assert x["count"]==2 and x["tokens"]==150 and x["error_rate"]==.5
def test_negative_metrics_rejected():
 with pytest.raises(ValueError): ObservabilityStore().record(Event("t","s","x",-1))
def test_empty_summary_is_safe(): assert ObservabilityStore().summary()["count"]==0
