.PHONY: serve publish

### start the local mkdocs server
serve:
	mkdocs serve

### build and push to the github page
publish:
	mkdocs build && mkdocs gh-deploy --clean
