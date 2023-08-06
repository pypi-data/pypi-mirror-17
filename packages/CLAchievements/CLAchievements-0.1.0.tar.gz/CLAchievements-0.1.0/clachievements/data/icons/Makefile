SVG=$(patsubst %.tex,%.svg,$(wildcard *.tex))

all: $(SVG)

%.pdf: %.tex
	pdflatex --shell-escape $<

%.svg: %.pdf
	inkscape --without-gui --file=$< --export-plain-svg=$@

