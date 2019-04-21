
# coding: utf-8
from elasticsearch import Elasticsearch

def do_the_search(query):
    #使用TF-IDF计算相似度
    body = {
        "query":{
            "bool":{
                "must":{
                    #文档与query匹配的条件（必须满足）：
                    "multi_match": {
                        "fields": [ "title","paperAbstract"], 
                        "query" : query,
                        "analyzer":"snowball",#query和文档都使用snowball analyzer
                        "fuzziness": "AUTO", #模糊匹配
                        "minimum_should_match":"75%"#指定匹配的term数
                    }
                }, 
                #如果与query能完全匹配，score更高
                "should":[
                    {"match_phrase":{
                        "title":{
                            "query" : query,
                            "slop":5,#phrase中term距离<=5的score更高      
                            "boost":2 # 在title中匹配的重要性是paperAbstract中的2倍
                            }
                        } 
                    },
                    {"match_phrase":{
                        "paperAbstract":{
                            "query" : query,
                            "slop":5,#phrase中term距离<=5的score更高 
                            }
                        }
                    }
                ]
            }
        }
    }
    es=Elasticsearch()
    search = es.search(index="academic", doc_type="article",body=body)
    
    return search

if __name__ == '__main__':
    
    search=do_the_search("Hypertrophic cardiomyopathy")
    title = [str(hit['_source']['title']) for hit in search['hits']['hits']]
    scores = [hit['_score'] for hit in search['hits']['hits']]
    url = [str(hit['_source']['s2Url']) for hit in search['hits']['hits']]

    for i in range(len(search)):
        print('result',i+1,':','score:',scores[i])
        print('title:',title[i])
        print('url:',url[i])
        print('--------------------------------------------------------------')

