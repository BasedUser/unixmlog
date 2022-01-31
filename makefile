build:
	python joiner.py -s kernel.mlog -o out/kernel.mlog

test:
	python joiner.py -s joiner-tests/test.mlog -o out/test.mlog
	python joiner.py -s joiner-tests/test.mlog -o out/test-unsafe.mlog --unsafe

