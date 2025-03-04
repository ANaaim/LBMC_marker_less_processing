import snip_h5py as snipH5
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import combinaison_camera

# reimport the data
folder_data = Path("./Comparaison_2D")
dict_final = snipH5.load_dictionary_from_hdf(folder_data / "comparaison_final.h5")
dict_mean_std = snipH5.load_dictionary_from_hdf( folder_data/"mean_std.h5")

list_model = list(dict_final.keys())
camera_configurations = list(dict_final[list_model[0]].keys())
key_points = list(dict_final[list_model[0]][camera_configurations[0]].keys())

value_to_plot_list = ["norm"]#, "Y", "Z","norm"]

# for value_to_plot in value_to_plot_list:
#     # plot box plot for each model and joint
#     # Prepare the data for the box plot and percentage of NaN values
#     data = []
#     plot_outliers = False
#     list_config_to_remove = []
#     nb_keypoints = len(key_points)
#     for points in key_points:
#         percentage_data = []
#         for name_config in camera_configurations:
#             for model in list_model:
#                 for value in dict_final[model][name_config][points]:
#                     data.append([model, name_config, points, value])
#
#         # Create DataFrames
#         df = pd.DataFrame(data, columns=['Model', 'name_config', 'Joint', 'Value'])
#
#         # Plot the data
#         fig, ax1 = plt.subplots(figsize=(15, 10))
#
#         # Box plot
#         sns.boxplot(x='name_config', y='Value',hue="Model", data=df, showfliers=plot_outliers, ax=ax1)
#         ax1.set_xlabel('Camera configuration')
#         ax1.set_ylabel('Value (mm)')
#         ax1.set_title(f'Distribution {value_to_plot} of error and percentage of non reconstructed values for {points}')
#         ax1.legend(title='Configuration', loc='upper left')
#         ax1.tick_params(axis='x', rotation=45)
#
#
#         #ax2.legend(title='NaN Percentage', loc='upper right')
#
#         fig.tight_layout()
#
#         # Save the figure
#         folder_figure = Path("./Comparaison_2D/figure")
#         if not folder_figure.exists():
#             folder_figure.mkdir()
#         if plot_outliers:
#             text_outliers = "with_outliers"
#         else:
#             text_outliers = "without_outliers"
#         figure_name_png = f"{points}_{value_to_plot}_boxplot_percentage_nan_points_outliers={text_outliers}.png"
#         figure_name_svg = f"{points}_{value_to_plot}_boxplot_percentage_nan_points_outliers={text_outliers}.svg"
#         plt.savefig(folder_figure / figure_name_png, format="png")
#         plt.savefig(folder_figure / figure_name_svg, format="svg")
#         plt.show()

data = []
plot_outliers = False
list_config_to_remove = []
nb_keypoints = len(key_points)
key_points = ['SJC', 'EJC', 'WJC', 'HMJC']
# Plot the data
fig_full, ax_full = plt.subplots(2,2,sharey=True,figsize=(15, 10))
for ind_point,points in enumerate(key_points):
    percentage_data = []
    for name_config in camera_configurations:
        for model in list_model:
            for value in dict_final[model][name_config][points]:
                data.append([model, name_config, points, value])

    # Create DataFrames
    df = pd.DataFrame(data, columns=['Model', 'name_config', 'Joint', 'Value'])
    # change the name of the model
    df['Model'] = df['Model'].replace('all_body_hrnet_coco_dark_coco_hdf5', 'HRNET')
    df['Model'] = df['Model'].replace('all_body_resnet_hdf5', 'ResNet')
    df['Model'] = df['Model'].replace('all_body_rtm_coktail_14_hdf5', 'RTM')


    ind_row_graph = ind_point // 2
    ind_col_graph = ind_point % 2
    # Box plot
    sns.boxplot(x='name_config', y='Value',hue="Model", data=df, showfliers=plot_outliers, ax=ax_full[ind_row_graph,ind_col_graph])

    ax_full[ind_row_graph, ind_col_graph].legend_ = None
    if ind_row_graph ==1 :
        ax_full[ind_row_graph,ind_col_graph].set_xlabel('Camera configuration')
    if ind_col_graph == 0:
        ax_full[ind_row_graph,ind_col_graph].set_ylabel('2D difference with reference in px')

    if ind_row_graph ==0:
        if ind_col_graph==0:
            ax_full[ind_row_graph,ind_col_graph].legend(title='', loc='upper left',ncol=len(df['Model'].unique()))

    ax_full[ind_row_graph, ind_col_graph].set_title(f'{points}')
    ax_full[ind_row_graph,ind_col_graph].tick_params(axis='x', rotation=0)


    #ax2.legend(title='NaN Percentage', loc='upper right')

#fig_full.suptitle(f'Distribution of the 2D difference error  {points}')
plt.rcParams.update({"font.size":40})
fig_full.tight_layout()

# Save the figure
folder_figure = Path("./Comparaison_2D/figure")
if not folder_figure.exists():
    folder_figure.mkdir()
if plot_outliers:
    text_outliers = "with_outliers"
else:
    text_outliers = "without_outliers"
figure_name_png = f"2D_boxplot_all_point_percentage_{text_outliers}.png"
figure_name_svg = f"2D_boxplot_all_point_percentage_{text_outliers}.svg"
plt.savefig(folder_figure / figure_name_png, format="png")
plt.savefig(folder_figure / figure_name_svg, format="svg")
plt.show()