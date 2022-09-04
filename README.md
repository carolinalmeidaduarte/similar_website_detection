Similar website detection
==============================

In this repo we implement an efficient strategy to detect clusters of similar sites.
Similar sites are sites that are generated almost identically from the same template, i.e, both their internal structure and external visual look very similar.
A known strategy to exploit money from ads online is to create dummy sites and generate traffic through them. Since these sites are usually created in batches, we can use this tool to detect them.

## Step 0 - Dependecies and run parameters
1. Install dependencies using `requirements.txt`
1. Define run parameters and input/output files `configuration.yaml` 

## Step 1 - Collect Data
1. Define list of domains to scrape in `data/raw/target_domains.csv`
2. Scrape the domains using `src/data/extract_html_data.py`
3. Clean data using `src/data/clean_and_process_data.py`

## Step 2 - Get clusters 
1. Run `src/models/train_model.py`
2. Analyse the output clusters in `data/scored/similar_groups.csv`