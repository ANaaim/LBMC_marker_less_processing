import numpy as np


def norm_vector(vector):
    """Transform any vector in the normed version of it."""
    # Normalisation des vecteurs
    vector_normed = (vector) / np.linalg.norm(vector, axis=0)
    return vector_normed
