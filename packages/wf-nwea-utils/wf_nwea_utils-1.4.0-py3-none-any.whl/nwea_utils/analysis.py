import wf_core_data.utils
import pandas as pd
import numpy as np
# import scipy.stats
import inflection
import collections
import itertools
import copy
import os
import logging

logger = logging.getLogger(__name__)

TIME_FRAME_ID_VARIABLES = [
    'school_year',
    'term'
]

STUDENT_ID_VARIABLES = [
    'legal_entity',
    'student_id_nwea'
]

STUDENT_INFO_VARIABLES = [
    'first_name',
    'last_name'
]

STUDENT_ASSIGNMENT_VARIABLES = [
    'school',
    'teacher_last_first',
    'classroom',
    'grade'
]

ASSESSMENT_ID_VARIABLES = [
    'subject',
    'course'
]

RESULTS_VARIABLES = [
    'test_date',
    'rit_score',
    'rit_score_sem',
    'percentile',
    'percentile_se'
]

TERMS = (
    'Fall',
    'Winter',
    'Spring'
)

ASSESSMENTS = collections.OrderedDict((
    ('Language Arts', [
        'Reading',
        'Reading (Spanish)',
        'Language Usage'
    ]),
    ('Mathematics', [
        'Math K-12'
    ])
))

SUBJECTS = list(ASSESSMENTS.keys())

COURSES=list(itertools.chain(*ASSESSMENTS.values()))

DEFAULT_MIN_GROWTH_DAYS = 120
DEFAULT_SCHOOL_YEAR_DURATION_MONTHS = 9

def fetch_results_local_directory(
    path,
    file_extensions=['.csv', '.CSV']
):
    if not os.path.exists(path):
        raise ValueError('Path \'{}\' not found'.format(path))
    if not os.path.isdir(path):
        raise ValueError('Object at \'{}\' is not a directory'.format(path))
    paths = list()
    for directory_entry in os.listdir(path):
        file_path = os.path.join(
            path,
            directory_entry
        )
        if not os.path.isfile(file_path):
            continue
        file_extension = os.path.splitext(os.path.normpath(file_path))[1]
        if file_extension not in file_extensions:
            continue
        paths.append(file_path)
    if len(paths) == 0:
        raise ValueError('No files of type {} found in directory'.format(file_extensions))
    results = fetch_results_local_files(paths)
    return results

def fetch_results_local_files(
    paths
):
    results_list = list()
    for path in paths:
        results_file = fetch_results_local_file(
            path=path
        )
        results_list.append(results_file)
    results = pd.concat(results_list)
    return results

def fetch_results_local_file(
    path
):
    if not os.path.exists(path):
        raise ValueError('File \'{}\' not found'.format(path))
    if not os.path.isfile(path):
        raise ValueError('Object at \'{}\' is not a file'.format(path))
    results = pd.read_csv(
        path,
        dtype='object'
    )
    return results

def parse_results(results):
    test_events = extract_test_events(results)
    student_info, student_info_changes = extract_student_info(results)
    student_assignments = extract_student_assignments(results)
    return test_events, student_info, student_info_changes, student_assignments

def extract_test_events(
    results
):
    test_events = (
        results
        .rename(columns={
            'TermTested': 'term_school_year',
            'DistrictName': 'legal_entity',
            'Subject': 'subject',
            'Course': 'course',
            'StudentID': 'student_id_nwea',
            'TestDate': 'test_date',
            'StartRIT': 'rit_score',
            'StartRITSEM': 'rit_score_sem',
            'StartPercentile': 'percentile',
            'StartPercentileSE': 'percentile_se'
        })
    )
    test_events['term'] = test_events['term_school_year'].apply(lambda x: x.split(' ')[0])
    test_events['school_year'] = test_events['term_school_year'].apply(lambda x: x.split(' ')[1])
    test_events['term'] = pd.Categorical(
        test_events['term'],
        categories=TERMS,
        ordered=True
    )
    test_events['subject'] = pd.Categorical(
        test_events['subject'],
        categories=SUBJECTS,
        ordered=True
    )
    test_events['course'] = pd.Categorical(
        test_events['course'],
        categories=COURSES,
        ordered=True
    )
    test_events['test_date'] = test_events['test_date'].apply(wf_core_data.utils.to_date)
    test_events['rit_score'] = pd.to_numeric(test_events['rit_score']).astype('float')
    test_events['rit_score_sem'] = pd.to_numeric(test_events['rit_score_sem']).astype('float')
    test_events['percentile'] = pd.to_numeric(test_events['percentile']).astype('float')
    test_events['percentile_se'] = pd.to_numeric(test_events['percentile_se'].replace('<1', 0.5)).astype('float')
    test_events = test_events.reindex(columns=list(itertools.chain(
        TIME_FRAME_ID_VARIABLES,
        ASSESSMENT_ID_VARIABLES,
        STUDENT_ID_VARIABLES,
        RESULTS_VARIABLES
    )))
    test_events = (
        test_events
        .drop_duplicates()
        .set_index(list(itertools.chain(
                TIME_FRAME_ID_VARIABLES,
                ASSESSMENT_ID_VARIABLES,
                STUDENT_ID_VARIABLES
        )))
        .sort_index()
    )
    return test_events

