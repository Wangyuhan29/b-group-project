.PHONY: validate test demo legacy-demo history check
PYTHON ?= python3
validate:
	$(PYTHON) validate.py
	$(PYTHON) scripts/minicalc.py --validate
test:
	$(PYTHON) -m unittest discover -s tests -v
demo:
	$(PYTHON) scripts/minicalc.py
legacy-demo:
	$(PYTHON) scripts/demo.py
history:
	$(PYTHON) scripts/verify_history.py
check: validate test demo history
