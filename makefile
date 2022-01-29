build:
	python joiner.py -s kernel.mlog -o out/kernel.mlog

test:
	python joiner.py -s joiner-tests/test.mlog -o out/test.mlog -r joiner-tests/
	python joiner.py -s joiner-tests/test.mlog -o out/test-unsafe.mlog -r joiner-tests/ --unsafe

