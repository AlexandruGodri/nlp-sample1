import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

'''
post-type-id

1 = Question
2 = Answer
3 = Orphaned tag wiki
4 = Tag wiki excerpt
5 = Tag wiki
6 = Moderator nomination
7 = "Wiki placeholder" (seems to only be the election description)
8 = Privilege wiki
'''

def normalize_text(html):
    txt = BeautifulSoup(html, features='html.parser').get_text()
    txt = txt.replace('\n', ' ')

    while '  ' in txt:
        txt = txt.replace('  ', ' ')
    
    return txt.strip()

tree = ET.parse('/opt/data/Posts.xml')
root = tree.getroot()

questions = {}

for child in root:
    row_data = child.attrib

    if row_data['PostTypeId'] == '1':
        questions[row_data['Id']] = {
            'title': row_data['Title'],
            'text': normalize_text(row_data['Body']),
            'tags': list(filter(lambda e: e != '',
                row_data['Tags'].replace('<', '').split('>')
            )),
            'correct_answer_id': row_data.get('AcceptedAnswerId', '-1'),
            'correct_answer': '',
            'other_answers': []
        }
    elif row_data['PostTypeId'] == '2':
        if row_data['ParentId'] not in questions: continue

        answer = normalize_text(row_data['Body'])

        if questions[row_data['ParentId']]['correct_answer_id'] == row_data['Id']:
            questions[row_data['ParentId']]['correct_answer'] = answer
        else:
            questions[row_data['ParentId']]['other_answers'].append(answer)

for qk in questions:
    qv = questions[qk]
    
    with open('/opt/corpus/question_%s.txt' % (qk), 'w+') as h:
        h.write(qv['title'])

    with open('/opt/corpus/text_%s.txt' % (qk), 'w+') as h:
        h.write(qv['text'])

    with open('/opt/corpus/answer_%s.txt' % (qk), 'w+') as h:
        h.write(qv['correct_answer'])

    with open('/opt/corpus/answers_%s.txt' % (qk), 'w+') as h:
        h.write('\n'.join(qv['other_answers']))
