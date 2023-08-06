# -*- coding: utf-8 -*-
# @Time    : 2022/2/21 16:43
# @Author  : wyw
import typing
import pandas as pd

__all__ = [
        "get_report_from_string",
        "report_metric",
        "pointer_report",
        "spo_report"]


def get_report_from_string(str_report,metric='micro'):
    report = {}
    arr = str_report.split('\n')
    for item in arr[1:]:
        d = item.replace(' ', '#')
        dd = ''
        last_flag = False
        for char in d:
            if char == '#':
                last_flag = True
                continue

            if last_flag:
                dd += ' '
            dd += char
            last_flag = False
        d = dd
        d = d.rsplit(' ', maxsplit=4)
        if d[0].startswith(' '):
            d[0] = d[0][1:]
        report[d[0]] = (float(d[1:][0]), float(d[1:][1]), float(d[1:][2]), int(d[1:][3]))
    if metric in report:
        return report[metric]
    if metric + ' avg' in report:
        return report[metric + ' avg']
    return report

def report_to_string(report,float_precision=4,col_space=10,):
    def dict2str(mdict,with_header=True):
        metric_pd = pd.DataFrame(mdict)
        # metric_pd = metric_pd.transpose()
        metric_pd.index = ['%20s' % index for index in metric_pd.index]
        metric_pd.columns = ["precision", "recall", "f1-score", "support"]
        metric_pd['support'] = metric_pd['support'].astype(dtype=int)

        # metric_pd = metric_pd.rename(lambda x: "     " + str(x) + "     ")
        pd.set_option('display.precision', float_precision)
        pd.set_option("display.colheader_justify", "right")
        str_report = metric_pd.to_string(justify="left", col_space=col_space, index_names=False,header=with_header)
        return str_report

    str_report = dict2str(report)
    return str_report

def report_metric(y_trues, y_preds):
    assert len(y_trues) == len(y_preds)
    X, Y, Z = 1e-10, 1e-10, 1e-10
    N = int(0)
    for true,pred in zip(y_trues, y_preds):
        R = set(pred)
        T = set(true)
        X += len(R & T)
        Y += len(R)
        Z += len(T)
        N += len(true)
    precision = X / Y if X != 1e-10 else 0.
    recall = X / Z if X != 1e-10 else 0.
    f1 = 2 * X / (Y + Z) if X != 1e-10 else 0.
    return (precision, recall, f1, N)

'''
    获取所有类别评价
    y_trues = [
        {
            'class0': [(any thing can do set)],
            'class1': [(any thing can do set)],
        }
    ]
'''

def class_report_for_all(y_trues: typing.Dict, y_preds: typing.Dict,auto_remove_zero=True,float_precision=4,col_space=10,):
    metric_map = {}
    all_trues = []
    all_preds = []
    for k, v in y_trues.items():
        tmp_trues = v
        tmp_preds = y_preds[k]
        metric_map[k] = report_metric(tmp_trues, tmp_preds)
        if auto_remove_zero and metric_map[k][-1] == 0:
            metric_map.pop(k)
            continue

        all_trues.extend(tmp_trues)
        all_preds.extend(tmp_preds)

    avg_f1, avg_precision, avg_recall = 0., 0., 0.
    weight_f1, weight_precision, weight_recall = 0., 0., 0

    e_count = 0
    for k, v in metric_map.items():
        avg_precision += v[0]
        avg_recall += v[1]
        avg_f1 += v[2]
        e_count += v[3]

        weight_precision += v[0] * v[3]
        weight_recall += v[1] * v[3]
        weight_f1 += v[2] * v[3]

    avg_precision /= (len(metric_map) + 1e-10)
    avg_recall /=(len(metric_map) + 1e-10)
    avg_f1 /= (len(metric_map) + 1e-10)

    if e_count > 0:
        weight_precision /= e_count
        weight_recall /= e_count
        weight_f1 /= e_count


    metric_map['micro avg'] = report_metric(all_trues, all_preds)
    metric_map['macro avg'] = (avg_precision, avg_recall, avg_f1, e_count)
    metric_map['weighted avg'] = (weight_precision, weight_recall, weight_f1, e_count)
    metric_pd = pd.DataFrame(metric_map)
    metric_pd = metric_pd.transpose()
    return report_to_string(metric_pd,
                            float_precision=float_precision,
                            col_space=col_space,
                            )


'''
    标签，起始坐标，终止坐标
    y_trues = [
        [(0,10,20),(1,30,40)]
    ]
'''

def pointer_report(y_trues, y_preds, label_list, auto_remove_zero=True,float_precision=4,col_space=10,):
    id2label = {i: label for i, label in enumerate(label_list)}
    my_trues = {
        label: [] for i, label in id2label.items()
    }
    my_preds = {
        label: [] for i, label in id2label.items()
    }
    for t,p in zip(y_trues,y_preds):
        one_trues = {
            label: [] for i, label in id2label.items()
        }
        one_preds = {
            label: [] for i, label in id2label.items()
        }
        for (l,start,end) in t:
            str_label = id2label[l]
            one_trues[str_label].append((l, start, end))
        for (l,start,end) in p:
            str_label = id2label[l]
            one_preds[str_label].append((l, start, end))

        for k, v in my_trues.items():
            v.append(one_trues[k])
        for k, v in my_preds.items():
            v.append(one_preds[k])

    report = class_report_for_all(my_trues,my_preds,auto_remove_zero=auto_remove_zero,
                                  float_precision=float_precision,
                                  col_space=col_space,
                                  )
    return report


'''
    sh,st,p,oh,ot
    subject start,subject end,relation,object start,object end
    y_trues = [
        [(0,10,0,10,20),]
    ]
'''

def spo_report(y_trues, y_preds, label_list, auto_remove_zero=True,float_precision=4,col_space=10,):
    id2label = {i: label for i, label in enumerate(label_list)}
    my_trues = {
        label: [] for i, label in id2label.items()
    }
    my_preds = {
        label: [] for i, label in id2label.items()
    }
    for tt,pp in zip(y_trues,y_preds):
        one_trues = {
            label: [] for i, label in id2label.items()
        }
        one_preds = {
            label: [] for i, label in id2label.items()
        }

        for (sh,st,p,oh,ot) in tt:
            str_label = id2label[p]
            one_trues[str_label].append((sh,st,p,oh,ot))


        for (sh,st,p,oh,ot) in pp:
            str_label = id2label[p]
            one_preds[str_label].append((sh,st,p,oh,ot))

        for k, v in my_trues.items():
            v.append(one_trues[k])
        for k, v in my_preds.items():
            v.append(one_preds[k])

    str_report = class_report_for_all(my_trues,my_preds,
                                      auto_remove_zero=auto_remove_zero,
                                      float_precision=float_precision,
                                      col_space=col_space,
                                      )
    return str_report