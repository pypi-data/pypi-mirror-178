#! /usr/bin/env python3
# -*- coding utf-8 -*-
"""
-------------------------------------------------
   File Name：     evaluate.py
   Author :       chenhao
   time：          2021/11/17 11:18
   Description :
-------------------------------------------------
"""
from collections import OrderedDict, defaultdict
from typing import List, Dict, Set, Sequence, Any

# 计算f1
from confai.models.schema import LabelOrLabels, Label, TextSpans, TextSpan, Task, GenText, Example


def get_f1(precision, recall):
    f1 = 0. if precision + recall == 0 else 2 * precision * recall / (precision + recall)
    return f1


# 获得precision和recall值
def get_pr(tp, fp, fn):
    precision = 0. if tp + fp == 0 else tp / (tp + fp)
    recall = 0. if tp + fn == 0 else tp / (tp + fn)
    return dict(precision=precision, recall=recall)


# 获得tp,fp,fn集合
def get_tp_fp_fn_set(true_set, pred_set):
    tp_set = true_set & pred_set
    fp_set = pred_set - tp_set
    fn_set = true_set - tp_set
    return tp_set, fp_set, fn_set


# 测评两个集合
def eval_sets(true_set, pred_set):
    tp_set, fp_set, fn_set = get_tp_fp_fn_set(true_set, pred_set)

    tp = len(tp_set)
    fp = len(fp_set)
    fn = len(fn_set)
    rs_dict = dict(tp=tp, fp=fp, fn=fn)
    pr_dict = get_pr(tp, fp, fn)
    rs_dict.update(**pr_dict)
    rs_dict.update(f1=get_f1(rs_dict['precision'], rs_dict['recall']))

    return rs_dict


def label2set(label: LabelOrLabels) -> Set[str]:
    if isinstance(label, Label):
        return {label.name}
    return set([l.name for l in label])


def get_unique_text_span(text_span: TextSpan):
    return text_span.text, text_span.label.name, text_span.span


def group_by(seq: Sequence, key=lambda x: x, map_func=lambda x: x) -> Dict[Any, List]:
    rs_dict = defaultdict(list)
    for i in seq:
        rs_dict[key(i)].append(map_func(i))
    return rs_dict


def get_micro_avg(set_eval_list):
    tp = sum(e['tp'] for e in set_eval_list)
    fp = sum(e['fp'] for e in set_eval_list)
    fn = sum(e['fn'] for e in set_eval_list)
    rs_dict = dict(tp=tp, fp=fp, fn=fn)
    pr_dict = get_pr(tp, fp, fn)
    rs_dict.update(**pr_dict)
    rs_dict.update(f1=get_f1(rs_dict['precision'], rs_dict['recall']))
    return rs_dict


def get_macro_avg(set_eval_list):
    precision_list = [e['precision'] for e in set_eval_list if e['tp'] + e['fp'] > 0]
    recall_list = [e['recall'] for e in set_eval_list if e['tp'] + e['fn'] > 0]
    precision = sum(precision_list) / len(precision_list) if precision_list else 0.
    recall = sum(recall_list) / len(recall_list) if recall_list else 0.
    f1 = get_f1(precision, recall)
    rs_dict = dict(precision=precision, recall=recall, f1=f1)
    return rs_dict


#
#
# 测评文本分类的结果
def eval_text_classify(true_labels: List[LabelOrLabels],
                       pred_labels: List[LabelOrLabels]) -> Dict:
    assert len(true_labels) == len(pred_labels)
    true_label_names = [(idx, l) for idx, labels in enumerate(true_labels) for l in label2set(labels)]
    pred_label_names = [(idx, l) for idx, labels in enumerate(pred_labels) for l in label2set(labels)]
    true_label_dict = group_by(true_label_names, key=lambda x: x[1])
    pred_label_dict = group_by(pred_label_names, key=lambda x: x[1])
    target_type_set = true_label_dict.keys() | pred_label_dict.keys()
    detail_dict = dict()
    for target_type in target_type_set:
        true_list = true_label_dict.get(target_type, [])
        true_set = set(true_list)
        pred_list = pred_label_dict.get(target_type, [])
        pred_set = set(pred_list)
        eval_rs = eval_sets(true_set, pred_set)
        detail_dict[target_type] = eval_rs
    detail_dict = dict(OrderedDict(sorted(detail_dict.items(), key=lambda x: x[1]["f1"], reverse=True)))

    set_eval_list = detail_dict.values()
    micro_eval_rs = get_micro_avg(set_eval_list)
    macro_eval_rs = get_macro_avg(set_eval_list)
    rs_dict = dict(detail=detail_dict, micro=micro_eval_rs, macro=macro_eval_rs)
    return rs_dict


#
def eval_text_span_classify(true_spans: List[TextSpans], pred_spans: List[TextSpans]) -> dict:
    assert len(true_spans) == len(pred_spans)
    flat_true_spans = [(idx, get_unique_text_span(s)) for idx, spans in enumerate(true_spans) for s in spans]
    flat_pred_spans = [(idx, get_unique_text_span(s)) for idx, spans in enumerate(pred_spans) for s in spans]

    true_span_dict = group_by(flat_true_spans, key=lambda x: x[1][1])
    pred_span_dict = group_by(flat_pred_spans, key=lambda x: x[1][1])

    target_type_set = true_span_dict.keys() | pred_span_dict.keys()
    detail_dict = dict()
    for target_type in target_type_set:
        true_spans = set(true_span_dict.get(target_type, []))
        pred_spans = set(pred_span_dict.get(target_type, []))
        eval_rs = eval_sets(true_spans, pred_spans)
        detail_dict[target_type] = eval_rs

    detail_dict = dict(OrderedDict(sorted(detail_dict.items(), key=lambda x: x[1]["f1"], reverse=True)))
    micro_eval_rs = get_micro_avg(detail_dict.values())
    macro_eval_rs = get_macro_avg(detail_dict.values())
    rs_dict = dict(detail=detail_dict, micro=micro_eval_rs, macro=macro_eval_rs)
    return rs_dict


def eval_text_gen(true_texts: List[GenText], pred_texts: List[GenText]) -> dict:
    assert len(true_texts) == len(pred_texts)
    flat_true_words = [(idx, c) for idx, gen in enumerate(true_texts) for c in gen.text]
    flat_pred_words = [(idx, c) for idx, gen in enumerate(pred_texts) for c in gen.text]

    eval_rs = eval_sets(set(flat_true_words), set(flat_pred_words))

    return eval_rs


def get_eval_func(task: Task):
    _task2eval_func = {
        Task.TEXT_CLS: eval_text_classify,
        Task.TEXT_SPAN_CLS: eval_text_span_classify,
        Task.TEXT_GEN: eval_text_gen
    }
    if task not in _task2eval_func:
        raise ValueError(f"no eval function found for task:{task}, valid tasks:"
                         f"{[e.name for e in _task2eval_func.keys()]}")
    return _task2eval_func[task]


def eval_on_task(examples: List[Example], preds: List[LabelOrLabels], task: Task) -> dict:
    eval_func = get_eval_func(task)
    true_labels = [e.get_ground_truth() for e in examples]
    return eval_func(true_labels, preds)
