OUT_PREFIX ?= out
EVALUATORS=$(wildcard evaluators/*.py)
OUTFILES=$(patsubst evaluators/%.py, $(OUT_PREFIX)/%, $(EVALUATORS))

all: $(OUTFILES)

$(OUT_PREFIX)/%: evaluators/%.py lost
	python3 $< $@

.PHONY: all
