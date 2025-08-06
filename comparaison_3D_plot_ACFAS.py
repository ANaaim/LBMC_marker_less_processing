from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

import snip_h5py as snipH5
import data_dictionary

def plot_distances_boxplots(dict_comp_population, models, populations, points, 
                            model_colors, pop_bg_colors,task_to_plot="All", width=0.6,
                            name_subject=None):
    """
    dict_comp_population: nested dict[model]["All"][population][point] → 1D array of distances
    models: list of model names, in the order you want their boxes
    populations: list of populations, e.g. ["Pop1", "Pop2"]
    points: list of point names, e.g. ["A", "B", "C"]
    model_colors: dict[model] → matplotlib color
    pop_bg_colors: dict[population] → background color (with alpha<1)
    width: total width allocated per (point, population) group
    """
    n_models = len(models)
    n_pops   = len(populations)
    n_points = len(points)
    
    # Compute x positions
    # Each "point" has n_pops groups; each group spans width.
    # Within each group, n_models boxes evenly spaced.
    group_sep = width * n_models  # separation between populations
    total_sep = width * n_models * n_pops  # separation per point
    x_positions = []
    for pi, point in enumerate(points):
        base = pi * total_sep * 1.5  # add extra gap between points
        for qi, pop in enumerate(populations):
            for mi, model in enumerate(models):
                x = base + qi * group_sep + (mi + 0.5) * width
                x_positions.append(x)
    # now build the data list in same order
    data = []
    for point in points:
        for pop in populations:
            for model in models:
                arr = dict_comp_population[model][task_to_plot][pop][point]
                # turn list or array into numpy array
                arr = np.asarray(arr)
                # remove NaNs
                arr_clean = arr[~np.isnan(arr)]
                data.append(arr_clean)
                
    # make the figure
    fig, ax = plt.subplots(figsize=(1.5*n_points*n_pops, 6))
    
    # shade populations
    for pi, point in enumerate(points):
        base = pi * total_sep * 1.5
        for qi, pop in enumerate(populations):
            start = base + qi * group_sep
            end   = start + width * n_models
            ax.axvspan(start, end, color=pop_bg_colors[pop], alpha=0.2, 
                       label=f"{pop}" if pi==0 else "")
    
    # draw boxes
    bp = ax.boxplot(
        data,
        positions=x_positions,
        widths=width*0.8,
        patch_artist=True,
        manage_ticks=False,
        showfliers=True,
    )
    # color them by model
    for i, patch in enumerate(bp['boxes']):
        model = models[i % n_models]
        patch.set_facecolor(model_colors[model])
    
    # X-ticks: center under each (point)
    xticks = []
    xlabels = []
    for pi, point in enumerate(points):
        group_center = pi * total_sep * 1.5 + total_sep/2
        xticks.append(group_center)
        xlabels.append(point)
    ax.set_xticks(xticks)
    ax.set_xticklabels(xlabels, fontsize=12)
    
    # Change the y-axis limits
    y_min = 0
    y_max = 0.20
    ax.set_ylim(y_min, y_max)
    # legend: points as legend handles
    handles = [
        plt.Line2D([0], [0], color=model_colors[m], lw=10) 
        for m in models
    ]
    ax.legend(handles, models, title="Models", loc="upper right")
    
    ax.set_ylabel("Distance to point (m)")
    ax.set_title("Distance distributions by point, population and model")
    plt.tight_layout()
    #plt.show()
    # Save the figure
    # Create the directory if it doesn't exist
    path_figure = Path("./ACFAS/figures")
    
    if name_subject is not None:
        path_figure = path_figure / name_subject
    
    if not path_figure.exists():
        path_figure.mkdir(parents=True, exist_ok=True)
    
    filename = f"boxplot_{task_to_plot}.png"
    
    fig.savefig(path_figure / filename, dpi=300, bbox_inches='tight')
    plt.close(fig)

