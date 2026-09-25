from observability_domain import *
def test_aggregate():
 x=aggregate([SpanMetric("a",10,False,100,.2),SpanMetric("a",20,True,50,.1)]);assert x["error_rate"]==.5 and x["tokens"]==150