import linecache
import json
import os
import argparse


def merge(answer_path, questions_path, out_dir, model_name):
    line_idx = 0

    out_file = open(os.path.join(out_dir, f"{model_name}-questions-answers.jsonl"), "w")

    with open(answer_path) as f:
        for line in f:
            question = json.loads(linecache.getline(questions_path, line_idx+1))
            line_idx += 1
            question["model_answer"] = json.loads(line)["answer"]
            json.dump(question, out_file, ensure_ascii=False)
            out_file.write("\n")
    out_file.close()
    
    return

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", type=str, help="path to the dataset")
    parser.add_argument("--answers", type=str, help="model answers path")
    parser.add_argument("--model_name", type=str, help="name of the model") 
    parser.add_argument("--out_dir", type=str, help="path to the output file")
    args = parser.parse_args()

    merge(args.answers, args.dataset, args.out_dir, args.model_name)
