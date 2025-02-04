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
camera_configurations = ["ABCDE"]
list_model = list(dict_mean_std[camera_configurations[0]].keys())
key_points = list(dict_mean_std[camera_configurations[0]][list_model[0]].keys())

value_to_plot_list = ["X", "Y", "Z","norm"]

info = combinaison_camera.generate()
for value_to_plot in value_to_plot_list:
    # plot box plot for each model and joint
    # Préparer les données pour le box plot
    data = []
    for points in key_points:
        for name_config in camera_configurations:
            list_camera = info[name_config]
            nb_camera = len(list_camera)
            for model in list_model:
                    for value in dict_final[name_config][model][points][value_to_plot]:
                        data.append([name_config, model, points,nb_camera, value*1000])

        # Example usage
        df = pd.DataFrame(data, columns=['name_config','Model', "Joint",'nb_camera', 'Value'])
        # df_cleaned = remove_outliers(df, 'Value')

        # Plot the cleaned data
        plt.figure(figsize=(15, 10))
        sns.boxplot(x='name_config', y='Value', hue='nb_camera', data=df,  showfliers=False)
        plt.title(points)
        name_figure_svg = points+".svg"
        name_figure_png = points+".png"
        folder_figure = Path("./figure")
        # check if the folder exist
        if not folder_figure.exists():
            folder_figure.mkdir()
        plt.savefig(folder_figure / name_figure_png, format="png")
        plt.savefig(folder_figure/ name_figure_svg,format="svg")
        plt.show()


    # Prepare the data for the box plot and percentage of NaN values
    data = []
    plot_outliers = False
    list_config_to_remove = []

    for points in key_points:
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

        # Plot the data
        fig, ax1 = plt.subplots(figsize=(15, 10))

        # Box plot
        sns.boxplot(x='name_config', y='Value', hue='nb_camera', data=df, showfliers=plot_outliers, ax=ax1)
        ax1.set_xlabel('Camera configuration')
        ax1.set_ylabel('Value (mm)')
        ax1.set_title(f'Distribution {value_to_plot} of error and percentage of non reconstructed values for {points}')
        ax1.legend(title='Configuration', loc='upper left')
        ax1.tick_params(axis='x', rotation=45)

        # Create a second y-axis for the percentage of NaN values
        ax2 = ax1.twinx()
        ax2.set_ylabel('Percentage of non reconstructed points')

        # Line plot for percentage of NaN values
        for name_config in df_percentage['name_config'].unique():
            for model in df_percentage['Model'].unique():
                subset = df_percentage[(df_percentage['name_config'] == name_config) & (df_percentage['Model'] == model)]
                ax2.plot(subset['name_config'], subset['Percentage'], marker='o', label=f'{name_config} - {model} NaN %')

        #ax2.legend(title='NaN Percentage', loc='upper right')

        fig.tight_layout()

        # Save the figure
        folder_figure = Path("./figure")
        if not folder_figure.exists():
            folder_figure.mkdir()
        if plot_outliers:
            text_outliers = "with_outliers"
        else:
            text_outliers = "without_outliers"
        figure_name_png = f"{points}_{value_to_plot}_boxplot_percentage_nan_points_outliers={text_outliers}.png"
        figure_name_svg = f"{points}_{value_to_plot}_boxplot_percentage_nan_points_outliers={text_outliers}.svg"
        plt.savefig(folder_figure / figure_name_png, format="png")
        plt.savefig(folder_figure / figure_name_svg, format="svg")
        plt.show()