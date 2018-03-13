# Data model & query

![1](https://www.safaribooksonline.com/library/view/designing-data-intensive-applications/9781491903063/assets/ch02-map-ebook.png)

Historically, data started out being represented as big tree (the hierarchical model), but that wasn't good for representing `many-to-many relationships` , so relational model was invented to solve that problem.

More recently, developers found that some apps don't fit well in the relational model either, so non-relational `NoSQL` datastores have come into play :

1. `Document databases` target use cases where data comes in self-contained documents and relationships between one document and another are rare.

2. `Graph databases` go in the opposite direction, targeting cases where anything is potentially related to everything.

All three data models (relational, document, graph) are widely used today, each good in its respective domain. We use different data models for different purpose, not a single one-size-fits-all solution.

Non relational databases don't enforce data schema, which makes it easier for apps to adapt to changing requirements.
