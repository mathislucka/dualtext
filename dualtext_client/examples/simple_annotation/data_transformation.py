import json
import os
from datasets import load_dataset
import argparse


def make_search_project_data(p_name, corpus_name, annotation_mode, data, use_yes_no=False):
    project = {
        'name': p_name,
        'corpora': [1],
        'annotation_mode': annotation_mode,
        'max_documents': 1 if annotation_mode == 'grouped' else 2
    }

    corpus = {
        'name': corpus_name,
        'corpus_meta': {'source': 'germandpr'}
    }

    if annotation_mode == 'grouped':
        labels = [
            {'name': 'anchor', 'key_code': 'a'},
            {'name': 'positive', 'key_code': 'p'},
            {'name': 'hard negative', 'key_code': 'h'},
        ]
        annotations = [
            {'identifier': 1, 'labels': ['anchor']},
            {'identifier': 2, 'labels': ['positive']},
            {'identifier': 3, 'labels': ['hard negative']},
            {'identifier': 4, 'labels': ['anchor']},
            {'identifier': 5, 'labels': ['positive']},
            {'identifier': 6, 'labels': ['hard negative']}
        ]
        annotation_groups = [
            {'annotation_ids': [1, 2, 3]},
            {'annotation_ids': [4, 5, 6]}
        ]
    else:
        if use_yes_no:
            labels = [
                {'name': 'similar', 'key_code': 'y'},
                {'name': 'not similar', 'key_code': 'n'}
            ]
        else:
            labels = [
                {'name': 'similarity 5', 'key_code': 'q'},
                {'name': 'similarity 4', 'key_code': 'w'},
                {'name': 'similarity 3', 'key_code': 'e'},
                {'name': 'similarity 2', 'key_code': 'r'},
                {'name': 'similarity 1', 'key_code': 't'},
                {'name': 'similarity 0', 'key_code': 'y'},
            ]
        annotations = [
            {'identifier': 1, 'labels': []},
            {'identifier': 2, 'labels': []},
            {'identifier': 3, 'labels': []},
            {'identifier': 4, 'labels': []},
            {'identifier': 5, 'labels': []},
            {'identifier': 6, 'labels': []},
            {'identifier': 7, 'labels': []},
            {'identifier': 8, 'labels': []},
            {'identifier': 9, 'labels': []},
            {'identifier': 10, 'labels': []}
        ]

    documents = []
    for idx in range(1,1000):
        row = data[idx]
        if idx < 2 and annotation_mode == 'grouped':
            docs = [
                {'content': row['question'], 'annotation_identifier': idx},
                {'content': row['positive_ctxs']['text'][0], 'annotation_identifier': idx+1},
                {'content': row['hard_negative_ctxs']['text'][0], 'annotation_identifier': idx + 2},
            ]
            documents.extend(docs)
        elif idx < 10 and annotation_mode == 'dualtext':
            documents.append({'content': row['question'], 'annotation_identifier': idx})
        elif idx < 20 and annotation_mode == 'classification':
            documents.extend([
                {'content': row, 'annotation_identifier': idx},
                {'content': data[idx+1], 'annotation_identifier': idx}
            ])
        else:
            documents.append({'content': row})

    collection = {
        'project': project,
        'corpus': corpus,
        'labels': labels,
        'annotations': annotations,
        'documents': documents
    }

    if annotation_mode == 'grouped':
        collection['annotation_groups'] = annotation_groups

    out_path = os.path.join(os.getcwd(), f'{annotation_mode}_germandpr.json')

    with open(out_path, 'w') as f:
        f.write(json.dumps(collection))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Creating dualtext data')

    parser.add_argument('-p', dest='project', type=str)
    parser.add_argument('-c', dest='corpus', type=str)
    parser.add_argument('-a', dest='annotation', type=str)
    parser.add_argument('-y', dest='yes_no', type=bool)
    args = parser.parse_args()
    paragraphs = []
    with open('paragraphs.jsonl', 'r') as f:
        for line in f:
            paragraphs.append(json.loads(line.strip())['text'])
    make_search_project_data(
        data=paragraphs,
        p_name=args.project,
        corpus_name=args.corpus,
        annotation_mode=args.annotation,
        use_yes_no=args.yes_no
    )


