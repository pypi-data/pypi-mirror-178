from debater_python_api.api.clients.key_point_analysis.KpAnalysisUtils import KpAnalysisUtils
from debater_python_api.api.clients.key_point_analysis.utils import get_all_files_in_dir

if __name__ == '__main__':
    KpAnalysisUtils.init_logger()

    file = '/Users/yoavkantor/Library/CloudStorage/Box-Box/interview_analysis/debater_p_results/2022/software/software_results/results_all_questions/eng_kp_input_2022_simplified_multi_kps_merged_kpa_results_software_kpa_result.csv'
    KpAnalysisUtils.generate_graphs_and_textual_summary(file)

    dirs_with_stances = ['/Users/yoavkantor/Library/CloudStorage/Box-Box/interview_analysis/debater_p_results/2022/research/combined',
                         '/Users/yoavkantor/Library/CloudStorage/Box-Box/interview_analysis/debater_p_results/2022/research/standalone_questions',
                         '/Users/yoavkantor/Library/CloudStorage/Box-Box/interview_analysis/debater_p_results/2022/research/standalone_questions_full_kps_list']
    dirs_no_stances = ['/Users/yoavkantor/Library/CloudStorage/Box-Box/interview_analysis/debater_p_results/2022/research/combined/no_stance',
                       '/Users/yoavkantor/Library/CloudStorage/Box-Box/interview_analysis/debater_p_results/2022/research/standalone_questions/no_stance',
                       '/Users/yoavkantor/Library/CloudStorage/Box-Box/interview_analysis/debater_p_results/2022/research/standalone_questions_full_kps_list/no_stance']
    for dir in dirs_with_stances:
        files = get_all_files_in_dir(dir)
        files = [f for f in files if 'pos.csv' in f or 'neg.csv' in f]
        for f in files:
            KpAnalysisUtils.generate_graphs_and_textual_summary(f)

    for dir in dirs_no_stances:
        files = get_all_files_in_dir(dir)
        files = [f for f in files if 'results.csv' in f]
        for f in files:
            KpAnalysisUtils.generate_graphs_and_textual_summary(f)