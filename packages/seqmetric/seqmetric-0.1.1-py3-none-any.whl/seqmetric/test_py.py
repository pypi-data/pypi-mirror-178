# -*- coding: utf-8 -*-
import sys
import numpy as np
sys.path.append('..')
from seqmetric.scheme import IOBS,IOBES,IOB2
from seqmetric.metrics import classification_report,f1_score

#场景1
mode = 2
trues = [['O', 'O', 'B-MISC', 'I-MISC', 'B-MISC', 'O', 'O'], ['B-PER', 'I-PER', 'O']]
preds = [['O', 'O', 'B-MISC', 'I-MISC', 'B-MISC', 'I-MISC', 'O'], ['B-PER', 'I-PER', 'O']]

if mode == 0:
    scheme = IOBES
elif mode == 1:
    scheme = IOBS
else:
    scheme = IOB2
f1 = f1_score(trues, preds, average='weighted',scheme=scheme)
report = classification_report(trues, preds, scheme=scheme,digits=4)
print(f1)
print(report)

from seqmetric.metrics import pointer_report,report_metric,get_report_from_string,spo_report

# 场景2

label_list = ['0','1']

trues = [
         [(0 , 10,20 ),],
         [(0 , 10,20)],
         [],
         [(1,100,201)]
         ] # label_id ,start ,end

preds = [
         [(0 , 10,20 ),],
         [],
         [(1,100,200)],
         []
         ]

str_report = pointer_report(trues, preds, label_list)
print(str_report)



report = get_report_from_string(str_report)
print(report)



label_list = ['0','1']
trues = [
    [(0, 10,0,20,30),],
    [(1, 10, 0, 20, 30), ]
]

preds = [
    [(0, 10, 0, 20, 30), ],
    [
    ],
]

str_report = spo_report(trues,preds,label_list=label_list)
print(str_report)