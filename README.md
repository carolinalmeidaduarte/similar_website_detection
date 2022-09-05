Similar website detection
==============================

In this repo we implement an efficient strategy to detect clusters of similar sites.
Similar sites are sites that are generated almost identically from the same template, i.e, both their internal structure and external visual look very similar.
A known strategy to exploit money from ads online is to create dummy sites and generate traffic through them. Since these sites are usually created in batches, we can use this tool to detect them.

## Past Work
T. Gowda and C. A. Mattmann [1] proposed a technique to detect similar web pages based on the structure and style similarity of the html, defined as:
- Structural similarity of HTML pages: measured by using Tree Edit Distance measure on DOM trees,
- Stylistic similarity: measured by using Jaccard similarity on CSS class names.

On top of these, an aggregated measure of similarity is proposed, combining structural and stylistic measures.
Since it is not possible to determine a priori the number of clusters - N - in the data, a technique that does not require N is needed. 
There is a python package that implements the described methodology: https://pypi.org/project/html-similarity/

## In this Repo
We want to apply html similarity to large-scale datasets. However, if we use the current methodology:

1. The similarity definition is good, but too slow
2. The cluster approach is not manageable for large datasets

In this repo we propose a new strategy that works like this:
1. We define a simpler way for representing the data. This can be based on some aggregated metrics about the html structure, such as tag counts. With such a vectorized representation, similarity becomes trivial - just a common distance metric can be used.
2. We improve the clustering computational performance by implementing a 2-step approach and then use a clustering technique on top of a much smaller and clean dataset.


[1] T. Gowda and C. A. Mattmann, "Clustering Web Pages Based on Structure and Style Similarity (Application Paper)," 2016 IEEE 17th International Conference on Information Reuse and Integration (IRI), 2016, pp. 175-180, doi: 10.1109/IRI.2016.30.

## How to run

### Step 1 - Collect Data
1. Define list of domains to scrape in `data/raw/target_domains.csv`
2. Scrape the domains using `src/data/extract_html_data.py`
3. Clean data using `src/data/clean_and_process_data.py`

### Step 2 - Get clusters 
1. Run `src/models/train_model.py` to do the 2-step clustering approach
2. Analyse the output clusters in `data/scored/similar_groups.csv`