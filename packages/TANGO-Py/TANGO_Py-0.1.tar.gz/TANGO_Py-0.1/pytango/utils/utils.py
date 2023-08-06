import h5py

def open_colocalization_data_h5(path, selection, ds_name, position):
    with h5py.File(path) as coloc_file:
        ds_dir = f"{selection}/{ds_name}/{position}/ColocalizationData"
        all_nuc = [f for f in coloc_file[ds_dir].keys() if f.startswith('0-')]
        return {name:coloc_file[f"{ds_dir}/{name}"][0] for name in all_nuc}
