import snip_h5py as snipH5
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import combinaison_camera

# reimport the data
folder_data = Path("./Comparaison_3D")
dict_final = snipH5.load_dictionary_from_hdf(folder_data / "comparaison_final_3d.h5")
dict_mean_std = snipH5.load_dictionary_from_hdf( folder_data/"mean_std_3d.h5")
dict_final_percentage = snipH5.load_dictionary_from_hdf(folder_data / "comparaison_percentage_3d.h5")

camera_configurations = list(dict_mean_std.keys())

list_model = list(dict_mean_std[camera_configurations[0]].keys())
key_points = list(dict_mean_std[camera_configurations[0]][list_model[0]].keys())

value_to_plot_list = ["X", "Y", "Z","norm"]
value_to_plot_list = ["norm"]
info = combinaison_camera.generate()
key_points = ["SJC", "EJC", "WJC", "HMJC"]
ax_y = []
for value_to_plot in value_to_plot_list:

    # Prepare the data for the box plot and percentage of NaN values
    data = []
    plot_outliers = False
    list_config_to_remove = []
    fig_full, ax_full = plt.subplots(2,2,sharey=True,figsize=(15, 10))

    for ind_point, points in enumerate(key_points):
        percentage_data = []
        for name_config in camera_configurations:
            list_camera = info[name_config]
            nb_camera = len(list_camera)
            for model in list_model:
                for value in dict_final[name_config][model][points][value_to_plot]:
                    data.append([name_config, model, points, nb_camera, value * 1000])
                percentage_data.append([name_config, model, points, nb_camera, dict_final_percentage[name_config][model][points]])

        # Create DataFrames
        df = pd.DataFrame(data, columns=['name_config', 'Model', 'Joint', 'nb_camera', 'Value'])
        df_percentage = pd.DataFrame(percentage_data, columns=['name_config', 'Model', 'Joint', 'nb_camera', 'Percentage'])
        # Assuming nb_camera is consistent for each 'name_config'
        desired_order = df.groupby('name_config')['nb_camera'].first().sort_values().index.tolist()

        # Create the box plot
        ind_row_graph = ind_point // 2
        ind_col_graph = ind_point % 2

        # Box plot
        sns.boxplot(x='name_config', y='Value', hue='nb_camera',palette=sns.color_palette('viridis',as_cmap=True), data=df,order=desired_order,showfliers=plot_outliers, ax=ax_full[ind_row_graph, ind_col_graph])
        ax_full[ind_row_graph, ind_col_graph].legend_ = None
        ax_full[ind_row_graph, ind_col_graph].tick_params(axis='x', rotation=45)
        if ind_row_graph==1:
            ax_full[ind_row_graph, ind_col_graph].set_xlabel('Camera configuration')

        if ind_col_graph==0:
            ax_full[ind_row_graph, ind_col_graph].set_ylabel('3D difference with reference in mm')
            if ind_row_graph==0:
                ax_full[ind_row_graph, ind_col_graph].legend(title='Number of cameras', loc='upper left',
                                                             ncol=len(df['nb_camera'].unique()))

        ax_full[ind_row_graph, ind_col_graph].set_title(f'{points}')




        # Create a second y-axis for the percentage of NaN values
        ax2 = ax_full[ind_row_graph, ind_col_graph].twinx()
        color_ax2 = (228/255,26/255,28/255)
        ax2.set_yscale("log")
        ax2.tick_params(axis='y', colors=color_ax2)
        ax2.spines['right'].set_color(color_ax2)
        ax_y.append(ax2)
        if ind_col_graph == 1:
            ax2.set_ylabel('Percentage of non reconstructed points in log scale (%)')
            ax2.yaxis.label.set_color(color_ax2)

        # Line plot for percentage of NaN values
        for name_config in df_percentage['name_config'].unique():
            for model in df_percentage['Model'].unique():
                subset = df_percentage[(df_percentage['name_config'] == name_config) & (df_percentage['Model'] == model)]
                ax2.plot(subset['name_config'], subset['Percentage'], marker='o', color=color_ax2, label=f'{name_config} - {model} NaN %')

        #ax2.legend(title='NaN Percentage', loc='upper right')

    ax_y[0].sharey(ax_y[1])
    ax_y[1].sharey(ax_y[2])
    ax_y[2].sharey(ax_y[3])
    fig_full.suptitle(f'Distribution {value_to_plot} of error and percentage of non reconstructed values')
    plt.rcParams.update({"font.size": 30})
    fig_full.tight_layout()

    # Save the figure
    folder_figure = Path("./figure")
    if not folder_figure.exists():
        folder_figure.mkdir()
    if plot_outliers:
        text_outliers = "with_outliers"
    else:
        text_outliers = "without_outliers"
    figure_name_png = f"3D_boxplot_all_point_percentage_nan_points_outliers={text_outliers}.png"
    figure_name_svg = f"3D_boxplot_all_point_percentage_nan_points_outliers={text_outliers}.svg"
    plt.savefig(folder_figure / figure_name_png, format="png")
    plt.savefig(folder_figure / figure_name_svg, format="svg")
    plt.show()