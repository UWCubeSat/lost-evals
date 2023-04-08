OUT_PREFIX ?= out

EVALUATORS := $(wildcard evaluators/*.py)
OUTFILES   := $(patsubst evaluators/%.py, $(OUT_PREFIX)/%, $(EVALUATORS))

SCENARIOS_PREFIX        ?= scenarios
SCENARIO_CSV_GENERATORS := $(wildcard comprehensive/*.csv.py)
SCENARIO_CSVS           := $(patsubst comprehensive/%.csv.py, $(SCENARIOS_PREFIX)/)

EXPECTED_ATTITUDES := $(SCENARIOS_PREFIX)/expected-attitudes.pkl

# So everyone can access `common` equally well:
PYTHONPATH=$(PWD) # I think you can just do '.' too but not sure

all: $(OUTFILES)

$(OUT_PREFIX)/%: evaluators/%.py lost
	python3 $< $@

$(OUT_PREFIX)/comprehensive.csv: $(SCENARIO_CSVS) comprehensive/combine-csvs.py
	python3 comprehensive/combine-csvs.py $@ $(SCENARIOS_PREFIX)

$(SCENARIOS_PREFIX)/%.csv: comprehensive/%.csv.py $(EXPECTED_ATTITUDES)
	python3 $< $@

# Generated the PNGs and expected attitudes:
$(EXPECTED_ATTITUDES): comprehensive/generate-pngs.py
	mkdir -p $(SCENARIOS_PREFIX)/indicators
	python3 comprehensive/generate-pngs.py $(SCENARIOS_PREFIX)

.PHONY: all
