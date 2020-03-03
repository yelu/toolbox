
cd cnn/test && rm -rf model && python TestCNN.py
cd ../../

cd intent/test && rm -rf test_output train_output && python TestIntentCNN.py
cd ../../

cd slot/test && rm -rf output && python TestSlotLCCRF.py
cd ../../

cd dialog/test && python TestTask.py
cd ../../

cd scenario/movie && rm -rf intent_ouput slot_output && python train.py && python Run.py
cd ../../

cd s2s/test && rm -rf model && python train.py && python TestSeq2SeqWithAttention.py
cd ../../