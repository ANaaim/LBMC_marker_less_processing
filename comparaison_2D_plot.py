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

value_to_plot_list = ["X"]#, "Y", "Z","norm"]

for value_to_plot in value_to_plot_list:
    # plot box plot for each model and joint
    # Prepare the data for the box plot and percentage of NaN values
    data = []
    plot_outliers = False
    list_config_to_remove = []

    for points in key_points:
        percentage_data = []
        for name_config in camera_configurations:
            for model in list_model:
                for value in dict_final[model][name_config][points]:
                    data.append([model, name_config, points, value])

        # Create DataFrames
        df = pd.DataFrame(data, columns=['Model', 'name_config', 'Joint', 'Value'])

        # Plot the data
        fig, ax1 = plt.subplots(figsize=(15, 10))

        # Box plot
        sns.boxplot(x='name_config', y='Value',hue="Model", data=df, showfliers=plot_outliers, ax=ax1)
        ax1.set_xlabel('Camera configuration')
        ax1.set_ylabel('Value (mm)')
        ax1.set_title(f'Distribution {value_to_plot} of error and percentage of non reconstructed values for {points}')
        ax1.legend(title='Configuration', loc='upper left')
        ax1.tick_params(axis='x', rotation=45)


        #ax2.legend(title='NaN Percentage', loc='upper right')

        fig.tight_layout()

        # Save the figure
        folder_figure = Path("./Comparaison_2D/figure")
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