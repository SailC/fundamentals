This repo contains a set of demo apps and documentations to show how to leverage ICP design pattern to build application contents.

## Updating the documentation
You need [mkdocs](http://www.mkdocs.org/) installed before you can build the github pages.

Available commands:
- `make serve` Start the local mkdocs dev server and view the page locally. Be aware that you will not be able to review the built site before it is pushed to GitHub. Therefore, you may want to first verify any changes you make to the docs and reviewing the built files locally by using this command.

- `make publish` Publish mkdocs to the [github page]([https://pages.github.ibm.com/watson-foundation-services/icp-content-demos/](https://pages.github.ibm.com/watson-foundation-services/icp-content-demos/)) . Behind the scenes, MkDocs will build your docs and use the ghp-import tool to commit them to the gh-pages branch and push the gh-pages branch to GitHub.

To create new pages, simply add/modify markdown files under [icp-content-demos/docs](https://github.ibm.com/watson-foundation-services/icp-content-demos/tree/master/docs), and `mkdocs build` will build the pages under [icp-content-demos/site](https://github.ibm.com/watson-foundation-services/icp-content-demos/tree/master/site) from the markdown files.
# fundamentals
