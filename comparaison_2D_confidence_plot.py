import snip_h5py as snipH5
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np


def plot_confidence_per_view(dict_final, view_to_plot, list_points, list_model, distance_threshold):

    nb_row = len(list_points)
    nb_col = len(list_model)


    # Create subplots grid (adjust figsize as needed)
    fig, axes = plt.subplots(nb_row, nb_col, figsize=(4 * nb_col, 4 * nb_row), squeeze=False)
    for i, point in enumerate(list_points):
        for j, model in enumerate(list_model):
            ax = axes[i, j]

            # Access the data for this model and point
            # Adjust the dictionary indexing if your structure is different.
            data = dict_final[model][view_to_plot][point]

            # Ensure data is a NumPy array (if not already)
            data = np.array(data)

            # Filter out points with distance >= threshold
            mask = data[:, 0] < distance_threshold
            distances = data[mask, 0]
            confidences = data[mask, 1]

            # Plot the hexbin plot in this subplot
            hb = ax.hexbin(distances, confidences, bins="log", gridsize=50, cmap='inferno')
            ax.set_title(f"{model} - {point}")
            ax.set_xlabel("Distance")
            ax.set_ylabel("Confidence")

            # Add a colorbar for each subplot
            fig.colorbar(hb, ax=ax, label="Count in bin")

    plt.suptitle(f"Confidence vs. Distance for {view_to_plot}")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":

    folder_data = Path("./Comparaison_2D")

    dict_final = snipH5.load_dictionary_from_hdf(folder_data / "comparaison_final.h5")


    # We will do a graph for each view of camera containing all the model and all points
    list_points = ["SJC","EJC","WJC","HMJC"]
    list_model = list(dict_final.keys())
    list_view = list(dict_final[list_model[0]].keys())

    for view in list_view:
        plot_confidence_per_view(dict_final,view, list_points,list_model, 200)






