import snip_h5py as snipH5
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np


def plot_confidence_per_view(dict_final, view_to_plot, list_points, list_model,correction_confidence, distance_threshold):
    nb_row = len(list_points)
    nb_col = len(list_model)

    # First pass: compute global extent across all data to standardize the hexbin bins
    all_distances = []
    all_confidences = []
    for point in list_points:
        for ind_model,model in enumerate(list_model):
            data = np.array(dict_final[model][view_to_plot][point])
            mask = data[:, 0] < distance_threshold
            distances = data[mask, 0]
            confidences = data[mask, 1]/correction_confidence[ind_model]
            all_distances.append(distances)
            all_confidences.append(confidences)

    # Concatenate all data to determine global min and max
    all_distances = np.concatenate(all_distances)
    all_confidences = np.concatenate(all_confidences)
    global_extent = (all_distances.min(), all_distances.max(),
                     0.0, 1.0)

    # Create subplots grid
    fig, axes = plt.subplots(nb_row, nb_col, figsize=(4 * nb_col, 4 * nb_row), squeeze=False)
    hb_list = []  # store hexbin objects for uniform color scaling

    # Plot each subplot using the same extent
    for i, point in enumerate(list_points):
        for j, model in enumerate(list_model):
            ax = axes[i, j]
            # Access the data for this model and point
            data = np.array(dict_final[model][view_to_plot][point])
            mask = data[:, 0] < distance_threshold
            distances = data[mask, 0]
            confidences = data[mask, 1]/correction_confidence[j]

            # Plot the hexbin plot in this subplot with the common extent
            hb = ax.hexbin(distances, confidences, bins="log", gridsize=50,
                           cmap='inferno', extent=global_extent)
            hb_list.append(hb)
            ax.set_title(f"{model} - {point}")
            ax.set_xlabel("Distance")
            ax.set_ylabel("Confidence")
            fig.colorbar(hb, ax=ax, label="Count in bin")

    # # Determine global color limits from all hexbin plots
    global_min = min(hb.get_array().min() for hb in hb_list if hb.get_array().size > 0)
    global_max = max(hb.get_array().max() for hb in hb_list if hb.get_array().size > 0)
    if global_min ==0.0:
        # to avoid problem with log scale
        global_min = 1.0
    for hb in hb_list:
         hb.set_clim(global_min, global_max)

    # # Add a single colorbar for the entire figure using one of the hexbin plots
    #fig.colorbar(hb_list[0], ax=axes, label="Count in bin")

    plt.suptitle(f"Confidence vs. Distance for {view_to_plot}")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":

    folder_data = Path("./Comparaison_2D")

    dict_final = snipH5.load_dictionary_from_hdf(folder_data / "comparaison_final.h5")


    # We will do a graph for each view of camera containing all the model and all points
    list_points = ["SJC","EJC","WJC","HMJC"]
    #list_model = list(dict_final.keys())
    list_model = ['all_body_hrnet_coco_dark_coco_hdf5', 'all_body_resnet_hdf5', 'all_body_rtm_coktail_14_hdf5']
    correction_confidence =[1,1,10]
    list_view = list(dict_final[list_model[0]].keys())


    for view in list_view:
        plot_confidence_per_view(dict_final,view, list_points,list_model,correction_confidence, 200)






