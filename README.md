# Literature-Article
A repository for an article on the literature review of the Prisoner's Dilemma.

The repository is structured as follows:


```
.
|---  assets
      |--- images
      |--- tex
|---  src
      |--- nbs/
      |--- data/ # hidden
      |--- articles_to_axelbib.py 
      |--- password.py # hidden
      |--- scraping.py 
|---  .gitignore
|---  environment.yml
|---  bibliography.bib
|---  main.pdf
|---  main.tex
|---  README.md
```


The command to compile `main.tex` is:

`pdflatex --shell-escape main`

The articles has the following structure:

```
|---  Introduction
      |--- introduction
      |--- applications
|---  Timeline
      |--- papers I have read
|---  Analysis
      |--- papers I have not read
      |--- data
            |--- description of data set
            |--- temporal analysis
            |--- co-authors analysis
            .... 
|---  Reproducing
      |--- zenodo
      |--- axelbib
      |--- repository with notebooks for analysis
|---  Conclusions
      |--- -//- of articles
      |--- -//- of the analysis
      |--- -//- of the paper

```