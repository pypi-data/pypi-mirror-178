import csv
import tempfile
import os
from fitmulticell.sumstat import hexagonal_cluster_sumstat as css
import fitmulticell.util as util
from fitmulticell.sumstat import plot_sumstat as pss
import fitmulticell.sumstat.cell_types_cout as cs
import matplotlib.pyplot as plt


def create_cluster_1():
    full_path = os.path.join(tempfile.gettempdir(), "logger.csv")
    csvfile = open(full_path, 'w', newline='')
    obj = csv.writer(csvfile, delimiter='\t')
    obj.writerow(['t', 'cell.id', 'RNA_concentration', 'infection'])
    obj.writerow(['0', '1', '0.1', '1'])
    obj.writerow(['0', '2', '0.2', '0'])
    obj.writerow(['0', '3', '0.3', '1'])
    obj.writerow(['0', '4', '0.4', '1'])
    obj.writerow(['0', '5', '0.5', '1'])
    obj.writerow(['0', '6', '0.6', '0'])
    obj.writerow(['0', '7', '0.7', '0'])
    obj.writerow(['0', '8', '0.8', '0'])
    obj.writerow(['0', '9', '0.9', '0'])
    obj.writerow(['0', '10', '0.9', '0'])
    obj.writerow(['0', '11', '0.9', '1'])
    obj.writerow(['0', '12', '0.9', '1'])
    obj.writerow(['0', '13', '0.9', '1'])
    obj.writerow(['0', '14', '0.9', '0'])
    obj.writerow(['0', '15', '0.9', '0'])
    obj.writerow(['0', '16', '0.9', '0'])
    obj.writerow(['0', '17', '0.9', '0'])
    obj.writerow(['0', '18', '0.9', '0'])
    obj.writerow(['0', '19', '0.9', '1'])
    obj.writerow(['1', '1', '0.1', '1'])
    obj.writerow(['1', '2', '0.2', '1'])
    obj.writerow(['1', '3', '0.3', '1'])
    obj.writerow(['1', '4', '0.4', '1'])
    obj.writerow(['1', '5', '0.5', '1'])
    obj.writerow(['1', '6', '0.6', '1'])
    obj.writerow(['1', '7', '0.7', '0'])
    obj.writerow(['1', '8', '0.8', '0'])
    obj.writerow(['1', '9', '0.9', '0'])
    obj.writerow(['1', '10', '0.9', '0'])
    obj.writerow(['1', '11', '0.9', '1'])
    obj.writerow(['1', '12', '0.9', '0'])
    obj.writerow(['1', '13', '0.9', '1'])
    obj.writerow(['1', '14', '0.9', '0'])
    obj.writerow(['1', '15', '0.9', '0'])
    obj.writerow(['1', '16', '0.9', '0'])
    obj.writerow(['1', '17', '0.9', '0'])
    obj.writerow(['1', '18', '0.9', '0'])
    obj.writerow(['1', '19', '0.9', '1'])
    csvfile.close()
    logger_file = util.tsv_to_df("/tmp")  # noqa: S108

    return logger_file


def create_cluster_2():
    full_path = os.path.join(tempfile.gettempdir(), "logger.csv")
    csvfile = open(full_path, 'w', newline='')
    obj = csv.writer(csvfile, delimiter='\t')
    obj.writerow(['t', 'cell.id', 'RNA_concentration', 'infection'])
    obj.writerow(['0', '1', '0.1', '1'])
    obj.writerow(['0', '2', '0.2', '0'])
    obj.writerow(['0', '3', '0.3', '1'])
    obj.writerow(['0', '4', '0.4', '1'])
    obj.writerow(['0', '5', '0.5', '1'])
    obj.writerow(['0', '6', '0.6', '0'])
    obj.writerow(['0', '7', '0.7', '0'])
    obj.writerow(['0', '8', '0.8', '0'])
    obj.writerow(['0', '9', '0.9', '0'])
    obj.writerow(['0', '10', '0.9', '0'])
    obj.writerow(['0', '11', '0.9', '1'])
    obj.writerow(['0', '12', '0.9', '1'])
    obj.writerow(['0', '13', '0.9', '1'])
    obj.writerow(['0', '14', '0.9', '0'])
    obj.writerow(['0', '15', '0.9', '0'])
    obj.writerow(['0', '16', '0.9', '0'])
    obj.writerow(['0', '17', '0.9', '0'])
    obj.writerow(['0', '18', '0.9', '0'])
    obj.writerow(['0', '19', '0.9', '1'])
    csvfile.close()
    logger_file = util.tsv_to_df("/tmp")  # noqa: S108
    return logger_file


