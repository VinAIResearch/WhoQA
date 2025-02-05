import json
import argparse
import json
import re
from statistics import mean 
import os

def phrase_in_document(phrase, document):
    # pattern = re.compile(rf"(?<![a-zA-Z\u00C0-\u024F]){re.escape(phrase)}(?![a-zA-Z\u00C0-\u024F])")
    pattern = re.compile(r"\b" + f"{re.escape(phrase)}" + r"\b", re.IGNORECASE)
    return bool(pattern.search(document))


def load_data(path):
    samples = []
    with open(path) as f:
        for line in f:
            samples.append(json.loads(line))
    return samples


def dump_data(samples: list, out_file):
    for sample in samples:
        json.dump(sample, out_file, ensure_ascii=False)
        out_file.write("\n")
    return

def grade_answer(question):
    score = 0
    context_flatten_answers = []

    for context_id, context in enumerate(question["contexts"]):
        context_answers = []
        for answer in question["answer_by_context"][str(context_id)]:
            for alias in answer:
                context_answers.append(alias)
        context_flatten_answers.append(context_answers)

    for context_id, context in enumerate(question["contexts"]):
        correct_answer = 0
        found_aliases = []
        for answer in question["answer_by_context"][str(context_id)]:
            for alias in answer:
                if "model_answer" in question:
                    flag = phrase_in_document(alias, question["model_answer"])
                else:
                    try:
                        flag = phrase_in_document(alias, question["answer"])
                    except Exception:
                        continue    
                if flag:
                    correct_answer += 1
                    found_aliases.append(alias)
                    break
        
        if correct_answer == 0:
            continue

        if correct_answer == len(question["answer_by_context"][str(context_id)]):
            score += 1

    if "num_distinct_answers" not in question:
        question["num_distinct_answers"] = 1

    if score == len(question["contexts"]):
        return 1, question["num_distinct_answers"]
    return 0, question["num_distinct_answers"]


def eval(questions):
    stat_num_answers = {} # num_ans: num_questions
    strict_score = {}
    scored_questions = []

    for question in questions:
        score, num_ans = grade_answer(question)
        if num_ans not in stat_num_answers:
            stat_num_answers[num_ans] = 1
            if score != 1:
                strict_score[num_ans] = 0
            else:
                strict_score[num_ans] = 1.0
        else:
            stat_num_answers[num_ans] += 1
            if score == 1:
                strict_score[num_ans] += 1
        question["score"] = score
        scored_questions.append(question)

    return scored_questions, stat_num_answers, strict_score

def main(args):

    questions = load_data(args.questions)

    score_file = os.path.join(args.out_file_dir, f"{args.model_name}-score.json")
    
    scored_questions, stat_num_answers, strict_score = eval(questions)
    
    strict_recall = {}
    for k, v in strict_score.items():
        strict_recall[k] = v/stat_num_answers[k]
    
    print("Model:", args.model_name)
    print("Averate Strict Recall", mean(list(strict_recall.values())[:7]))
    print("Strict recall by num answer", strict_recall)
    print("Num questions:", sum(list(stat_num_answers.values())))
    print("Dataset stat", stat_num_answers)

    json.dump(strict_recall, open(score_file, "w"))
    
    out_file_path = os.path.join(args.out_file_dir, f"{args.model_name}-eval.jsonl")
    out_file = open(out_file_path, "w")
    dump_data(scored_questions, out_file)
    out_file.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--questions", type=str, help="model response path (jsonl)")
    parser.add_argument("--out_file_dir", type=str, help="evaluation results path (jsonl)")
    parser.add_argument("--model_name", type=str)

    args = parser.parse_args()

    main(args)
