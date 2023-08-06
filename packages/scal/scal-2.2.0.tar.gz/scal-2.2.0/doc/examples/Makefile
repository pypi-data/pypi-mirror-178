SCL=$(wildcard *.scl)
PDF=$(SCL:.scl=.pdf)

WEEKLY=$(wildcard weekly*.scl)
IMPOSE=$(WEEKLY:.scl=-impose.pdf)

main: $(PDF) $(IMPOSE)

.ONESHELL:
%.tex: %.scl
	export PYTHONPATH="$${PYTHONPATH}:$$(cd ../.. && pwd)"
	python3 -m scal $< > $@

%.pdf: %.tex
	spix $<

weekly-%-impose.pdf: weekly-%.pdf
	pdfimpose perfect --group 3 --output $@ $<
