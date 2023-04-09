OUT_PREFIX ?= out

EVALUATORS := $(wildcard evaluators/*.py)
OUTFILES   := $(patsubst evaluators/%.py, $(OUT_PREFIX)/%, $(EVALUATORS))

SCENARIOS_PREFIX         ?= scenarios
SCENARIO_JSON_GENERATORS := $(wildcard comprehensive/*.json.py)
SCENARIO_JSONS           := $(patsubst comprehensive/%.json.py, $(SCENARIOS_PREFIX)/%.json, $(SCENARIO_JSON_GENERATORS))

SCENARIOS_GENERATE_DONE := $(SCENARIOS_PREFIX)/generate-done

# So everyone can access `common` equally well:
# also, if you add a comment on the same line as the variable, but leave a trailing space before the #, then that space gets added to the variable and python doesn't like it. Just completely normal Makefile things.
export PYTHONPATH := $(PWD)

all: $(OUTFILES)

$(OUT_PREFIX)/%: evaluators/%.py lost
	python3 $< $@

$(OUT_PREFIX)/comprehensive.csv: comprehensive/combine-jsons.py $(SCENARIO_JSONS)
	python3 $< $@ $(SCENARIOS_PREFIX)

# For scenarios, we're really trying to do something which is fundamentally beyond Make's abilities: Have an outer folder parametrized 

$(SCENARIOS_PREFIX)/%.json: comprehensive/%.json.py $(SCENARIOS_GENERATE_DONE)
	python3 $< $@ $(SCENARIOS_PREFIX)

# Generated the PNGs and expected attitudes:
$(SCENARIOS_GENERATE_DONE): comprehensive/generate-pngs.py common/scenarios.py
	python3 comprehensive/generate-pngs.py $(SCENARIOS_PREFIX)
	touch $@

clean:
	rm -rf $(SCENARIOS_PREFIX) $(OUTFILES)

.PHONY: all clean
