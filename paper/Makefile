pdf:
	latexmk -pdf -biber main.tex

watch:
	latexmk -pdf -biber -pvc main.tex

clean:
	latexmk -C
	rm -f *.bbl *.run.xml

.PHONY: pdf watch clean
