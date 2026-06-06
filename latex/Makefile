# Makefile — LuaLaTeX 4-pass build with biber
# Usage: cd latex && make
# Requirements: lualatex, biber (TeXLive 2023+ recommended)

MAIN        = main
OUTPUT_DIR  = output
GROUP_CODE  = uoh-sqak
PDF_NAME    = $(GROUP_CODE)-article.pdf

.PHONY: all clean distclean

all: $(OUTPUT_DIR)/$(PDF_NAME)

$(OUTPUT_DIR)/$(PDF_NAME): $(MAIN).tex bib/references.bib $(wildcard chapters/*.tex) \
                            $(wildcard figures/*) style/article.sty
	@mkdir -p $(OUTPUT_DIR)
	@echo "==> Pass 1: lualatex"
	lualatex --output-directory=$(OUTPUT_DIR) --interaction=nonstopmode $(MAIN).tex
	@echo "==> Pass 2: biber"
	biber --input-directory=$(OUTPUT_DIR) --output-directory=$(OUTPUT_DIR) $(MAIN)
	@echo "==> Pass 3: lualatex"
	lualatex --output-directory=$(OUTPUT_DIR) --interaction=nonstopmode $(MAIN).tex
	@echo "==> Pass 4: lualatex"
	lualatex --output-directory=$(OUTPUT_DIR) --interaction=nonstopmode $(MAIN).tex
	@cp $(OUTPUT_DIR)/$(MAIN).pdf $(OUTPUT_DIR)/$(PDF_NAME)
	@echo "==> Done: $(OUTPUT_DIR)/$(PDF_NAME)"

clean:
	@rm -f $(OUTPUT_DIR)/*.aux $(OUTPUT_DIR)/*.log $(OUTPUT_DIR)/*.toc \
	        $(OUTPUT_DIR)/*.bbl $(OUTPUT_DIR)/*.blg $(OUTPUT_DIR)/*.bcf \
	        $(OUTPUT_DIR)/*.run.xml $(OUTPUT_DIR)/*.out $(OUTPUT_DIR)/*.lof \
	        $(OUTPUT_DIR)/*.lot $(OUTPUT_DIR)/*.fls $(OUTPUT_DIR)/*.fdb_latexmk
	@echo "Cleaned auxiliary files"

distclean: clean
	@rm -f $(OUTPUT_DIR)/$(MAIN).pdf $(OUTPUT_DIR)/$(PDF_NAME)
	@echo "Cleaned all generated files"
