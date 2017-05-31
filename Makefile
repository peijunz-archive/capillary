frames:
	#rm images/output_*
	ffmpeg -i T-L\ _\ 1-50\ tip-tip.avi 2>&1 |grep -o '[0-9]\+ fps'
	ffmpeg -i T-L\ _\ 1-50\ tip-tip.avi -r 30 images/output_%04d.png
analyse:
	python3 -m capillary.analyse
test:
	python3 test.py
processed.txz:
	tar -cJf processed.tar.xz processed/*
processed.tgz:
	tar -czf processed.tar.gz processed/*
processed.zip:
	zip processed.zip processed/*
