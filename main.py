from process_data import average, parameters
from process_data.drawning import make_plot

input_file = 'model_data/isotherm_structed_after_rans/structed_rans.csv'
out_f = 'model_data/t_i_average_data_to_2d_matplotlib.tsv'
mean = False
rms = True
MODEL = False
ave = False

if mean:
    _type = 'u_mean'
    LES_mean = True
    EXP_mean = True
    LIMITS_MEAN = True
    LES_rms = False
    EXP_rms = False
    LIMITS_RMS = False
elif rms:
    _type = 'u_rms'
    LES_rms = True
    EXP_rms = True
    LIMITS_RMS = True
    LES_mean = False
    EXP_mean = False
    LIMITS_MEAN = False
else:
    _type = None
    LES_rms = True
    EXP_rms = True
    LIMITS_RMS = False
    LES_mean = False
    EXP_mean = False
    LIMITS_MEAN = False


if __name__ == '__main__':
    if ave:
        x, y, z, u, v, w, uu, vv, ww, uv, vw, uw = average.download_data_from_pw(input_file)
        output_file = average.save(input_file, average.count_averages(x, y, z, u, v, w, uu, vv, ww, uv, vw, uw))
    else:
        output_file = out_f
    for i in range(len(parameters.z_)):
        FIG_NAME = f'{_type}_at_z' + str(parameters.z_label[i]) + '_mm'
        w_exp = 'exp_data/cSwB1_ns_z' + str(parameters.z_label[i]) + '_W_MeanAndRMS.txt'
        uv_exp = 'exp_data/cSwB1_ns_z' + str(parameters.z_label[i]) + '_UV_MeanAndRMS.txt'
        zz = parameters.z_[i]
        make_plot.write_points_and_made_plot(make_plot.fill_array(output_file, w_exp, uv_exp, zz), LES_mean,
                                             EXP_mean, LES_rms, EXP_rms, MODEL, LIMITS_MEAN, LIMITS_RMS, FIG_NAME)
