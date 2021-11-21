from process_data import average
from process_data.drawning import make_plot

# Choose plot params

input_file = 'model_data/ns_structed_after_rans/ns_structed_after_rans.csv'
out_f = 'model_data/ns_structed_after_rans/ns_structed_after_rans_average_data_to_2d_matplotlib.tsv'
z_label = [2, 10, 30, 50]
z_ = [z_label[i] * 1e-3 for i in range(len(z_label))]
mean = False
rms = False
MODEL = False
ave = False

if mean:
    _type = 'Mean'
    LES_mean = True
    EXP_mean = True
    LIMITS_MEAN = True
    LES_rms = False
    EXP_rms = False
    LIMITS_RMS = False
elif rms:
    _type = 'Rms'
    LES_rms = True
    EXP_rms = True
    LIMITS_RMS = True
    LES_mean = False
    EXP_mean = False
    LIMITS_MEAN = False
else:
    _type = None
    LES_rms = True
    EXP_rms = False
    LIMITS_RMS = False
    LES_mean = True
    EXP_mean = False
    LIMITS_MEAN = False


if __name__ == '__main__':
    if ave:
        x, y, z, u, v, w, uu, vv, ww, uv, vw, uw = average.download_data_from_pw(input_file)
        output_file = average.save(input_file, average.count_averages(x, y, z, u, v, w, uu, vv, ww, uv, vw, uw))
    else:
        output_file = out_f
    for i in range(len(z_)):
        FIG_NAME = f'{_type}_z=' + str(z_label[i])
        w_exp = 'exp_data/cSwB1_ns_z' + str(z_label[i]) + '_W_MeanAndRMS.txt'
        uv_exp = 'exp_data/cSwB1_ns_z' + str(z_label[i]) + '_UV_MeanAndRMS.txt'
        zz = z_[i]
        make_plot.write_points_and_made_plot(make_plot.fill_array(output_file, w_exp, uv_exp, zz), LES_mean,
                                             EXP_mean, LES_rms, EXP_rms, MODEL, LIMITS_MEAN, LIMITS_RMS, FIG_NAME)
