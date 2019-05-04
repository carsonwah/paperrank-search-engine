from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from elasticsearch.exceptions import TransportError
import json
import os


class ElasticObj:
    def __init__(self, index_name, index_type):
        """
        index_name: 索引名称
        index_type: 索引类型
        """
        self.index_name = index_name
        self.index_type = index_type
        # 无用户名密码状态
        self.es = Elasticsearch(['localhost'], port=9200)
        # 用户名密码状态
        # self.es = Elasticsearch([ip],http_auth=('elastic', 'password'),port=9200)

    def create_index(self):
        # 创建映射
        index_mappings = {

            "mappings": {
                self.index_type: {
                    "properties": {
                        "id": {  # S2 generated research paper ID.
                            'type': 'keyword'
                        },
                        "title": {  # Research paper title.
                            'type': 'text',
                            'analyzer': 'snowball'
                        },
                        "paperAbstract": {  # Extracted abstract of the paper.
                            'type': 'text',
                            'analyzer': 'snowball'
                        },
                        "entities": {  # Extracted list of relevant entities or topics
                            'type': 'text', 'index_name': 'entity'
                        },
                        "s2Url": {  # URL to S2 research paper details page.
                            'type': 'string',
                            'index': 'not_analyzed'
                        },
                        "s2PdfUrl": {  # URL to PDF on S2 if available.
                            'type': 'string',
                            'index': 'not_analyzed'
                        },
                        "pdfUrls": {  # URLs related to this PDF scraped from the web.
                            'type': 'string',
                            'index_name': 'pdfUrl',
                            'index': 'not_analyzed'
                        },
                        "authors": {  # List of authors with an S2 generated author ID and name.
                            'type': 'nested',
                            'include_in_parent': True,
                            'properties': {
                                "ids": {"type": 'keyword'},
                                "name": {"type": 'text'}
                            }
                        },
                        "inCitations": {  # List of S2 paper IDs which cited this paper.
                            'type': 'string',
                            'index_name': 'inCitation',
                            'index': 'not_analyzed'

                        },
                        "outCitations": {  # List of S2 paper IDs which this paper cited.
                            'type': 'string',
                            'index_name': 'outCitation',
                            'index': 'not_analyzed'
                        },
                        "year": {  # Year this paper was published as integer.
                            'type': 'date',
                            'index': 'not_analyzed'
                        },
                        "venue": {  # Extracted publication venue for this paper.
                            'type': 'text'
                        },
                        "journalName": {  # Name of the journal that published this paper.
                            'type': 'text',
                            'analyzer': 'standard'
                        },
                        "journalVolume": {  # The volume of the journal where this paper was published.
                            'type': 'text',
                            'index': 'not_analyzed'
                        },
                        "journalPages": {  # The pages of the journal where this paper was published.
                            'type': 'text',
                            'index': 'not_analyzed'
                        },
                        "sources": {  # Identifies papers sourced from DBLP or Medline.
                            'type': 'text',
                            'index_name': 'source'
                        },
                        "doi": {  # Digital Object Identifier registered at doi.org.
                            'type': 'string',
                            'index': 'not_analyzed'
                        },
                        "doiUrl ": {  # DOI link for registered objects.
                            'type': 'string',
                            'index': 'not_analyzed'
                        },
                        "pmid": {  # Unique identifier used by PubMed.
                            'type': 'string',
                            'index': 'not_analyzed'
                        },
                        "pagerank":{ #pagerank score
                             'type': 'rank_feature'
                        }
                    }
                }
            }
        }

        try:
            self.es.indices.create(
                index=self.index_name,
                body=index_mappings, ignore=[400, 404])
        except TransportError as e:
            # ignore already existing index
            if e.error == 'index_already_exists_exception':
                pass
            else:
                raise

    # 插入数据
    def insert_data(self, inputfile):
        path1=os.path.abspath('.') 
        f = open(path1+inputfile, 'r', encoding='UTF-8')

        ACTIONS = []
        i = 1
        bulk_num = 2000
        for list_line in f.readlines():
            action = {
                "_index": self.index_name,
                "_type": self.index_type,
                "_id": i,  # _id 也可以默认生成，不赋值
                "_source": json.loads(list_line)
            }
            i += 1
            ACTIONS.append(action)
            # 批量处理
            if len(ACTIONS) == bulk_num:
                print('index data', int(i)-2001,'-',int(i)-1)
                success, _ = bulk(self.es, ACTIONS, index=self.index_name, raise_on_error=True)
                del ACTIONS[0:len(ACTIONS)]

        if len(ACTIONS) > 0:
            success, _ = bulk(self.es, ACTIONS, index=self.index_name, raise_on_error=True)
            del ACTIONS[0:len(ACTIONS)]
            print('Performed %d actions' % success)
            
        f.close()


if __name__ == '__main__':
    obj = ElasticObj("academic", "article")
    obj.create_index()
    obj.insert_data('/pagerank_result.json')
