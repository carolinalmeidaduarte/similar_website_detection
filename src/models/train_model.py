import vptree
import datetime
import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN
import pickle
from src.utils.utils import *

def reshape_as_input_features(data):
    features = ["div", "ul", "li", "a", "img", "span"]
    return data[features].to_numpy()


def distance_metric(a, b):
    # define distance as the percentage of difference between 2 vectors over the smallest norm
    return np.sum(np.abs(a - b)) / min(np.sum(a), np.sum(b)) + \
           0.02 * (1 - len(np.where((a - b == 0) & (a > 0) & (b > 0))[0]) / len(a))


if __name__ == "__main__":
    start_time = datetime.datetime.now()

    logger = get_logger(__name__, "log_data")

    data = pd.read_csv(
        get_path_to_file(get_config_parameter("processed_data")),
        index_col=False)

    train_data = reshape_as_input_features(data)
    tree = vptree.VPTree(train_data, distance_metric)
    pickle.dump(tree, open(get_path_to_file(get_config_parameter("vp_tree_model")), 'wb'))

    logger.info(
        " training took: {}".format(dir(tree))
    )
    data["number_similar_sites"] = [
        len(tree.get_all_in_range(site, get_config_parameter("max_distance_between_similar_sites")))
        for site in train_data
    ]

    suspicious_sites = data[
        data["number_similar_sites"] >= get_config_parameter("min_number_similar_sites")
        ]

    dbscan = DBSCAN(
        metric=distance_metric,
        eps=get_config_parameter("max_distance_between_similar_sites"),
        min_samples=get_config_parameter("min_number_similar_sites"),
        n_jobs=-1
    )
    dbscan.fit(reshape_as_input_features(suspicious_sites))
    pickle.dump(dbscan, open(get_path_to_file(get_config_parameter("dbscan_model")), 'wb'))

    suspicious_sites.loc[:, "cluster_id"] = dbscan.labels_

    suspicious_sites.to_csv(get_path_to_file(get_config_parameter("scored_data")))
    # log execution time
    end_time = datetime.datetime.now()
    logger.info(
        " training took: {}".format((end_time - start_time).total_seconds())
    )