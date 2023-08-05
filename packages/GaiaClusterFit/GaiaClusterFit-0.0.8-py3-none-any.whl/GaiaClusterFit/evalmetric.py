import sklearn as sk
import numpy as np

def homogeneityscore(dataselection, regiondata,data=None):
    """Cross-match-scores 2 sets of clustered data on a homogeneity score
    Args:
        dataselection (astropy.Table): Astropy Table that includes all imported Gaia data of the Queried region.
        regiondata (astropy.Table): Astropy Table that includes all imported luster data .

    Returns:
        Float: The return value. True for success, False otherwise.
    """
    redundant,spots1, spots2 = np.intersect1d(dataselection["source_id"],regiondata["source_id"],return_indices=True)
    predicted_common_elements = dataselection[spots1].group_by("source_id")
    true_common_elements = regiondata[spots2].group_by("source_id")
    placeholder = np.array([np.where(np.unique(predicted_common_elements["population"]) == i)[0][0] for i in predicted_common_elements["population"]])
    score = sk.metrics.homogeneity_score(true_common_elements["population"],placeholder)
    return score

def completenessscore(dataselection, regiondata,data=None):
    """Cross-match-scores 2 sets of clustered data on a homogeneity score
    Args:
        dataselection (astropy.Table): Astropy Table that includes all imported Gaia data of the Queried region.
        regiondata (astropy.Table): Astropy Table that includes all imported luster data .

    Returns:
        Float: The return value. True for success, False otherwise.
    """

    redundant,spots1, spots2 = np.intersect1d(dataselection["source_id"],regiondata["source_id"],return_indices=True)
    predicted_common_elements = dataselection[spots1].group_by("source_id")
    true_common_elements = regiondata[spots2].group_by("source_id")
    placeholder = np.array([np.where(np.unique(predicted_common_elements["population"]) == i)[0][0] for i in predicted_common_elements["population"]])
       
    score = sk.metrics.completeness_score(true_common_elements["population"], placeholder)
    return score


def randscore(dataselection, regiondata,data=None):
    """Cross-match-scores 2 sets of clustered data on a homogeneity score
    Args:
        dataselection (astropy.Table): Astropy Table that includes all imported Gaia data of the Queried region.
        regiondata (astropy.Table): Astropy Table that includes all imported luster data .

    Returns:
        Float: The return value. True for success, False otherwise.
    """

    redundant,spots1, spots2 = np.intersect1d(dataselection["source_id"],regiondata["source_id"],return_indices=True)
    predicted_common_elements = dataselection[spots1].group_by("source_id")
    true_common_elements = regiondata[spots2].group_by("source_id")
    placeholder = np.array([np.where(np.unique(predicted_common_elements["population"]) == i)[0][0] for i in predicted_common_elements["population"]])
         
    score = sk.metrics.rand_score(true_common_elements["population"], placeholder)
    return score

def calinskiharabaszscore(dataselection, regiondata,data=None):
    """Cross-match-scores 2 sets of clustered data on a homogeneity score
    Args:
        dataselection (astropy.Table): Astropy Table that includes all imported Gaia data of the Queried region.
        regiondata (astropy.Table): Astropy Table that includes all imported luster data .

    Returns:
        Float: The return value. True for success, False otherwise.
    """

    redundant,spots1, spots2 = np.intersect1d(dataselection["source_id"],regiondata["source_id"],return_indices=True)
    predicted_common_elements = dataselection[spots1].group_by("source_id")
    true_common_elements = regiondata[spots2].group_by("source_id")
    placeholder = np.array([np.where(np.unique(predicted_common_elements["population"]) == i)[0][0] for i in predicted_common_elements["population"]])
    
    score = sk.metrics.calinski_harabasz_score(true_common_elements["population"], placeholder)
    return score

def mutualinfoscore(dataselection, regiondata,data=None):
    """Cross-match-scores 2 sets of clustered data on a homogeneity score
    Args:
        dataselection (astropy.Table): Astropy Table that includes all imported Gaia data of the Queried region.
        regiondata (astropy.Table): Astropy Table that includes all imported luster data .

    Returns:
        Float: The return value. True for success, False otherwise.
    """

    redundant,spots1, spots2 = np.intersect1d(dataselection["source_id"],regiondata["source_id"],return_indices=True)
    predicted_common_elements = dataselection[spots1].group_by("source_id") #put elements in the same order
    true_common_elements = regiondata[spots2].group_by("source_id") #put elements in the same order
    placeholder = np.array([np.where(np.unique(predicted_common_elements["population"]) == i)[0][0] for i in predicted_common_elements["population"]])#convert any cluster naming scheme to a population number
    
    score = sk.metrics.mutual_info(true_common_elements["population"], placeholder)
    return score

def daviesbouldinscore(dataselection, regiondata,data=None):
    """Cross-match-scores 2 sets of clustered data on a homogeneity score
    Args:
        dataselection (astropy.Table): Astropy Table that includes all imported Gaia data of the Queried region.
        regiondata (astropy.Table): Astropy Table that includes all imported luster data .

    Returns:
        Float: The return value. True for success, False otherwise.
    """

    redundant,spots1, spots2 = np.intersect1d(dataselection["source_id"],regiondata["source_id"],return_indices=True)
    predicted_common_elements = dataselection[spots1].group_by("source_id") #put elements in the same order
    true_common_elements = regiondata[spots2].group_by("source_id") #put elements in the same order
    placeholder = np.array([np.where(np.unique(predicted_common_elements["population"]) == i)[0][0] for i in predicted_common_elements["population"]])#convert any cluster naming scheme to a population number
    
    score = sk.metrics.davies_bouldin_score(true_common_elements["population"],placeholder)
    return score

def vmeasurescore(dataselection, regiondata,data=None):
    """Cross-match-scores 2 sets of clustered data on a v-measure score
    Args:
        dataselection (astropy.Table): Astropy Table that includes all imported Gaia data of the Queried region.
        regiondata (astropy.Table): Astropy Table that includes all imported luster data .

    Returns:
        Float: Score between 0 and 1
    """

    redundant,spots1, spots2 = np.intersect1d(dataselection["source_id"],regiondata["source_id"],return_indices=True)
    predicted_common_elements = dataselection[spots1].group_by("source_id") #put elements in the same order
    true_common_elements = regiondata[spots2].group_by("source_id") #put elements in the same order
    placeholder = np.array([np.where(np.unique(predicted_common_elements["population"]) == i)[0][0] for i in predicted_common_elements["population"]])#convert any cluster naming scheme to a population number
      
    score = sk.metrics.v_measure_score(true_common_elements["population"],placeholder)
    return score


def silhouettescore(dataselection, regiondata,data=None):
    """Cross-match-scores 2 sets of clustered data on a homogeneity score
    Args:
        dataselection (astropy.Table): Astropy Table that includes all imported Gaia data of the Queried region.
        regiondata (astropy.Table): Astropy Table that includes all imported luster data .

    Returns:
        Float: The return value. True for success, False otherwise.
        
    """
    print(np.unique(dataselection["population"]))
    try:
        
        score = sk.metrics.silhouette_score(np.array(data).T,dataselection["population"])
        print(score)
        return score

    except Exception as e:
        print("Could not compute silhouette score")
        print(f"Error message:{e}")
        return float("nan")