def create_cluster_3():
    full_path = os.path.join(tempfile.gettempdir(), "logger.csv")
    csvfile = open(full_path, 'w', newline='')
    obj = csv.writer(csvfile, delimiter='\t')
    obj.writerow(['t', 'cell.id', 'RNA_concentration', 'infection'])
    obj.writerow(['0', '1', '0.1', '1'])
    obj.writerow(['0', '2', '0.2', '1'])
    obj.writerow(['0', '3', '0.3', '0'])
    obj.writerow(['0', '4', '0.4', '1'])
    obj.writerow(['0', '5', '0.5', '1'])
    obj.writerow(['0', '6', '0.6', '0'])
    obj.writerow(['0', '7', '0.7', '0'])
    obj.writerow(['0', '8', '0.8', '0'])
    obj.writerow(['0', '9', '0.9', '0'])
    obj.writerow(['0', '10', '0.9', '0'])
    obj.writerow(['0', '11', '0.9', '0'])
    obj.writerow(['0', '12', '0.9', '0'])
    obj.writerow(['0', '13', '0.9', '0'])
    obj.writerow(['0', '14', '0.9', '0'])
    obj.writerow(['0', '15', '0.9', '0'])
    obj.writerow(['0', '16', '0.9', '0'])
    obj.writerow(['0', '17', '0.9', '1'])
    obj.writerow(['0', '18', '0.9', '0'])
    obj.writerow(['0', '19', '0.9', '1'])
    obj.writerow(['1', '1', '0.1', '1'])
    obj.writerow(['1', '2', '0.2', '1'])
    obj.writerow(['1', '3', '0.3', '0'])
    obj.writerow(['1', '4', '0.4', '1'])
    obj.writerow(['1', '5', '0.5', '1'])
    obj.writerow(['1', '6', '0.6', '0'])
    obj.writerow(['1', '7', '0.7', '0'])
    obj.writerow(['1', '8', '0.8', '1'])
    obj.writerow(['1', '9', '0.9', '1'])
    obj.writerow(['1', '10', '0.9', '0'])
    obj.writerow(['1', '11', '0.9', '0'])
    obj.writerow(['1', '12', '0.9', '0'])
    obj.writerow(['1', '13', '0.9', '1'])
    obj.writerow(['1', '14', '0.9', '0'])
    obj.writerow(['1', '15', '0.9', '1'])
    obj.writerow(['1', '16', '0.9', '1'])
    obj.writerow(['1', '17', '0.9', '1'])
    obj.writerow(['1', '18', '0.9', '0'])
    obj.writerow(['1', '19', '0.9', '1'])
    csvfile.close()
    logger_file = util.tsv_to_df("/tmp")  # noqa: S108
    return logger_file


def create_cluster_4():
    full_path = os.path.join(tempfile.gettempdir(), "logger.csv")
    csvfile = open(full_path, 'w', newline='')
    obj = csv.writer(csvfile, delimiter='\t')
    obj.writerow(['t', 'cell.id', 'RNA_concentration', 'cell_type'])
    obj.writerow(['0', '1', '0.1', '0'])
    obj.writerow(['0', '2', '0.2', '0'])
    obj.writerow(['0', '3', '0.3', '0'])
    obj.writerow(['1', '4', '0.4', '1'])
    obj.writerow(['1', '5', '0.5', '2'])
    obj.writerow(['1', '6', '0.6', '1'])
    obj.writerow(['2', '7', '0.7', '2'])
    obj.writerow(['2', '8', '0.8', '3'])
    obj.writerow(['2', '9', '0.9', '2'])
    csvfile.close()
    logger_file = util.tsv_to_df("/tmp")  # noqa: S108
    return logger_file


def test_cluster_count():
    logger_file = create_cluster_1()
    field_of_interest = 'infection'
    cluster_cell_types = [1]
    t_symbol = 't'
    cluster_count_result = css.get_clusters_count(logger_file,
                                                  field_of_interest,
                                                  cluster_cell_types,
                                                  time_symbol=t_symbol)
    assert cluster_count_result["cluster_count"][0] == 5
    assert cluster_count_result["cluster_count"][1] == 3


def test_cluster_size():
    logger_file = create_cluster_2()
    field_of_interest = 'infection'
    cluster_cell_types = [1]
    time_point = 0
    t_symbol = 't'
    cluster_size_result = css.get_clusters_sizes_tp(logger_file,
                                                    field_of_interest,
                                                    cluster_cell_types,
                                                    time_point,
                                                    time_symbol=t_symbol)
    assert cluster_size_result[1] == 3
    assert cluster_size_result[3] == 1


def test_active_infected_cell():
    logger_file = create_cluster_3()
    field_of_interest = 'infection'
    cluster_cell_types = [1]
    t_interval = [0, 1]
    t_symbol = 't'
    CC_Contributor_count_result = css.get_count_cc_contributors_alltp(
        logger_file, field_of_interest, cluster_cell_types,
        time_interval=t_interval, time_symbol=t_symbol)

    assert CC_Contributor_count_result["cc_contributors"][0] == 5
    assert CC_Contributor_count_result["cc_contributors"][1] == 8


def test_cell_types_count():
    logger_file = create_cluster_4()
    t_symbol = 't'
    field_of_interest = 'cell_type'
    cell_types_list = [1, 2, 3]
    cell_type_result = cs.count_cell_types(logger_file,
                                           field_of_interest,
                                           cell_types_list,
                                           time_symbol=t_symbol)
    assert cell_type_result['cell_type'][0][0] == 0
    assert cell_type_result['cell_type'][0][1] == 2
    assert cell_type_result['cell_type'][1][1] == 1
    assert cell_type_result['cell_type'][1][2] == 2


def test_cluster_cout_plot():
    """Test `fitmulticell.sumstat.plot_sumstat.
    plot_cluster_count_all_time_point`"""
    logger_file = create_cluster_1()
    field_of_interest = 'infection'
    cluster_cell_types = [1]
    t_symbol = 't'
    cluster_count_result = css.get_clusters_count(logger_file,
                                                  field_of_interest,
                                                  cluster_cell_types,
                                                  time_symbol=t_symbol)
    pss.plot_cluster_count_all_time_point(cluster_count_result,
                                          field_of_interest)
    plt.close()


def test_active_cell_plot():
    """Test `fitmulticell.sumstat.plot_sumstat.
    plot_active_cell_all_time_point`"""
    logger_file = create_cluster_1()
    field_of_interest = 'infection'
    cluster_cell_types = [1]
    t_interval = [0, 1]
    t_symbol = 't'
    CC_Contributor_count_result = css.get_count_cc_contributors_alltp(
        logger_file, field_of_interest, cluster_cell_types,
        time_interval=t_interval, time_symbol=t_symbol)
    pss.plot_active_cell_all_time_point(CC_Contributor_count_result)
    plt.close()
