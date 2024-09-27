##### Table of contents
1. [Dataset](#Dataset) 
2. [Acknowledgments](#Acknowledgments)

# Who’s Who: Large Language Models Meet Knowledge Conflicts in Practice ([EMNLP 2024 Findings](https://2024.emnlp.org/program/accepted_findings/))


> **Abstract**: 
Retrieval-augmented generation (RAG) methods are viable solutions for addressing the static memory limits of pre-trained language models. Nevertheless, encountering conflicting sources of information within the retrieval context is an inevitable practical challenge. In such situations, the language models are recommended to transparently inform users about the conflicts rather than autonomously deciding what to present based on their inherent biases. To analyze how current large language models (LLMs) align with our recommendation, we introduce WhoQA, a public benchmark dataset to examine model's behavior in knowledge conflict situations. We induce conflicts by asking about a common property among entities having the same name, resulting in questions with up to 8 distinctive answers. WhoQA evaluation set includes 5K questions across 13 Wikidata property types and 150K Wikipedia entities. Our experiments show that despite the simplicity of WhoQA questions, knowledge conflicts significantly degrades LLMs' performance in RAG settings.

![overview](docs/conflict_demonstration_short.pdf)

Details of the model architecture and experimental results can be found in [our paper]():
```bibtext
@inproceedings{pham_whoqa,
  title={Who’s Who: Large Language Models Meet Knowledge Conflicts in Practice},
  author={Quang Hieu Pham and Hoang Ngo and Anh Tuan Luu and Dat Quoc Nguyen},
  year={2024},
  booktitle={The 2024 Conference on Empirical Methods in Natural Language Processing}
}
```
**Please CITE** our [paper]() whenever this repository is used to help produce published results or incorporated into other software.

By downloading the WhoQA dataset, USER agrees:

* to use WhoQA for research or educational purposes only.
* to not distribute WhoQA or part of WhoQA in any original or modified form.
* and to cite our paper above whenever WhoQA is employed to help produce published results.