# for i in range(8):
#     print('f{}:\n\tffmpeg -i videos/{}.avi -filter:v "crop=120:284:70:0"  -r 30 images/{}/output_%04d.png'.format(i,i,i))
f0:
	rm -f images/0/*
	ffmpeg -i videos/0.avi -filter:v "crop=120:284:70:0" -r 30 images/0/output_%04d.png
f1: # Skip 3 seconds as there is a switching
	rm -f images/1/*
	ffmpeg -i videos/1.avi -ss 00:00:03 -filter:v "crop=300:280:142:90" -r 15 images/1/output_%04d.png
f2:
	rm -f images/2/*
	ffmpeg -i videos/2.avi -filter:v "crop=240:240:160:184" -r 15 images/2/output_%04d.png
f3: # Skip 12 seconds as there is a shift
	rm -f images/3/*
	ffmpeg -i videos/3.avi -ss 00:00:12 -filter:v "crop=240:128:192:349" -r 15 images/3/output_%04d.png
f4: # Skip 3 seconds as there is a bluring because of focusing?
	rm -f images/4/*
	ffmpeg -i videos/4.avi -ss 00:00:03 -filter:v "crop=240:180:165:210" -r 15 images/4/output_%04d.png
f5:
	rm -f images/5/*
	ffmpeg -i videos/5.avi -filter:v "crop=180:160:88:233" -r 15 images/5/output_%04d.png
f6:
	rm -f images/6/*
	ffmpeg -i videos/6.avi -r 30 images/6/output_%04d.png
f7: # Skip 10 seconds as there is only thin edge
	rm -f images/7/*
	ffmpeg -i videos/7.avi -ss 00:00:10 -r 30 images/7/output_%04d.png
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
frames.zip:
	for i in {1..7} ; do \
	cpdf -merge -idir pdf/$$i -o pdf/video_$$i.pdf ; \
	done
	zip frames.zip pdf/*.pdf
figures.pdf:
	cpdf -merge -idir figures/ -o figures.pdf ; \