def extract_student_info(
    results
):
    student_info = (
        results
        .rename(columns= {
            'TermTested': 'term_school_year',
            'DistrictName': 'legal_entity',
            'StudentID': 'student_id_nwea',
            'StudentLastName': 'last_name',
            'StudentFirstName': 'first_name'
        })
    )
    student_info['term'] = student_info['term_school_year'].apply(lambda x: x.split(' ')[0])
    student_info['school_year'] = student_info['term_school_year'].apply(lambda x: x.split(' ')[1])
    student_info = (
        student_info
        .reindex(columns=list(itertools.chain(
            STUDENT_ID_VARIABLES,
            TIME_FRAME_ID_VARIABLES,
            STUDENT_INFO_VARIABLES
        )))
        .drop_duplicates()
    )
    student_info_changes = (
        student_info
        .groupby(STUDENT_ID_VARIABLES)
        .filter(lambda group: len(group.drop_duplicates(subset=STUDENT_INFO_VARIABLES)) > 1)
    )
    student_info = (
        student_info
        .sort_values(TIME_FRAME_ID_VARIABLES)
        .drop(columns=TIME_FRAME_ID_VARIABLES)
        .groupby(STUDENT_ID_VARIABLES)
        .tail(1)
        .set_index(STUDENT_ID_VARIABLES)
        .sort_index()
    )
    return student_info, student_info_changes

def extract_student_assignments(
    results
):
    student_assignments = (
        results
        .rename(columns= {
            'TermTested': 'term_school_year',
            'DistrictName': 'legal_entity',
            'StudentID': 'student_id_nwea',
            'SchoolName': 'school',
            'Teacher': 'teacher_last_first',
            'ClassName': 'classroom',
            'StudentGrade': 'grade'
        })
    )
    student_assignments['term'] = student_assignments['term_school_year'].apply(lambda x: x.split(' ')[0])
    student_assignments['school_year'] = student_assignments['term_school_year'].apply(lambda x: x.split(' ')[1])
    student_assignments = (
        student_assignments
        .reindex(columns=list(itertools.chain(
            STUDENT_ID_VARIABLES,
            TIME_FRAME_ID_VARIABLES,
            STUDENT_ASSIGNMENT_VARIABLES
        )))
        .drop_duplicates()
        .set_index(list(itertools.chain(
            STUDENT_ID_VARIABLES,
            TIME_FRAME_ID_VARIABLES
        )))
        .sort_index()
    )
    return student_assignments

def summarize_by_test(
    test_events,
    student_assignments,
    grouping_variables = [
        'school_year',
        'legal_entity',
        'school',
        'classroom',
        'subject',
        'course',
        'term'
    ],
    filter_dict=None,
    select_dict=None
):
    tests = (
        test_events
        .join(
            student_assignments,
            how='left',
            on=[
                'legal_entity',
                'student_id_nwea',
                'school_year',
                'term'
            ]
        )
        .groupby(grouping_variables)
        .agg(
            num_test_events=('test_date', 'count'),
            num_valid_rit_score=('rit_score', 'count'),
            num_valid_percentile=('percentile', 'count')
        )
    )
    tests = tests.loc[tests['num_test_events'] > 0].copy()
    if filter_dict is not None:
        tests = wf_core_data.utils.filter_dataframe(
            dataframe=tests,
            filter_dict=filter_dict
        )
    if select_dict is not None:
        tests = wf_core_data.utils.select_from_dataframe(
            dataframe=tests,
            select_dict=select_dict
        )
    return tests

