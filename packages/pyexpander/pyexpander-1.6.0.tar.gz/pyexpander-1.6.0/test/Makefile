#
# test1.in : simply macro replacement

TOP:=$(shell pwd)/..

PYVER:=$(strip $(PYVER))

ifeq (,$(findstring $(PYVER),2 3))
$(error error variable PYVER must be set to 2 or 3)
endif

export PYVER

# set PYTHON only if it is not yet defined:
ifeq (,$(PYTHON))
        PYTHON:=python$(PYVER)
endif

BINDIR:=$(TOP)/python$(PYVER)/bin
LIBDIR:=$(TOP)/python$(PYVER)/pyexpander

export PYTHONPATH:=$(TOP)/python$(PYVER):$(PYTHONPATH)

ifeq ($(PYVER),2)
EXPANDER_BIN=expander.py
else
EXPANDER_BIN=expander3.py
endif

EXPANDER=$(BINDIR)/$(EXPANDER_BIN)

.PRECIOUS: %.out

# set this only to "yes" in order to create the 
# test[n].ok files. These files are later compared to
# the test[n].out files.
# In order for the tests to really test pyexpander, 
# the variable MUST BE set to "no".
CREATE_TESTS=no

testlist= test1 test2 test3 test4 test5 test6 test7 test8 test9 \
	  test10 test11 test12 test13 test14 test15 test16 test17 \
	  test18 test19 test20 test21 test22 test23 test24 test25 \
	  test26 test27 test28 test29


all: pure_module_test external_module_test $(addsuffix .tst, $(testlist))

clean:
	rm -f $(addsuffix .out, $(testlist))

_clean: clean
	rm -f $(addsuffix .ok, $(testlist))

pure_module_test:
	echo "PYTHONPATH: " $(PYTHONPATH)
	$(PYTHON) $(LIBDIR)/parser.py
	$(PYTHON) $(LIBDIR)/lib.py

external_module_test:
	$(PYTHON) ./pyexpander_test.py

ok: $(addsuffix .ok, $(testlist))

%.out: %.in
	$(EXPANDER) -f $< > $@

test3.out: test3.in
	$(EXPANDER) -f $< --eval 'x=1' > $@

test4.out: test4.in
	($(EXPANDER) -f $< || true) 2>&1 | \
	    sed -e 's/.*\//  "/;s/line [0-9]\+/line xxx/;s/$(EXPANDER_BIN)/expander.py/;s/\(raise\) NameError, \(.*\)/\1 e.__class__(\2)/;s/\(str(e),\)\([^ ]\)/\1 \2/' > $@

test7.out: test7.in
	$(EXPANDER) -s -f $< > $@

test19.out: test19.in
	mkdir x
	echo "\$$py(a+=1)" > x/test.inc
	$(EXPANDER) -f $< -I x > $@
	rm -rf x

test25.out: test25.in
	$(EXPANDER) -f $< | sed -e 's/<type/<class/' > $@

ifeq "$(CREATE_TESTS)" "yes"
%.ok: %.out
	cp $< $@
endif

%.tst: %.in %.out %.ok
	diff $(wordlist 2, 3, $+) || true