def plot_distances_boxplots_v2(dict_comp_population, models, populations, points, points_names, 
                            model_colors, pop_bg_colors, task_to_plot="All", 
                            width=0.6, name_subject=None,model_legends=None):
    """
    dict_comp_population: nested dict[model][task_to_plot][population][point] → 1D array of distances
    models: list of model names
    populations: list of population names, e.g. ["Pop1","Pop2"]
    points: list of point names, e.g. ["A","B","C"]
    model_colors: dict mapping model → color
    pop_bg_colors: dict mapping population → background color
    """
    n_models = len(models)
    n_pops   = len(populations)
    n_points = len(points)

    font_size = 20

    # layout helpers
    group_sep = width * n_models
    total_sep = group_sep * n_pops

    # 1) build x-positions
    x_positions = []
    for pi in range(n_points):
        base = pi * total_sep * 1.5
        for qi in range(n_pops):
            for mi in range(n_models):
                x_positions.append(base + qi*group_sep + (mi+0.5)*width)

    # 2) collect & clean data
    data = []
    for point in points:
        for pop in populations:
            for model in models:
                arr = np.asarray(dict_comp_population[model][task_to_plot][pop][point])
                arr = arr[~np.isnan(arr)]
                data.append(arr)

    # 3) plot setup
    fig, ax = plt.subplots(figsize=(1.5*n_points*n_pops, 6))

    # 4) shading (no labels yet)
    for pi in range(n_points):
        base = pi * total_sep * 1.5
        for qi, pop in enumerate(populations):
            start = base + qi*group_sep
            end   = start + width*n_models
            ax.axvspan(start, end, color=pop_bg_colors[pop], alpha=0.2)

    # 5) boxplots
    bp = ax.boxplot(
        data,
        positions=x_positions,
        widths=width*0.8,
        patch_artist=True,
        manage_ticks=False,
        showfliers=True,
    )
    for i, patch in enumerate(bp['boxes']):
        patch.set_facecolor(model_colors[models[i % n_models]])

    # 6) axes tweaks
    # X-ticks at point-centers
    xticks = [pi*total_sep*1.5 + total_sep/2 for pi in range(n_points)]
    ax.set_xticks(xticks)
    ax.set_xticklabels(points_names, fontsize=font_size)

    # Y-limits
    ax.set_ylim(0, 0.1)

    # 7) draw population labels **inside** the plot
    for pi in range(n_points):
        base = pi * total_sep * 1.5
        for qi, pop in enumerate(populations):
            start = base + qi*group_sep
            end   = start + width*n_models
            center = (start + end) / 2
            ax.text(
                center, 0.95, pop,
                ha="center", va="top",
                transform=ax.get_xaxis_transform(),
                fontsize=font_size,
                #bbox=dict(
                #    facecolor=pop_bg_colors[pop],
                #    alpha=0.3,
                #    edgecolor="none"
                #),
                clip_on=False
            )

    # 8) legend for models using model_legends if provided
    handles = [
        plt.Line2D([0], [0], color=model_colors[m], lw=10)
        for m in models
    ]
    labels = [
        model_legends.get(m, m) if model_legends else m
        for m in models
    ]
    ax.legend(
        handles, labels,
        loc="lower center",
        bbox_to_anchor=(0.5, -0.25),
        ncol=n_models,
        frameon=False,
        fontsize=font_size,
    )

    ax.set_ylabel("3D difference with reference (m)",fontsize=font_size)
    ax.set_title("Distance distributions by point, population and model", fontsize=font_size)
    # change the sie of the textr on th y tick
    for tick in ax.get_yticklabels():
        tick.set_fontsize(font_size-3)

    # 9) save
    path_figure = Path("./ACFAS/figures")
    if name_subject:
        path_figure /= name_subject
    path_figure.mkdir(parents=True, exist_ok=True)
    fig.savefig(path_figure / f"boxplot_{task_to_plot}.png",
                dpi=300, bbox_inches="tight")
    plt.close(fig)

def plot_distances_violin(
    dict_comp_population,
    models,
    populations,
    points,
    model_colors,
    pop_bg_colors,
    task_to_plot="All",
    width=0.6,
    name_subject=None,
    model_legends=None
):
    """
    Now renders violins instead of boxplots.
    """
    n_models = len(models)
    n_pops   = len(populations)
    n_points = len(points)
    font_size = 20

    # sizing
    group_sep = width * n_models
    total_sep = group_sep * n_pops

    # 1) x positions
    x_positions = []
    for pi in range(n_points):
        base = pi * total_sep * 1.5
        for qi in range(n_pops):
            for mi in range(n_models):
                x_positions.append(base + qi*group_sep + (mi+0.5)*width)

    # 2) gather & clean
    data = []
    for point in points:
        for pop in populations:
            for model in models:
                arr = np.asarray(
                    dict_comp_population[model][task_to_plot][pop][point]
                )
                data.append(arr[~np.isnan(arr)])

    # 3) figure
    fig, ax = plt.subplots(figsize=(1.5*n_points*n_pops, 6))
    fig.subplots_adjust(bottom=0.30)

    # 4) shade populations
    for pi in range(n_points):
        base = pi * total_sep * 1.5
        for qi, pop in enumerate(populations):
            start = base + qi*group_sep
            end   = start + width*n_models
            ax.axvspan(start, end, color=pop_bg_colors[pop], alpha=0.2)

    # 5) violin plot
    vp = ax.violinplot(
        data,
        positions=x_positions,
        widths=width*0.8,
        showmeans=False,
        showextrema=False,
        showmedians=True
    )
    for i, body in enumerate(vp['bodies']):
        col = model_colors[models[i % n_models]]
        body.set_facecolor(col)
        body.set_edgecolor('black')
        body.set_alpha(0.7)
    # optional: style median lines if you want:
    if 'cmedians' in vp:
        vp['cmedians'].set_color('black')
        vp['cmedians'].set_linewidth(2)

    # 6) x‐axis
    xticks = [pi*total_sep*1.5 + total_sep/2 for pi in range(n_points)]
    ax.set_xticks(xticks)
    ax.set_xticklabels(points, fontsize=font_size)
    ax.set_ylim(0, 0.20)

    # 7) population labels inside
    for pi in range(n_points):
        base = pi * total_sep * 1.5
        for qi, pop in enumerate(populations):
            start = base + qi*group_sep
            end   = start + width*n_models
            center = (start + end) / 2
            ax.text(
                center, 0.95, pop,
                ha="center", va="top",
                transform=ax.get_xaxis_transform(),
                fontsize=font_size,
                clip_on=False
            )

    # 8) horizontal legend below
    handles = [
        plt.Line2D([0], [0], color=model_colors[m], lw=10)
        for m in models
    ]
    labels = [
        model_legends.get(m, m) if model_legends else m
        for m in models
    ]
    ax.legend(
        handles, labels,
        loc="upper center",
        bbox_to_anchor=(0.5, -0.25),
        ncol=n_models,
        frameon=False,
        fontsize=font_size
    )

    ax.set_ylabel("Distance to point (m)", fontsize=font_size)
    ax.set_title("Distance distributions by point, population and model", fontsize=font_size)

    # 9) save
    path_figure = Path("./ACFAS/figures")
    if name_subject:
        path_figure /= name_subject
    path_figure.mkdir(parents=True, exist_ok=True)
    fig.savefig(path_figure / f"violin_{task_to_plot}.png", dpi=300, bbox_inches="tight")
    plt.close(fig)

