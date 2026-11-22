# Copies of the sources

The PDFs and texts that were read are kept here on the machine where they were read. Git ignores this folder:
most of them are under licences that do not allow sharing, and the rest are a download away.

Each note in `../notes` names its file here and the address it came from. With the files in place, the quotes in
the notes can be checked again against the pages they give:

```
python3 -I <poiesis-research>/skills/research/scripts/extract_text.py research/papers/<name>.pdf
python3 -I <poiesis-research>/skills/research/scripts/verify_quotes.py research/notes --papers research/papers
```