def summarize_by_student(
    test_events,
    student_info,
    student_assignments,
    new_time_index=['school_year'],
    min_growth_days=DEFAULT_MIN_GROWTH_DAYS,
    school_year_duration_months=DEFAULT_SCHOOL_YEAR_DURATION_MONTHS,
    filter_dict=None,
    select_dict=None
):
    new_index_variables = list(itertools.chain(
        new_time_index,
        ASSESSMENT_ID_VARIABLES,
        STUDENT_ID_VARIABLES
    ))
    unstack_variables = copy.deepcopy(TIME_FRAME_ID_VARIABLES)
    for new_time_index_variable in new_time_index:
        unstack_variables.remove(new_time_index_variable)
    students = (
        test_events
        .unstack(unstack_variables)
    )
    students.columns = ['_'.join([inflection.underscore(variable_name) for variable_name in x]) for x in students.columns]
    underlying_data_columns = list(students.columns)
    rit_scores = (
        test_events
        .dropna(subset=['rit_score'])
        .sort_values('test_date')
        .groupby(new_index_variables)
        .agg(
            rit_score_starting_date=('test_date', lambda x: x.dropna().iloc[0]),
            rit_score_ending_date=('test_date', lambda x: x.dropna().iloc[-1]),
            starting_rit_score=('rit_score', lambda x: x.dropna().iloc[0]),
            starting_rit_score_sem=('rit_score_sem', lambda x: x.dropna().iloc[0]),
            ending_rit_score=('rit_score', lambda x: x.dropna().iloc[-1]),
            ending_rit_score_sem=('rit_score_sem', lambda x: x.dropna().iloc[-1])
        )
    )
    percentiles = (
        test_events
        .dropna(subset=['percentile'])
        .sort_values('test_date')
        .groupby(new_index_variables)
        .agg(
            percentile_starting_date=('test_date', lambda x: x.dropna().iloc[0]),
            percentile_ending_date=('test_date', lambda x: x.dropna().iloc[-1]),
            starting_percentile=('percentile', lambda x: x.dropna().iloc[0]),
            starting_percentile_se=('percentile_se', lambda x: x.dropna().iloc[0]),
            ending_percentile=('percentile', lambda x: x.dropna().iloc[-1]),
            ending_percentile_se=('percentile_se', lambda x: x.dropna().iloc[-1])
        )
    )
    students = (
        students
        .join(
            rit_scores,
            how='left'
        )
        .join(
            percentiles,
            how='left'
        )
    )
    students['rit_score_num_days'] = (
        np.subtract(
            students['rit_score_ending_date'],
            students['rit_score_starting_date']
        )
        .apply(lambda x: x.days)
    )
    students['rit_score_growth'] = np.subtract(
        students['ending_rit_score'],
        students['starting_rit_score']
    )
    students.loc[students['rit_score_num_days'] < min_growth_days, 'rit_score_growth'] = np.nan
    students['rit_score_growth_per_school_year'] = students.apply(
        lambda row: wf_core_data.utils.calculate_score_growth_per_school_year(
            score_growth=row['rit_score_growth'],
            days_between_tests=row['rit_score_num_days'],
            min_growth_days=min_growth_days,
            school_year_duration_months=school_year_duration_months
        ),
        axis=1
    )
    students['percentile_num_days'] = (
        np.subtract(
            students['percentile_ending_date'],
            students['percentile_starting_date']
        )
        .apply(lambda x: x.days)
    )
    students['percentile_growth'] = np.subtract(
        students['ending_percentile'],
        students['starting_percentile']
    )
    students.loc[students['percentile_num_days'] < min_growth_days, 'percentile_growth'] = np.nan
    students['percentile_growth_per_school_year'] = students.apply(
        lambda row: wf_core_data.utils.calculate_percentile_growth_per_school_year(
            starting_percentile=row['starting_percentile'],
            ending_percentile=row['ending_percentile'],
            days_between_tests=row['rit_score_num_days'],
            min_growth_days=min_growth_days,
            school_year_duration_months=school_year_duration_months
        ),
        axis=1
    )
    students['percentile_growth_per_school_year_linear_scaling'] = students.apply(
        lambda row: wf_core_data.utils.calculate_score_growth_per_school_year(
            score_growth=row['percentile_growth'],
            days_between_tests=row['percentile_num_days'],
            min_growth_days=min_growth_days,
            school_year_duration_months=school_year_duration_months
        ),
        axis=1
    )
    students = students.join(
        student_info,
        how='left',
        on=['legal_entity', 'student_id_nwea']
    )
    latest_student_assignments = (
        student_assignments
        .reset_index()
        .sort_values(['school_year', 'term'])
        .groupby(list(itertools.chain(
            STUDENT_ID_VARIABLES,
            new_time_index
        )))
        .tail(1)
        .set_index(list(itertools.chain(
            STUDENT_ID_VARIABLES,
            new_time_index
        )))
    )
    students = students.join(
        latest_student_assignments,
        how='left',
        on=latest_student_assignments.index.names
    )
    students = students.reindex(columns=list(itertools.chain(
        STUDENT_INFO_VARIABLES,
        STUDENT_ASSIGNMENT_VARIABLES,
        underlying_data_columns,
        [
            'rit_score_starting_date',
            'rit_score_ending_date',
            'rit_score_num_days',
            'starting_rit_score',
            'starting_rit_score_sem',
            'ending_rit_score',
            'ending_rit_score_sem',
            'rit_score_growth',
            'rit_score_growth_per_school_year',
            'percentile_starting_date',
            'percentile_ending_date',
            'percentile_num_days',
            'starting_percentile',
            'starting_percentile_se',
            'ending_percentile',
            'ending_percentile_se',
            'percentile_growth',
            'percentile_growth_per_school_year',
            'percentile_growth_per_school_year_linear_scaling'
        ]
    )))
    if filter_dict is not None:
        students = wf_core_data.utils.filter_dataframe(
            dataframe=students,
            filter_dict=filter_dict
        )
    if select_dict is not None:
        students = wf_core_data.utils.select_from_dataframe(
            dataframe=students,
            select_dict=select_dict
        )
    return students

