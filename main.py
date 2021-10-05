from process_data import average
from drawning import make_plot

# Choose plot params

input_file = 'isoterm_turb_ns_r6/r6_keqn_r2_inner_finish.csv'
out_f = 'isoterm_turb_ns_r6/r6_keqn_r2_inner_finish_average_data_to_2d_matplotlib.tsv'
z_label = [2, 10, 30, 50]
z_ = [z_label[i] * 1e-3 for i in range(len(z_label))]
mean = False
rms = True
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
    LES_rms = False
    EXP_rms = False
    LIMITS_RMS = False
    LES_mean = False
    EXP_mean = True
    LIMITS_MEAN = True


if __name__ == '__main__':
    if ave:
        x, z, y, u, w, v, uu, ww, vv, uw, uv, vw = average.download_data_from_pw(input_file)
        output_file = average.save(input_file, average.count_averages(x, z, y, u, w, v, uu, ww, vv, uw, uv, vw))
    else:
        output_file = out_f
    for i in range(len(z_)):
        FIG_NAME = f'{_type}_z=' + str(z_label[i])
        w_exp = 'exp_data/cSwB1_ns_z' + str(z_label[i]) + '_W_MeanAndRMS.txt'
        uv_exp = 'exp_data/cSwB1_ns_z' + str(z_label[i]) + '_UV_MeanAndRMS.txt'
        zz = z_[i]
        make_plot.write_points_and_made_plot(make_plot.fill_array(output_file, w_exp, uv_exp, zz), LES_mean,
                                             EXP_mean, LES_rms, EXP_rms, MODEL, LIMITS_MEAN, LIMITS_RMS, FIG_NAME)
    # print('Q_initial = ', calculate_stream.calc_cylinder_stream(calculate_stream.f_initial_for_q))
    # print('Q_present = ', calculate_stream.calc_cylinder_stream(calculate_stream.f_smooth_for_q_final))
