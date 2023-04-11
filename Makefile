OUT_PREFIX ?= out

EVALUATORS := $(wildcard evaluators/*.py)
OUTFILES   := $(patsubst evaluators/%.py, $(OUT_PREFIX)/%, $(EVALUATORS))

SCENARIOS_PREFIX         ?= scenarios
SCENARIO_JSON_GENERATORS := $(wildcard comprehensive/*.json.py)
SCENARIO_JSONS           := $(patsubst comprehensive/%.json.py, $(SCENARIOS_PREFIX)/%.json, $(SCENARIO_JSON_GENERATORS))

SCENARIOS_GENERATE_DONE := $(SCENARIOS_PREFIX)/generate-done
OST_CALIBRATION_DONE    := $(SCENARIOS_PREFIX)/ost-calibration-done

# So everyone can access `common` equally well:
# also, if you add a comment on the same line as the variable, but leave a trailing space before the #, then that space gets added to the variable and python doesn't like it. Just completely normal Makefile things.
export PYTHONPATH := $(PWD)
export OPENSTARTRACKER_DIR ?= openstartracker

all: $(OUTFILES)

# Convenience when typing at cli:
comprehensive: $(OUT_PREFIX)/comprehensive.csv
graphs: $(OUTFILES)

$(OUT_PREFIX)/%: evaluators/%.py
	python3 $< $@

$(OUT_PREFIX)/comprehensive.csv: comprehensive/combine-jsons.py common/params.py $(SCENARIO_JSONS)
	python3 $< $@ $(SCENARIOS_PREFIX)

# For scenarios, we're really trying to do something which is fundamentally beyond Make's abilities: Have an outer folder parametrized 

# Of course, these also depend on params.py...but we don't want to re-run everything every jjjj
$(SCENARIOS_PREFIX)/%.json: comprehensive/%.json.py $(SCENARIOS_GENERATE_DONE)
	python3 $< $@ $(SCENARIOS_PREFIX)

# Override to add calibration dependency for openstartracker
$(SCENARIOS_PREFIX)/openstartracker.json: $(OST_CALIBRATION_DONE)

$(OST_CALIBRATION_DONE): comprehensive/calibrate-openstartracker.py $(SCENARIOS_GENERATE_DONE)
	python3 $< $(SCENARIOS_PREFIX)
	touch $@

# Generated the PNGs and expected attitudes:
$(SCENARIOS_GENERATE_DONE): comprehensive/generate-pngs.py
	python3 comprehensive/generate-pngs.py $(SCENARIOS_PREFIX)
	touch $@

# Force regeneration of images and, by consequence, all the jsons and comprehensive.csv
clean-comprehensive:
	rm -f $(SCENARIOS_GENERATE_DONE)

# Force regeneration of jsons and comprehensive.csv, but keep same generated images:
clean-jsons:
	rm -f $(SCENARIO_JSONS)

clean:
	rm -rf $(SCENARIOS_PREFIX) $(OUTFILES)

.PHONY: all clean clean-comprehensive clean-jsons comprehensive graphs