def summarize_by_group(
    students,
    grouping_variables=[
        'school_year',
        'legal_entity',
        'subject',
        'course'
    ],
    filter_dict=None,
    select_dict=None
):
    groups = (
        students
        .reset_index()
        .groupby(grouping_variables)
        .agg(
            num_test_results=('student_id_nwea', 'count'),
            num_valid_starting_rit_score=('starting_rit_score', 'count'),
            mean_starting_rit_score=('starting_rit_score', 'mean'),
            starting_rit_score_sd=('starting_rit_score', 'std'),
            num_valid_ending_rit_score=('ending_rit_score', 'count'),
            mean_ending_rit_score=('ending_rit_score', 'mean'),
            ending_rit_score_sd=('ending_rit_score', 'std'),
            num_valid_rit_score_growth=('rit_score_growth', 'count'),
            mean_rit_score_growth=('rit_score_growth', 'mean'),
            rit_score_growth_sd=('rit_score_growth', 'std'),
            mean_rit_score_growth_per_school_year=('rit_score_growth_per_school_year', 'mean'),
            rit_score_growth_per_school_year_sd=('rit_score_growth_per_school_year', 'std'),
            num_valid_starting_percentile=('starting_percentile', 'count'),
            mean_starting_percentile=('starting_percentile', 'mean'),
            starting_percentile_sd=('starting_percentile', 'std'),
            num_valid_ending_percentile=('ending_percentile', 'count'),
            mean_ending_percentile=('ending_percentile', 'mean'),
            ending_percentile_sd=('ending_percentile', 'std'),
            num_valid_percentile_growth=('percentile_growth', 'count'),
            mean_percentile_growth=('percentile_growth', 'mean'),
            percentile_growth_sd=('percentile_growth', 'std'),
            mean_percentile_growth_per_school_year=('percentile_growth_per_school_year', 'mean'),
            percentile_growth_per_school_year_sd=('percentile_growth_per_school_year', 'std'),
            mean_percentile_growth_per_school_year_linear_scaling=('percentile_growth_per_school_year_linear_scaling', 'mean'),
            percentile_growth_per_school_year_linear_scaling_sd=('percentile_growth_per_school_year_linear_scaling', 'std'),
        )
        .dropna(how='all')
    )
    groups = groups.loc[groups['num_test_results'] > 0].copy()
    groups['mean_starting_rit_score_sem'] = np.divide(
        groups['starting_rit_score_sd'],
        np.sqrt(groups['num_valid_starting_rit_score'])
    )
    groups['mean_ending_rit_score_sem'] = np.divide(
        groups['ending_rit_score_sd'],
        np.sqrt(groups['num_valid_ending_rit_score'])
    )
    groups['mean_rit_score_growth_sem'] = np.divide(
        groups['rit_score_growth_sd'],
        np.sqrt(groups['num_valid_rit_score_growth'])
    )
    groups['mean_rit_score_growth_per_school_year_sem'] = np.divide(
        groups['rit_score_growth_per_school_year_sd'],
        np.sqrt(groups['num_valid_rit_score_growth'])
    )
    groups['mean_starting_percentile_sem'] = np.divide(
        groups['starting_percentile_sd'],
        np.sqrt(groups['num_valid_starting_percentile'])
    )
    groups['mean_ending_percentile_sem'] = np.divide(
        groups['ending_percentile_sd'],
        np.sqrt(groups['num_valid_ending_percentile'])
    )
    groups['mean_percentile_growth_sem'] = np.divide(
        groups['percentile_growth_sd'],
        np.sqrt(groups['num_valid_percentile_growth'])
    )
    groups['mean_percentile_growth_per_school_year_sem'] = np.divide(
        groups['percentile_growth_per_school_year_sd'],
        np.sqrt(groups['num_valid_percentile_growth'])
    )
    groups['mean_percentile_growth_per_school_year_linear_scaling_sem'] = np.divide(
        groups['percentile_growth_per_school_year_linear_scaling_sd'],
        np.sqrt(groups['num_valid_percentile_growth'])
    )
    groups = groups.reindex(columns=[
        'num_test_results',
        'num_valid_starting_rit_score',
        'mean_starting_rit_score',
        'starting_rit_score_sd',
        'mean_starting_rit_score_sem',
        'num_valid_ending_rit_score',
        'mean_ending_rit_score',
        'ending_rit_score_sd',
        'mean_ending_rit_score_sem',
        'num_valid_rit_score_growth',
        'mean_rit_score_growth',
        'rit_score_growth_sd',
        'mean_rit_score_growth_sem',
        'mean_rit_score_growth_per_school_year',
        'rit_score_growth_per_school_year_sd',
        'mean_rit_score_growth_per_school_year_sem',
        'num_valid_starting_percentile',
        'mean_starting_percentile',
        'starting_percentile_sd',
        'mean_starting_percentile_sem',
        'num_valid_ending_percentile',
        'mean_ending_percentile',
        'ending_percentile_sd',
        'mean_ending_percentile_sem',
        'num_valid_percentile_growth',
        'mean_percentile_growth',
        'percentile_growth_sd',
        'mean_percentile_growth_sem',
        'mean_percentile_growth_per_school_year',
        'percentile_growth_per_school_year_sd',
        'mean_percentile_growth_per_school_year_sem',
        'mean_percentile_growth_per_school_year_linear_scaling',
        'percentile_growth_per_school_year_linear_scaling_sd',
        'mean_percentile_growth_per_school_year_linear_scaling_sem'
    ])
    if filter_dict is not None:
        groups = wf_core_data.utils.filter_dataframe(
            dataframe=groups,
            filter_dict=filter_dict
        )
    if select_dict is not None:
        groups = wf_core_data.utils.select_from_dataframe(
            dataframe=groups,
            select_dict=select_dict
        )
    return groups

