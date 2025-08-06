
import snip_h5py as snipH5
from pathlib import Path
import numpy as np
# reimport the data
folder_data = Path("./Comparaison_3D")
dict_final_population = snipH5.load_dictionary_from_hdf(folder_data / "comparaison_population_3d.h5")
dict_final = dict_final_population["ABCDE"]
a=1

list_model = models = ['all_body_hrnet_coco_dark_coco_hdf5', 'all_body_resnet_hdf5', 'all_body_rtm_coktail_14_hdf5']
list_pop = ['TDC', 'CP']
list_joint = ['SJC', 'EJC','WJC','HMJC']
for joint in list_joint:
    for pop in list_pop:
        for model in list_model:
            if joint in dict_final[model]['All'][pop].keys():
                data = np.array(dict_final[model]['All'][pop][joint])
                mean = np.nanmean(data)
                std = np.nanstd(data)
                print(f"Model: {model}, Population: {pop}, Joint: {joint}, Mean: {mean:.4f}, Std: {std:.4f}")
            else:
                print(f"Joint {joint} not found for Model: {model}, Population: {pop}")

# Save all the value in a xlsx
import pandas as pd
data_to_save = []
for joint in list_joint:
    for pop in list_pop:
        for model in list_model:
            if joint in dict_final[model]['All'][pop].keys():
                data = np.array(dict_final[model]['All'][pop][joint])
                mean = np.nanmean(data)
                std = np.nanstd(data)
                data_to_save.append({
                    'Joint': joint,
                    'Population': pop,
                    'Model': model,
                    'Mean': mean*1000,  # Convert to mm
                    'Std': std*1000  # Convert to mm
                })
for pop in list_pop:
    for model in list_model:
          # lets concatenate the data
        data = np.concatenate([dict_final[model]['All'][pop]['EJC'],
                                dict_final[model]['All'][pop]['HMJC']
                                ,dict_final[model]['All'][pop]['WJC']])
        mean = np.nanmean(data)
        std = np.nanstd(data)
        print(f"Model: {model}, Population: {pop}, Mean of EJC, HMJC, WJC: {mean:.4f}, Std: {std:.4f}")
        data_to_save.append({
                    'Joint': 'EJC_HMJC_WJC',
                    'Population': pop,
                    'Model': model,
                    'Mean': mean*1000,
                    'Std': std*1000
                })

df = pd.DataFrame(data_to_save)
df.to_excel(folder_data / "mean_std_population.xlsx", index=False)
