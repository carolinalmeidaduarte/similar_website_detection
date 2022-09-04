# References


## Past Work
[1] proposed a technique to detect similar web pages based on the structure and style similarity of the html, defined as:
- Structural similarity of HTML pages: measured by using Tree Edit Distance measure on DOM trees,
- Stylistic similarity: measured by using Jaccard similarity on CSS class names.

On top of these, an aggregated measure of similarity is proposed, combining structural and stylistic measures.
Since it is not possible to determine a priori the number of clusters - N - in the data, a technique that does not require N is needed. The authors use Shared Near Neighbor Clustering, which complexity is O(n^2).
There is a python package that implements the described methodology: https://pypi.org/project/html-similarity/

There is also another python package that can be used to compare html files - https://github.com/TeamHG-Memex/page-compare.
It used a sequence comparison methodology which, however, is O(n^2)

## What can be improved
There are two main issues on these approaches for a large-scale dataset:
1 - The similarity definition is good, but too slow
2 - The cluster approach is not manageable for large datasets

The stragegy can be:
1 - Define a simpler, quick method for similarity. This can be based on some aggregated metrics about the html structure, such as tag counts.
2 - Distance metric is then only a function of integers - can be euclidean, or something else
3 - Instead of trying a clustering approach with the full data, try to filter out domains which have close by neighbours. This can be done using VP Trees
4 - Use a clustering technique that does not require knowing N a priori and that allows for complex clusters shape. DBSCAN can be good for this.



[1] T. Gowda and C. A. Mattmann, "Clustering Web Pages Based on Structure and Style Similarity (Application Paper)," 2016 IEEE 17th International Conference on Information Reuse and Integration (IRI), 2016, pp. 175-180, doi: 10.1109/IRI.2016.30.