def format_group_summary(
    groups,
    index_names=None
):
    groups_formatted = groups.copy()
    groups_formatted['ending_rit_score_error_range'] = groups_formatted.apply(
        lambda row: '{:.1f} \u2013 {:.1f}'.format(
            row['mean_ending_rit_score'] - row ['mean_ending_rit_score_sem'],
            row['mean_ending_rit_score'] + row ['mean_ending_rit_score_sem'],
        ) if pd.notna(row['mean_ending_rit_score_sem']) else '',
        axis=1
    )
    groups_formatted['ending_percentile_error_range'] = groups_formatted.apply(
        lambda row: '{:.1f} \u2013 {:.1f}'.format(
            row['mean_ending_percentile'] - row ['mean_ending_percentile_sem'],
            row['mean_ending_percentile'] + row ['mean_ending_percentile_sem'],
        ) if pd.notna(row['mean_ending_percentile_sem']) else '',
        axis=1
    )
    groups_formatted['rit_score_growth_per_school_year_error_range'] = groups_formatted.apply(
        lambda row: '{:+.1f} \u2013 {:+.1f}'.format(
            row['mean_rit_score_growth_per_school_year'] - row ['mean_rit_score_growth_per_school_year_sem'],
            row['mean_rit_score_growth_per_school_year'] + row ['mean_rit_score_growth_per_school_year_sem']
        ) if pd.notna(row['mean_rit_score_growth_per_school_year_sem']) else '',
        axis=1
    )
    groups_formatted['percentile_growth_per_school_year_error_range'] = groups_formatted.apply(
        lambda row: '{:+.1f} \u2013 {:+.1f}'.format(
            row['mean_percentile_growth_per_school_year'] - row ['mean_percentile_growth_per_school_year_sem'],
            row['mean_percentile_growth_per_school_year'] + row ['mean_percentile_growth_per_school_year_sem']
        ) if pd.notna(row['mean_percentile_growth_per_school_year_sem']) else '',
        axis=1
    )
    groups_formatted['mean_ending_rit_score'] = (
        groups_formatted['mean_ending_rit_score']
        .apply(lambda x: '{:.1f}'.format(x))
    )
    groups_formatted['mean_ending_rit_score_sem'] = (
        groups_formatted['mean_ending_rit_score_sem']
        .apply(lambda x: '{:.1f}'.format(x) if pd.notna(x) else '')
    )
    groups_formatted['mean_ending_percentile'] = (
        groups_formatted['mean_ending_percentile']
        .apply(lambda x: '{:.1f}'.format(x))
    )
    groups_formatted['mean_ending_percentile_sem'] = (
        groups_formatted['mean_ending_percentile_sem']
        .apply(lambda x: '{:.1f}'.format(x) if pd.notna(x) else '')
    )
    groups_formatted['mean_rit_score_growth_per_school_year'] = (
        groups_formatted['mean_rit_score_growth_per_school_year']
        .apply(lambda x: '{:+.1f}'.format(x) if pd.notna(x) else '')
    )
    groups_formatted['mean_rit_score_growth_per_school_year_sem'] = (
        groups_formatted['mean_rit_score_growth_per_school_year_sem']
        .apply(lambda x: '{:.1f}'.format(x) if pd.notna(x) else '')
    )
    groups_formatted['mean_percentile_growth_per_school_year'] = (
        groups_formatted['mean_percentile_growth_per_school_year']
        .apply(lambda x: '{:+.1f}'.format(x) if pd.notna(x) else '')
    )
    groups_formatted['mean_percentile_growth_per_school_year_sem'] = (
        groups_formatted['mean_percentile_growth_per_school_year_sem']
        .apply(lambda x: '{:.1f}'.format(x) if pd.notna(x) else '')
    )
    groups_formatted = (
        groups_formatted
        .reindex(columns=[
            'num_valid_ending_rit_score',
            'mean_ending_rit_score',
            'mean_ending_rit_score_sem',
            'ending_rit_score_error_range',
            'num_valid_ending_percentile',
            'mean_ending_percentile',
            'mean_ending_percentile_sem',
            'ending_percentile_error_range',
            'num_valid_rit_score_growth',
            'mean_rit_score_growth_per_school_year',
            'mean_rit_score_growth_per_school_year_sem',
            'rit_score_growth_per_school_year_error_range',
            'num_valid_percentile_growth',
            'mean_percentile_growth_per_school_year',
            'mean_percentile_growth_per_school_year_sem',
            'percentile_growth_per_school_year_error_range'
        ])
    )
    groups_formatted.columns = pd.MultiIndex.from_product([
        ['Attainment', 'Growth per year'],
        ['Raw score', 'Percentile'],
        ['N', 'Avg', 'SEM', 'Error range']
    ])
    if index_names is not None:
        groups_formatted.index.names=index_names
    return groups_formatted