# reimport the data
folder_data = Path("./Comparaison_3D")
dict_final_population = snipH5.load_dictionary_from_hdf(folder_data / "comparaison_population_3d.h5")
dict_mean_population = snipH5.load_dictionary_from_hdf(folder_data / "mean_std_3d.h5")
dict_final_population = dict_final_population["ABCDE"]
#models = list(dict_final_population.keys())
models = ['all_body_hrnet_coco_dark_coco_hdf5', 'all_body_resnet_hdf5', 'all_body_rtm_coktail_14_hdf5']
models =['all_body_rtm_coktail_14_hdf5']
model_legends = {
    "all_body_hrnet_coco_dark_coco_hdf5":"HRNet",
    "all_body_resnet_hdf5":"ResNet",
    "all_body_rtm_coktail_14_hdf5":"RTM",
}
#populations = list(dict_final_population[models[0]]["All"].keys())
populations = ["TDC", "CP"]
#points     = list(dict_final_population[models[0]]["All"][populations[0]].keys())
points      = ['SJC', 'EJC', 'WJC', 'HMJC']
points_names =['Shoulder', 'Elbow', 'Wrist', 'Hand']
# pick distinct colors for each model
model_colors = {
    "all_body_hrnet_coco_dark_coco_hdf5":"C0",
    "all_body_resnet_hdf5":"C4",
    "all_body_rtm_coktail_14_hdf5":"C2",
}
# subtle background hues for populations
pop_bg_colors = {
    "CP":"skyblue",
    "TDC":"lightcoral",
}

list_tasks = ["01_Shoulder_Abduction_Adduction","02_Shoulder_Flexion_Extension",
                                   "05_Elbow_Pronosupination_Bras_Bend","06_Elbow_Flexion_Extension",
                                   "11_Hand_to_Head","12_Reaches_And_Manipulation",
                                   "13_Open_a_Bottle_and_Pour","19_Cymbals","All"]
for task in list_tasks:
    print(task)
    plot_distances_boxplots_v2(
        dict_final_population,
        models, populations, points, points_names,
        model_colors, pop_bg_colors,
        task_to_plot=task,
        width=0.6,
        name_subject=None,
        model_legends=model_legends,
    )



# Generate 3d_to_2d hdf5 ------------------------------------------------
study = data_dictionary.CRME_study_ISB()
study = data_dictionary.remove_tasks(study, ["00_S"])
# study = data_dictionary.remove_subjects(study, ["Subject_04_TDC","Subject_05_TDC","Subject_02_CP","Subject_05_CP","Subject_06_TDC","Subject_07_TDC","Subject_08_TDC"
#                                                     ,"Subject_06_CP","Subject_07_CP","Subject_08_CP",])

study = data_dictionary.remove_subjects(study, ["Subject_09_TDC","Subject_10_TDC","Subject_11_TDC"
                                                     ,"Subject_09_CP","Subject_10_CP",])

sujet_to_list_task = study["task"]
subjects_names = list(study["task"].keys())

for subject_name in subjects_names:
    # Get the list of tasks for the current subject
    list_task = study["task"][subject_name]
    # clean the name of the list of tasks removing _000 and _001 from the name
    list_task = [task.replace("_000", "").replace("_001", "") for task in list_task]
    populations = [subject_name]
    pop_bg_colors[subject_name] = "white"
    for task in list_task:
        plot_distances_boxplots(
            dict_final_population,
            models, populations, points,
            model_colors, pop_bg_colors,
            task_to_plot=task,
            width=0.6,
            name_subject=subject_name,
        )

    



