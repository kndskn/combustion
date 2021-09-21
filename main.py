import average
import make_plot

# Choose plot params

model_type = 'on'
z_label = 2
z_ = z_label * 1e-3
LES_mean = False
EXP_mean = False
LES_rms = True
EXP_rms = True
MODEL = False
LIMITS = False

# Choose input data

FIG_NAME = f'Turbulent inlet {model_type} z = ' + str(z_label)
input_file = 'isoterm_turb_ns_r6/isoterm_turb_ns_r6_paraview.csv'
w_exp = 'exp_data/cSwB1_ns_z' + str(z_label) + '_W_MeanAndRMS.txt'
uv_exp = 'exp_data/cSwB1_ns_z' + str(z_label) + '_UV_MeanAndRMS.txt'
out_f = 'isoterm_turb_ns_r6/isoterm_turb_ns_r6_paraview_average_data_to_2d_matplotlib.tsv'
ave = False


if __name__ == '__main__':
    if ave:
        x, z, y, u, w, v, uu, ww, vv, uw, uv, vw = average.download_data_from_pw(input_file)
        output_file = average.save(input_file, average.count_averages(x, z, y, u, w, v, uu, ww, vv, uw, uv, vw))
    else:
        output_file = out_f
    make_plot.write_points_and_made_plot(make_plot.fill_array(output_file, w_exp, uv_exp, z_), LES_mean, EXP_mean,
                                         LES_rms, EXP_rms, MODEL, LIMITS)
    # print('Q_initial = ', calculate_stream.calc_cylinder_stream(calculate_stream.f_initial_for_q))
    # print('Q_present = ', calculate_stream.calc_cylinder_stream(calculate_stream.f_smooth_for_q_final))
