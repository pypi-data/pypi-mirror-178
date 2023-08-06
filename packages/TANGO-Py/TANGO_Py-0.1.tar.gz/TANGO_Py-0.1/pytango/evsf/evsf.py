import numpy as np

def get_evsf(colocalization_data, nchannels, evf_idx =-1, nbins = 30):
    data = []
    for nuc_data in colocalization_data.values():
        plot_data, breaks, breaks_centers = compute_evsf(nuc_data[evf_idx], nbins, nuc_data[:nchannels])
        data.append(plot_data)
    data = np.stack(data) # nucleus / channel / break
    data_summary = np.stack([ np.mean(data, axis=0), np.std(data, axis=0), np.broadcast_to(data.shape[0], data.shape[1:] ) ]) # [mean, std, n] per channel per break
    return data, data_summary, breaks_centers

def compute_evsf(evf, nbins, channels):
    # sort arrays according to EVF
    indexes = evf.argsort()
    reference_array = np.ones_like(evf)[np.newaxis]
    data = np.concatenate([channels[:, indexes], reference_array], axis=0)
    evf = evf[indexes]
    # create breaks
    breaks = np.linspace(0, 1, nbins+1, True)
    breaks_idx = np.linspace(0, evf.shape[0], nbins+1).astype(np.int32) # regular breaks to have equal volume fractions
    # average channels values at duplicate EVF values
    _, rep_idx_start, rep_count = np.unique(evf, return_counts=True, return_index=True)
    for i,l in zip(rep_idx_start, rep_count):
        if l>1:
            data[:, i:i+l] = np.mean(data[:, i:i+l], axis=1, keepdims=True)
    # sum per break
    values = np.zeros(shape=(data.shape[0], nbins), dtype=np.float64)
    for i in range(nbins):
        np.sum(data[:, breaks_idx[i]:breaks_idx[i+1]], axis=1, out = values[:, i])
    values = values / np.nansum(values, axis=1, keepdims=True)
    values = np.cumsum(values, axis=1, dtype=np.float64)
    centers = (breaks[1:]+breaks[:-1])/2
    values = values - values[-1:] + centers # so that a random distribution corresponds to the first diagonal
    return values[:-1], breaks, centers # returns array of per-channel EVSF data (first axis=channel, second axis=break), breaks and break center

def get_evfs_metrics(evfs, break_centers):
    diff = evfs - break_centers
    area = np.sum(diff, axis=-1)
    max_pos = np.max(diff, axis=-1)
    max_pos[max_pos<0] = np.nan
    min_neg = np.min(diff, axis=-1)
    min_neg[min_neg>0] = np.nan
    return area, max_pos, min_neg
