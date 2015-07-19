::tesseract.exe ddo-ddo_font-exp4.bmp ddo-ddo_font-exp4 -l ddotrain -psm 6 batch.nochop makebox
::tesseract.exe ddo-ddo_font-exp5.bmp ddo-ddo_font-exp5 -l ddotrain -psm 6 batch.nochop makebox
::tesseract.exe ddo-ddo_font-exp6.bmp ddo-ddo_font-exp6 -l ddotrain -psm 6 batch.nochop makebox
::tesseract.exe ddo-ddo_font-exp7.bmp ddo-ddo_font-exp7 -l ddotrain -psm 6 batch.nochop makebox
::tesseract.exe ddo-ddo_font-exp8.bmp ddo-ddo_font-exp8 -l ddotrain -psm 6 batch.nochop makebox
::tesseract.exe ddo-ddo_font-exp9.bmp ddo-ddo_font-exp9 -l ddotrain -psm 6 batch.nochop makebox
::tesseract.exe ddo-ddo_font-exp10.bmp ddo-ddo_font-exp10 -l ddotrain -psm 6 batch.nochop makebox
::tesseract.exe ddo-ddo_font-exp11.bmp ddo-ddo_font-exp11 -l ddotrain -psm 6 batch.nochop makebox
::tesseract.exe ddo-ddo_font-exp12.bmp ddo-ddo_font-exp12 -l ddotrain -psm 6 batch.nochop makebox
::tesseract.exe ddo-ddo_font-exp13.bmp ddo-ddo_font-exp13 -l ddotrain -psm 6 batch.nochop makebox
::tesseract.exe ddo-ddo_font-exp14.bmp ddo-ddo_font-exp14 -l ddotrain -psm 6 batch.nochop makebox
::tesseract.exe ddo-ddo_font-exp15.bmp ddo-ddo_font-exp15 -l ddotrain -psm 6 batch.nochop makebox
::tesseract.exe ddo-ddo_font-exp16.bmp ddo-ddo_font-exp16 -l ddotrain -psm 6 batch.nochop makebox

::tesseract.exe ddo-ddo_font-exp4.bmp ddo-ddo_font-exp4 -l ddotrain -psm 6 nobatch box.train
::tesseract.exe ddo-ddo_font-exp5.bmp ddo-ddo_font-exp5 -l ddotrain -psm 6 nobatch box.train
::tesseract.exe ddo-ddo_font-exp6.bmp ddo-ddo_font-exp6 -l ddotrain -psm 6 nobatch box.train
::tesseract.exe ddo-ddo_font-exp7.bmp ddo-ddo_font-exp7 -l ddotrain -psm 6 nobatch box.train
::tesseract.exe ddo-ddo_font-exp8.bmp ddo-ddo_font-exp8 -l ddotrain -psm 6 nobatch box.train
::tesseract.exe ddo-ddo_font-exp9.bmp ddo-ddo_font-exp9 -l ddotrain -psm 6 nobatch box.train
::tesseract.exe ddo-ddo_font-exp10.bmp ddo-ddo_font-exp10 -l ddotrain -psm 6 nobatch box.train
::tesseract.exe ddo-ddo_font-exp11.bmp ddo-ddo_font-exp11 -l ddotrain -psm 6 nobatch box.train
::tesseract.exe ddo-ddo_font-exp12.bmp ddo-ddo_font-exp12 -l ddotrain -psm 6 nobatch box.train
::tesseract.exe ddo-ddo_font-exp13.bmp ddo-ddo_font-exp13 -l ddotrain -psm 6 nobatch box.train
::tesseract.exe ddo-ddo_font-exp14.bmp ddo-ddo_font-exp14 -l ddotrain -psm 6 nobatch box.train
::tesseract.exe ddo-ddo_font-exp15.bmp ddo-ddo_font-exp15 -l ddotrain -psm 6 nobatch box.train
::tesseract.exe ddo-ddo_font-exp16.bmp ddo-ddo_font-exp16 -l ddotrain -psm 6 nobatch box.train

::unicharset_extractor.exe ddo-ddo_font-exp4.box ddo-ddo_font-exp5.box ddo-ddo_font-exp6.box ddo-ddo_font-exp7.box ddo-ddo_font-exp8.box ddo-ddo_font-exp9.box ddo-ddo_font-exp10.box ddo-ddo_font-exp11.box ddo-ddo_font-exp12.box ddo-ddo_font-exp13.box ddo-ddo_font-exp14.box ddo-ddo_font-exp15.box ddo-ddo_font-exp16.box
shapeclustering.exe -F font_properties -U unicharset ddo-ddo_font-exp4.tr ddo-ddo_font-exp5.tr ddo-ddo_font-exp6.tr ddo-ddo_font-exp7.tr ddo-ddo_font-exp8.tr ddo-ddo_font-exp9.tr ddo-ddo_font-exp10.tr ddo-ddo_font-exp11.tr ddo-ddo_font-exp12.tr ddo-ddo_font-exp13.tr ddo-ddo_font-exp14.tr ddo-ddo_font-exp15.tr ddo-ddo_font-exp16.tr
mftraining -F font_properties -U unicharset -O ddo.unicharset ddo-ddo_font-exp4.tr ddo-ddo_font-exp5.tr ddo-ddo_font-exp6.tr ddo-ddo_font-exp7.tr ddo-ddo_font-exp8.tr ddo-ddo_font-exp9.tr ddo-ddo_font-exp10.tr ddo-ddo_font-exp11.tr ddo-ddo_font-exp12.tr ddo-ddo_font-exp13.tr ddo-ddo_font-exp14.tr ddo-ddo_font-exp15.tr ddo-ddo_font-exp16.tr
cntraining ddo-ddo_font-exp4.tr ddo-ddo_font-exp5.tr ddo-ddo_font-exp6.tr ddo-ddo_font-exp7.tr ddo-ddo_font-exp8.tr ddo-ddo_font-exp9.tr ddo-ddo_font-exp10.tr ddo-ddo_font-exp11.tr ddo-ddo_font-exp12.tr ddo-ddo_font-exp13.tr ddo-ddo_font-exp14.tr ddo-ddo_font-exp15.tr ddo-ddo_font-exp16.tr
move inttemp ddo.inttemp
move normproto ddo.normproto
move pffmtable ddo.pffmtable
move shapetable ddo.shapetable
combine_tessdata ddo.