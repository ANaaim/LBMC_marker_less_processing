from pathlib import Path
import snip_h5py as snipH5
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# # ── 0) load the dict with the correct nesting ─────────────────────────────
folder_data = Path("./Comparaison_2D")
dict_final   = snipH5.load_dictionary_from_hdf(folder_data/"comparaison_final_pop.h5")

# ── 1) your explicit orders ───────────────────────────────────────────────
camera_order = ["R_back","L_back","R_lat","L_lat","R_front","L_front","Up"]           # exactly the order you want
pop_order  = ["TDC","CP"]             # likewise
point_order  = ["SJC","EJC","WJC","HMJC"]  # facet order

#sns.set_context("talk", font_scale=1.1)  

point_labels = {
  "SJC": "Shoulder",
  "EJC": "Elbow",
  "WJC": "Wrist",
  "HMJC": "Hand"
}
# ── define your pop_bg_colors ────────────────────────────────────────────
pop_bg_colors = {
    "CP":"skyblue",
    "TDC":"lightcoral",
}

# pick distinct colors for each model
model_colors = {
    "all_body_hrnet_coco_dark_coco_hdf5":"C0",
    "all_body_resnet_hdf5":"C4",
    "all_body_rtm_coktail_14_hdf5":"C2",
}

# define your short labels
model_labels = {
    "all_body_hrnet_coco_dark_coco_hdf5": "HRNet",
    "all_body_resnet_hdf5":            "ResNet",
    "all_body_rtm_coktail_14_hdf5":    "RTM"
}

# ── 2) flatten into a DataFrame ──────────────────────────────────────────
records = []
for model, pop_dict in dict_final.items():
    for pop_name, cam_dict in pop_dict.items():
        for cam_group, pts_dict in cam_dict.items():
            for pt_code, arr in pts_dict.items():
                for d in arr[:, 0]:
                    records.append({
                        "model":         model,
                        "population":    pop_name,
                        "camera_group":  cam_group,
                        "point":         pt_code,
                        "distance":      d
                    })

df = pd.DataFrame(records)

# # ── 3) force categorical ordering ────────────────────────────────────────
# df["camera_group"] = pd.Categorical(
#     df["camera_group"],
#     categories=camera_order,
#     ordered=True
# )
# df["population"] = pd.Categorical(
#     df["population"],
#     categories=pop_order,
#     ordered=True
# )
# df["point"] = pd.Categorical(
#     df["point"],
#     categories=point_order,
#     ordered=True
# )

# # ── 4) build composite x-axis category ──────────────────────────────────
# df["cam_pop"] = pd.Categorical(
#     df["camera_group"].astype(str) + "_" + df["population"].astype(str),
#     categories=[f"{cg}_{pop}" for cg in camera_order for pop in pop_order],
#     ordered=True
# )


# ── 3) add the short‐name column and force ordering ───────────────────────
df["model_short"] = df["model"].map(model_labels)
df["camera_group"] = pd.Categorical(df["camera_group"], categories=camera_order, ordered=True)
df["population"]   = pd.Categorical(df["population"],   categories=pop_order,    ordered=True)
df["point"]        = pd.Categorical(df["point"],        categories=point_order,  ordered=True)
df["cam_pop"] = pd.Categorical(
    df["camera_group"].astype(str) + "_" + df["population"].astype(str),
    categories=[f"{cg}_{pop}" for cg in camera_order for pop in pop_order],
    ordered=True
)
# ── 4) build a palette for the short names ───────────────────────────────
palette_short = {model_labels[k]: v for k,v in model_colors.items() }
hue_order = list(palette_short.keys())

# ── assume you already have df, camera_order, pop_order, point_order, point_labels, pop_bg_colors

g = sns.catplot(
    data=df,
    kind="box",
    x="cam_pop",
    y="distance",
    hue="model_short",
    hue_order=hue_order,
    palette=palette_short,
    col="point",
    col_order=point_order,
    col_wrap=2,
    sharey=True,
    sharex=False,
    height=4.5,
    aspect=1.2,
    showfliers=False
)

# ── 1) Shade with your pop_bg_colors and rotate bottom ticks ─────────────
for ax in g.axes.flatten():
    xticks = ax.get_xticks()
    width  = (xticks[1] - xticks[0]) if len(xticks)>1 else 1
    for pos, lbl in zip(xticks, ax.get_xticklabels()):
        cam_pop = lbl.get_text()
        pop = cam_pop.split("_")[-1]
        #color = pop_bg_colors.get(pop, "lightgray")
        color = pop_bg_colors[pop]
        ax.axvspan(pos - width/2, pos + width/2, color=color, alpha=0.3)
    # rotate only the bottom‐row labels (we’ll hide the top anyway)
    ax.tick_params(axis="x", rotation=45)

# ── 2) Remove x‐labels (and ticks) on the top row ────────────────────────
# Because col_wrap=2, the first two axes in flattened order are the top row.
top_row = g.axes.flatten()[:2]
for ax in top_row:
    ax.set_xlabel("")               # removes the “Camera group – Population” label
    ax.tick_params(labelbottom=False)  # hides the tick labels

# ── 3) Give nice facet titles and legend title ──────────────────────────
for ax in g.axes.flatten():
    short = ax.get_title().split(" = ")[-1]
    ax.set_title(point_labels.get(short, short), fontsize=18)

for ax in g.axes.flatten():
    ax.tick_params(axis="y", labelsize=14)  


g.set_axis_labels("", "2D difference with  \n reference (px)", fontsize=16)

# set all y-axes to run from 0 up to, say, 200 pixels
g.set(ylim=(0, 50))
# remove the seaborn facet‐grid legend
g._legend.remove()
#g._legend.set_title("Model")

# g.set_xlabels(g.ax.get_xlabel(), fontsize=18)
# g.set_ylabels(g.ax.get_ylabel(), fontsize=18)

plt.tight_layout()
plt.show()