def format_student_summary(
    students
):
    students_formatted = students.copy()
    students_formatted['rit_score_num_days'] = (
        students_formatted['rit_score_num_days']
        .apply(lambda x: '{:.0f}'.format(x) if pd.notna(x) else '')
    )
    students_formatted['starting_rit_score'] = (
        students_formatted['starting_rit_score']
        .apply(lambda x: '{:.0f}'.format(x) if pd.notna(x) else '')
    )
    students_formatted['ending_rit_score'] = (
        students_formatted['ending_rit_score']
        .apply(lambda x: '{:.0f}'.format(x) if pd.notna(x) else '')
    )
    students_formatted['rit_score_growth'] = (
        students_formatted['rit_score_growth']
        .apply(lambda x: '{:.0f}'.format(x) if pd.notna(x) else '')
    )
    students_formatted['rit_score_growth_per_school_year'] = (
        students_formatted['rit_score_growth_per_school_year']
        .apply(lambda x: '{:.1f}'.format(x) if pd.notna(x) else '')
    )
    students_formatted['percentile_num_days'] = (
        students_formatted['percentile_num_days']
        .apply(lambda x: '{:.0f}'.format(x) if pd.notna(x) else '')
    )
    students_formatted['starting_percentile'] = (
        students_formatted['starting_percentile']
        .apply(lambda x: '{:.0f}'.format(x) if pd.notna(x) else '')
    )
    students_formatted['ending_percentile'] = (
        students_formatted['ending_percentile']
        .apply(lambda x: '{:.0f}'.format(x) if pd.notna(x) else '')
    )
    students_formatted['percentile_growth'] = (
        students_formatted['percentile_growth']
        .apply(lambda x: '{:.0f}'.format(x) if pd.notna(x) else '')
    )
    students_formatted['percentile_growth_per_school_year'] = (
        students_formatted['percentile_growth_per_school_year']
        .apply(lambda x: '{:.1f}'.format(x) if pd.notna(x) else '')
    )
    students_formatted = (
        students_formatted
        .reset_index()
        .reindex(columns=[
            'subject',
            'course',
            'legal_entity',
            'school',
            'classroom',
            'teacher_last_first',
            'student_id_nwea',
            'first_name',
            'last_name',
            'grade',
            'rit_score_starting_date',
            'rit_score_ending_date',
            'rit_score_num_days',
            'starting_rit_score',
            'ending_rit_score',
            'rit_score_growth',
            'rit_score_growth_per_school_year',
            'percentile_starting_date',
            'percentile_ending_date',
            'percentile_num_days',
            'starting_percentile',
            'ending_percentile',
            'percentile_growth',
            'percentile_growth_per_school_year'
        ])
        .sort_values([
            'subject',
            'course',
            'legal_entity',
            'school',
            'classroom',
            'teacher_last_first',
            'last_name',
        ])
        .rename(columns={
            'subject': 'Subject',
            'course': 'Course',
            'legal_entity': 'Legal entity',
            'school': 'School',
            'classroom': 'Classroom',
            'teacher_last_first': 'Teacher',
            'student_id_nwea': 'Student ID',
            'first_name': 'First name',
            'last_name': 'Last name',
            'grade': 'Grade',
            'rit_score_starting_date': 'RIT score starting date',
            'rit_score_ending_date': 'RIT score ending date',
            'rit_score_num_days': 'RIT score days between tests',
            'starting_rit_score': 'Starting RIT score',
            'ending_rit_score': 'Ending RIT score',
            'rit_score_growth': 'RIT score growth',
            'rit_score_growth_per_school_year': 'RIT score growth per school year',
            'percentile_starting_date': 'Percentile starting date',
            'percentile_ending_date': 'Percentile ending date',
            'percentile_num_days': 'Percentile days between tests',
            'starting_percentile': 'Starting percentile',
            'ending_percentile': 'Ending percentile',
            'percentile_growth': 'Percentile growth',
            'percentile_growth_per_school_year': 'Percentile growth per school year',
        })
    )
    return students_formatted
