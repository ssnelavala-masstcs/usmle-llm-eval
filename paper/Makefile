pdf:
	pdflatex -interaction=nonstopmode main.tex
	biber main
	pdflatex -interaction=nonstopmode main.tex
	pdflatex -interaction=nonstopmode main.tex

watch:
	latexmk -pdf -pvc main.tex

clean:
	latexmk -C
	rm -f *.bbl *.run.xml

.PHONY: pdf watch clean
