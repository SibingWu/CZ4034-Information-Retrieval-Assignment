# -*- coding: utf-8 -*-
import json
import matplotlib.pyplot as plt
import os
from pathlib import Path

import base64
from io import BytesIO

BASE_DIR = Path(__file__).resolve().parent.parent
fig_save_path = os.path.join(BASE_DIR, 'search/static')

def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    print(image_png)
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph

def draw_count_bar_chart(json_record):
    keyword_records = json_record["facet_counts"]["facet_fields"]["keyword"]
    keywords = []
    counts = []

    for i in range(0, len(keyword_records), 2):
        keyword = keyword_records[i]
        count = keyword_records[i + 1]
        keywords.append(keyword)
        counts.append(count)

    plt.switch_backend('AGG')
    plt.title("Keywords")
    
    fig, ax = plt.subplots(figsize=(20, 10), dpi=100)
    plt.bar(keywords, counts, tick_label=keywords)
    
    #plt.tick_params(label_size = 23)

    # 显示数据标签
    for a, b in zip(keywords, counts):
        plt.text(
            x=a,
            y=b,
            s=b,
            ha='center',
            va='bottom'
        )
    

    graph = get_graph()
    return graph

    #plt.show()



#if __name__ == "__main__":#

    








# bar_chart_json_record = {
#   "responseHeader":{
#     "status":0,
#     "QTime":8,
#     "params":{
#       "q":"*:*",
#       "facet.field":"keyword",
#       "indent":"true",
#       "q.op":"AND",
#       "rows":"0",
#       "spatial":"true",
#       "facet":"true",
#       "_":"1649472049320"
#     }
#   },
#   "response":{"numFound":66856,"start":0,"numFoundExact": True, "docs":[]},
#   "facet_counts":{
#     "facet_queries":{},
#     "facet_fields":{
#       "keyword":[
#         "pandemic",9894,
#         "from",9675,
#         "home",9675,
#         "lockdown",7571,
#         "quarantine",5723,
#         "coronavirus",5000,
#         "covid",4999,
#         "wfh",4999,
#         "workfromhome",4999,
#         "remotework",4996,
#         "work",4991,
#         "working",4987,
#         "distancing",4971,
#         "social",4971,
#         "remoteworking",4229,
#         "wearamask",4071,
#         "workingfromhome",1112,
#         "socialdistancing",584,
#         "socialdistance",49]},
#     "facet_ranges":{},
#     "facet_intervals":{},
#     "facet_heatmaps":{}
#   }
# }

# pie_chart_json_record = {
#   "responseHeader":{
#     "warnings":["Raising facet.mincount from 0 to 1, because field sentiment is Points-based."],
#     "status":0,
#     "QTime":4,
#     "params":{
#       "q":"*:*",
#       "facet.field":"sentiment",
#       "indent":"true",
#       "q.op":"AND",
#       "rows":"0",
#       "spatial":"true",
#       "facet":"true",
#       "_":"1649472049320"}},
#   "response":{"numFound":66856,"start":0,"numFoundExact": True,"docs":[]
#   },
#   "facet_counts":{
#     "facet_queries":{},
#     "facet_fields":{
#       "sentiment":[
#         "2.0",40466,
#         "0.0",18608,
#         "4.0",7782]
#     },
#     "facet_ranges":{},
#     "facet_intervals":{},
#     "facet_heatmaps":{}
#   }
# }


