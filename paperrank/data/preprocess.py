import os
import json


if __name__ == "__main__":
    with open('../../data/static/sample.json', 'r', encoding='UTF-8') as data:

        # Construct paper dict
        paper_out_citations_dict = {}
        paper_count = 0
        for line in data:
            paper_count += 1
            paper = json.loads(line)
            if not paper['id']:
                print('{}th paper has no id.'.format(paper_count))
                continue
            if type(paper['outCitations']) is not list or not paper['outCitations']:
                print('{}th paper has no out citation.'.format(paper_count))
                continue
            paper_out_citations_dict[paper['id']] = paper['outCitations']

        print('Successfully processed {} papers'.format(paper_count))

    with open('./citations.csv', 'w') as output:
        print('Start writing into csv...')
        row_count = 0
        for paper_id, out_citations in paper_out_citations_dict.items():
            for cited_paper_id in out_citations:
                if cited_paper_id in paper_out_citations_dict:
                    # The cited paper exists in our dataset
                    # Write to csv
                    output.write('{},0,{},1\n'.format(paper_id, cited_paper_id))
                    row_count += 1

    print('Successful! Written {} rows into citations.csv'.format(row_count))
