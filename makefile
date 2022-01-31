JOINER_SCRIPT=tools/mlog-joiner/joiner.py

build:
	python $(JOINER_SCRIPT) -s kernel.mlog -o out/kernel.mlog

test:
	python $(JOINER_SCRIPT) -s tools/mlog-joiner/tests/test.mlog -o out/test.mlog
	python $(JOINER_SCRIPT) -s tools/mlog-joiner/tests/test.mlog -o out/test-unsafe.mlog --unsafe

