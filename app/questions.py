from app import db
from app.models import Question, Option, Answer, Response
from copy import deepcopy
from random import choice, shuffle
from catsim.cat import generate_item_bank

import glob, os, json, numpy

org_qns = {
    "Fill in the blank: 423 x 1000 = ____ x 10": {
        "answers": [
            "42300",
            "423",
            "4230",
            "423000"
        ],
        "difficulty": "Easy"
    },
    "Which of the following is closest to 1?": {
        "answers": [
            "4/5",
            "1/2",
            "2/3",
            "3/4"
        ],
        "difficulty": "Easy"
    },
    "Which of the following is the same as 2010 g?": {
        "answers": [
            "2 kg 10 g",
            "2 kg 1 g",
            "20 kg 1 g",
            "20 kg 10 g"
        ],
        "difficulty": "Easy"
    },
    "Find the value of (3y +1) / 4 , when y = 5": {
        "answers": [
            "4",
            "9",
            "8",
            "5"
        ],
        "difficulty": "Easy"
    },
    "The ratio of Rachel's age to Samy's age is 7 : 6.  Rachel is 4 years older than Samy. What is Samy's age this year?": {
        "answers": [
            "24",
            "10",
            "11",
            "28"
        ],
        "difficulty": "Easy"
    },
    "How many fifths are there in 2 3/5?": {
        "answers": [
            "13",
            "11",
            "3",
            "6"
        ],
        "difficulty": "Easy"
    },
    "The sum of 1/2 and 2/5 is the same as ___.": {
        "answers": [
            "0.900",
            "0.009",
            "0.090",
            "9.000"
        ],
        "difficulty": "Easy"
    },
    "What is the value of 36 + 24 / (9 - 3) + 2 x 5 ?": {
        "answers": [
            "50",
            "51",
            "60",
            "66"
        ],
        "difficulty": "Easy"
    },
    "Sally has 100 marbles and her brother has 300 marbles. Express Sally's marbles as a percentage of the total number of marbles they have altogether.": {
        "answers": [
            "25%",
            "33 1/3 %",
            "300%",
            "400%"
        ],
        "difficulty": "Easy"
    },
    "Mr Tan has an equal number of pens and pencils. He puts the pens in bundles of 8 and the pencils in bundles of 12. There are 15 bundles altogether. How many pens are there?": {
        "answers": [
            "72",
            "24",
            "48",
            "96"
        ],
        "difficulty": "Hard"
    },
    "3 ones, 4 tenths and 7 thousandths is ___": {
        "answers": [
            "3.407",
            "3.470",
            "3.047",
            "3.740"
        ],
        "difficulty": "Hard"
    },
    "Which of the following is equal to 0.25%?": {
        "answers": [
            "1/400",
            "1/25",
            "1/4",
            "25"
        ],
        "difficulty": "Hard"
    }
}

def remove_qn():
    for q in Question.query.all():
        db.session.delete(q)
        db.session.commit()
    for q in Option.query.all():
        db.session.delete(q)
        db.session.commit()
    for q in Answer.query.all():
        db.session.delete(q)
        db.session.commit()

def clear_responses():
    for r in Response.query.all():
        db.session.delete(r)
    db.session.commit()

def add_qn():
    remove_qn()
    if Question.query.all(): return
    for q in org_qns.keys():
        item = generate_item_bank(1)[0]
        qn = Question(question=q, discrimination=item[0], \
                    difficulty=item[1], guessing=item[2], upper=item[3])
        db.session.add(qn)
        db.session.commit()
        qid = Question.query.filter_by(question=q).first().id
        b=True
        for o in org_qns[q]['answers']:
            opt=Option(qnID=qid,option=o)
            db.session.add(opt)
            if b:
                optID = Option.query.filter_by(option=o).first().id
                ans = Answer(qnID=qid, optID=optID)
                db.session.add(ans)
                b=False
            
            db.session.commit()

#add_qn()

def get_qns():
    d = {}
    questions = Question.query.all()
    for q in questions:
        opt = Option.query.filter_by(qnId=q.id).all()
        d[q.question] = {}
        d[q.question]["answers"] = []
        for o in opt:
            #if (Answer.query.filter(optId=o.Id)):
            #    d[q.question].insert(0, opt.option)
            d[q.question]["answers"].append(o.option)
 
    return d

#og_qns = get_qns()
#qns = deepcopy(og_qns)

def final_qns():
    sh_qns = og_qns.keys()
    shuffle(sh_qns)
    for k in qns.keys():
        shuffle(qns[k]['answers'])
    return sh_qns, qns

#remove_qn()

def insert_qns():
    path = 'app/static/resources/questions'
    qn_dict = {}
    for filename in glob.glob(os.path.join(path, '*.json')):
        print("===")
        print(filename)
        print("===")
        with open(filename, 'r') as f: # open in readonly mode
            data = json.load(f)
            for qn_set in data.values():
                qn_txt = qn_set["question_text"]
                n, qn_text = qn_txt.split(")",1)
                options = qn_set["option_texts"]
                options = [[o[0], o[6:]] for o in options]
                
                answer = qn_set["answer"]
                a, answer = answer.split("Answer / Explanation :\n\nAnswer : ", 1)
                answer, explanation = answer.split(".", 1)

                item = generate_item_bank(1)[0]

                question = Question(question=qn_text, discrimination=item[0], \
                    difficulty=item[1], guessing=item[2], upper=item[3])
                db.session.add(question)

                qid = Question.query.filter_by(question=qn_text).first().id

                for opt in options:
                    o = Option(qnID=qid, option=opt[1])
                    db.session.add(o)
                    if opt[0] == answer:
                        optID = Option.query.filter_by(option=opt[1]).first().id
                        ans = Answer(qnID=qid, optID=optID)
                        db.session.add(ans)

                db.session.commit()

                #print (qn_text)
                #print(options)
                #print(answer)
                #print(explanation)

def test_insert():
    insert_qns()
    questions = Question.query.all()
    for q in questions:
        options = Option.query.filter_by(qnID=q.id)
        answer = Answer.query.filter_by(qnID=q.id).first()
        print(q.question)
        for o in options:
            if o.id == answer.optID:
                ans_opt = o
            print(o.option)

        print("ANS" + o.option)

#test_insert()


def get_items():
    questions = Question.query.all()
    get_dis = lambda x:x.discrimination
    get_diff = lambda x:x.difficulty
    get_guess = lambda x:x.guessing
    get_upp = lambda x:x.upper
    get_params = [get_dis, get_diff, get_guess, get_upp]
    items = [[get(qn) for get in get_params] for qn in questions]
    return numpy.array(items)

clear_responses()