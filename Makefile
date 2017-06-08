# for i in range(8):
#     print('f{}:\n\tffmpeg -i videos/{}.avi -filter:v "crop=120:284:70:0"  -r 30 images/{}/output_%04d.png'.format(i,i,i))
f0:
	rm images/0/*
	ffmpeg -i videos/0.avi -filter:v "crop=120:284:70:0" -r 30 images/0/output_%04d.png
f1:
	rm images/1/*
	ffmpeg -i videos/1.avi -ss 00:00:03 -filter:v "crop=300:280:142:90" -r 15 images/1/output_%04d.png
f2:
	rm images/2/*
	ffmpeg -i videos/2.avi -filter:v "crop=240:240:160:184" -r 15 images/2/output_%04d.png
f3:
	rm images/3/*
	ffmpeg -i videos/3.avi -ss 00:00:21 -filter:v "crop=240:128:192:349" -r 15 images/3/output_%04d.png
f4:
	rm images/4/*
	ffmpeg -i videos/4.avi -ss 00:00:03 -filter:v "crop=240:180:165:210" -r 15 images/4/output_%04d.png
f5:
	rm images/5/*
	ffmpeg -i videos/5.avi -filter:v "crop=180:160:88:233" -r 15 images/5/output_%04d.png
f6:
	rm images/6/*
	ffmpeg -i videos/6.avi -r 30 images/6/output_%04d.png
f7:
	rm images/7/*
	ffmpeg -i videos/7.avi -r 30 images/7/output_%04d.png
fall: f0 f1 f2 f3 f4 f5 f6 f7

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
