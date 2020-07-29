#!/bin/bash
rm AI_2019-03-0* -r
rm source_label_pred_MaxLoss0.txt source_cls_pred_MaxLoss0.txt test_log option_test.txt
make_predicion_cnn.sh ../../c2d-SWIRE_region/appendix_Model_IV/part1_train/ MaxLoss5 MaxLoss0
print_test_result.py MaxLoss0 > test_log
