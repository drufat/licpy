SHELL := /bin/bash

ifndef PY
PY := python3
endif

MPLPY := MPLBACKEND="Agg" $(PY)

DIR := licpy/vectorfields
SRC := $(shell find $(DIR) -name "*.py" -not -iname __init__.py -not -iname transform.py)
PLT_SOURCES += $(SRC)
PLT_RESULTS += $(SRC:.py=.arr.png)
PLT_RESULTS += $(SRC:.py=.lic.png)

$(DIR)/%.arr.png: $(DIR)/%.py
	$(MPLPY) -m licpy.command.vf arr $* $@

$(DIR)/%.lic.png: $(DIR)/%.py
	$(MPLPY) -m licpy.command.vf lic $* $@

.PHONY: plt
plt: $(PLT_SOURCES) $(PLT_RESULTS)
