import pandas as pd

def get_initial_data(url):
    initial_data = pd.read_csv(url,
                      encoding='ISO-8859-1',
                      names= {'raw_data': 0})
    
    return initial_data


def get_heads(initial_data):
    equal_filter = initial_data['raw_data'].str.contains('=+')
    rows_with_equal_signs = initial_data['raw_data'][equal_filter]
    position_of_equal_signs = rows_with_equal_signs.index[0]
    heads = initial_data.iloc[:position_of_equal_signs]['raw_data'].str.replace(r'\s+', ' ', regex=True)
    heads = heads.str.strip()
        
    name_university = pd.Series([heads[0]])
    type_exam_and_place = pd.Series([heads[1]])
    third_row = pd.Series([heads[2]])
    fourth_row = pd.Series([None])
    
    if heads.shape[0] == 4:        
        fourth_row = pd.Series([heads[3]])
        
    return name_university[0], type_exam_and_place[0], third_row[0], fourth_row[0]

def remove_extra_spaces(initial_data):
    filter_rows = ( initial_data
                   ['raw_data']
                   .map(lambda row: row.startswith(' 0'))
                   )

    without_extra_spaces = ( initial_data
                            .loc[filter_rows]
                            .reset_index()
                            .drop('index', axis=1)
                            ['raw_data']
                            .str.replace(r'\s+', ' ', regex=True)
                            .str.strip()
                            )
    
    return without_extra_spaces

def get_full_name(without_extra_spaces):
    full_name = ( without_extra_spaces
                  .str.extract(r'(\s\D+[0]?\D+[0]?\s-?\d)')
                  [0]
                  .str.replace(r'\s-?\d$', '', regex=True)
                  )
  
    return full_name

def get_grades(without_extra_spaces):
    grades = ( without_extra_spaces
               .str.extractall(r'(-?\d+\.\d+)')
               .unstack()
               )

    grades.columns = grades.columns.droplevel(0)
    grades.columns = grades.columns.rename(name=None)

    return grades[[0, 1, 2]]

def get_school_and_details(without_extra_spaces):
    school_and_details = ( without_extra_spaces
                          .str.extract(r'(\.\d+\s[A-Z].*)')
                          [0]
                          .str.replace(r'\.\d+\s', '', regex=True)
                           )
  
    return school_and_details

def get_details(school_and_details):
    details = ( school_and_details
               .str.extract(r'(INGRESA|NO\sINGRESA|ING\.\s?2.*|AUSENTE.*|ANULADO.*|^SI\s|^NO\s|\sSI$|\sNO$)')
               [0]
               )
  
    return details

def get_school(school_and_details):
    school = ( school_and_details
            .str.replace(r'INGRESA.*|NO\sINGRESA.*|ING\.\s?2.*|AUSENTE.*|ANULADO.*|^SI\s|^NO\s|\sSI$|\sNO$', '', regex=True)
              )
  
    return school

def join_data(full_name, grades, school, details, name_university, type_exam_and_place, third_row, fourth_row):
    joined_data = pd.concat(
        [full_name, grades, school, details]
        ,axis = 'columns'
        ,sort=False
    )

    joined_data.columns = ['nombres', 'result_1', 'result_2', 'total', 'escuela', 'observacion']

    joined_data['universidad'] = name_university
    joined_data['tipo_y_lugar'] = type_exam_and_place
    joined_data['third_row'] = third_row
    joined_data['fourth_row'] = fourth_row
    
    return joined_data

def transform_data(initial_data):
    name_university, type_exam_and_place, third_row, fourth_row = get_heads(initial_data)
    without_extra_spaces = remove_extra_spaces(initial_data)
    full_name = get_full_name(without_extra_spaces)
    grades = get_grades(without_extra_spaces)
    school_and_details = get_school_and_details(without_extra_spaces)
    details = get_details(school_and_details)
    school = get_school(school_and_details)
    
    joined_data = join_data(full_name, grades, school, details, name_university, type_exam_and_place, third_row, fourth_row)

    return joined_data

def join_all_data(data_url):

    results = []
    
    for url in data_url.values():
        initial_data = get_initial_data(url)
        result = transform_data(initial_data)
        results.append(result)

    final_results = pd.concat(results, axis=0, sort=False)

    return final_results.reset_index().loc[:, "nombres":]


data_url = {
    'url_1': 'https://unitru.edu.pe/webfiles///Convocatoria/2023/9//87_DOC_CONVO_300920230853.txt',
    'url_2': 'https://unitru.edu.pe/webfiles///Convocatoria/2023/9//87_DOC_CONVO_300920230847.txt',
    'url_3': 'https://unitru.edu.pe/webfiles///Convocatoria/2023/9//87_DOC_CONVO_240920230959.txt',
    'url_4': 'https://unitru.edu.pe/webfiles///Convocatoria/2023/9//87_DOC_CONVO_240920230904.txt',
    'url_5': 'https://unitru.edu.pe/webfiles///Convocatoria/2023/9//87_DOC_CONVO_230920231114.txt',
    'url_6': 'https://unitru.edu.pe/webfiles///Convocatoria/2023/9//87_DOC_CONVO_230920231112.txt',
    'url_7': 'https://unitru.edu.pe/webfiles///Convocatoria/2023/9//84_DOC_CONVO_030920230618.txt',
    'url_8': 'https://unitru.edu.pe/webfiles///Convocatoria/2023/9//84_DOC_CONVO_030920230617.txt',
    'url_9': 'https://unitru.edu.pe/webfiles///Convocatoria/2023/8//77_DOC_CONVO_210820231242.txt',
    'url_10': 'https://unitru.edu.pe/webfiles///Convocatoria/2023/8//77_DOC_CONVO_210820231240.txt',
    'url_11': 'https://unitru.edu.pe/webfiles///Convocatoria/2023/8//77_DOC_CONVO_200820231146.txt',
    'url_12': 'https://unitru.edu.pe/webfiles///Convocatoria/2023/3//73_DOC_CONVO_260320230625.txt',
    'url_13': 'https://unitru.edu.pe/webfiles///Convocatoria/2023/3//73_DOC_CONVO_260320230621.txt',
    'url_14': 'https://unitru.edu.pe/webfiles///Convocatoria/2023/3//73_DOC_CONVO_260320230619.txt',
    'url_15': 'https://unitru.edu.pe/webfiles///Convocatoria/2023/3//73_DOC_CONVO_260320230551.txt',
    'url_16': 'https://unitru.edu.pe/webfiles///Convocatoria/2023/3//73_DOC_CONVO_250320230733.txt',
    'url_17': 'https://unitru.edu.pe/webfiles///Convocatoria/2023/3//73_DOC_CONVO_250320230635.txt',
    'url_18': 'https://unitru.edu.pe/webfiles///Convocatoria/2023/3//73_DOC_CONVO_250320230631.txt',
    'url_19': 'https://unitru.edu.pe/webfiles///Convocatoria/2023/3//73_DOC_CONVO_240320230541.txt',
    'url_20': 'https://unitru.edu.pe/webfiles///Convocatoria/2023/3//73_DOC_CONVO_240320230533.txt',
    'url_21': 'https://unitru.edu.pe/webfiles///Convocatoria/2023/3//73_DOC_CONVO_240320230530.txt',
    'url_22': 'https://unitru.edu.pe/webfiles///Convocatoria/2023/3//71_DOC_CONVO_120320230547.txt',
    'url_23': 'https://unitru.edu.pe/webfiles///Convocatoria/2023/3//71_DOC_CONVO_120320230543.txt',
    'url_24': 'https://unitru.edu.pe/webfiles///Convocatoria/2023/3//71_DOC_CONVO_120320230541.txt',
    'url_25': 'https://unitru.edu.pe/webfiles///Convocatoria/2023/3//71_DOC_CONVO_110320230628.txt',
    'url_26': 'https://unitru.edu.pe/webfiles///Convocatoria/2023/3//71_DOC_CONVO_110320230602.txt',
    'url_27': 'https://unitru.edu.pe/webfiles///Convocatoria/2023/3//71_DOC_CONVO_110320230545.txt',
    'url_28': 'https://unitru.edu.pe/webfiles///Convocatoria/2023/3//71_DOC_CONVO_100320230549.txt',
    'url_29': 'https://unitru.edu.pe/webfiles///Convocatoria/2023/3//71_DOC_CONVO_100320230547.txt',
    'url_30': 'https://unitru.edu.pe/webfiles///Convocatoria/2023/3//71_DOC_CONVO_100320230544.txt',
    'url_31': 'https://unitru.edu.pe/webfiles///Convocatoria/2023/2//69_DOC_CONVO_110220230639.txt',
    'url_32': 'https://unitru.edu.pe/webfiles///Convocatoria/2023/2//69_DOC_CONVO_110220230638.txt',
    'url_33': 'https://unitru.edu.pe/webfiles///Convocatoria/2023/2//69_DOC_CONVO_110220230636.txt',
    'url_34': 'https://unitru.edu.pe/webfiles///Convocatoria/2023/2//69_DOC_CONVO_110220230635.txt',
    'url_35': 'https://unitru.edu.pe/webfiles///Convocatoria/2023/2//69_DOC_CONVO_110220230633.txt',
    'url_36': 'https://unitru.edu.pe/webfiles///Convocatoria/2023/2//69_DOC_CONVO_110220230631.txt',
    'url_37': 'https://unitru.edu.pe/webfiles///Convocatoria/2022/10//63_DOC_CONVO_231020220538.txt',
    'url_38': 'https://unitru.edu.pe/webfiles///Convocatoria/2022/10//63_DOC_CONVO_231020220535.txt',
    'url_39': 'https://unitru.edu.pe/webfiles///Convocatoria/2022/10//63_DOC_CONVO_221020221049.txt',
    'url_40': 'https://unitru.edu.pe/webfiles///Convocatoria/2022/10//63_DOC_CONVO_221020221033.txt',
    'url_41': 'https://unitru.edu.pe/webfiles///Convocatoria/2022/10//63_DOC_CONVO_211020220748.txt',
    'url_42': 'https://unitru.edu.pe/webfiles///Convocatoria/2022/10//63_DOC_CONVO_211020220740.txt',
    'url_43': 'https://unitru.edu.pe/webfiles///Convocatoria/2022/9//60_DOC_CONVO_170920220744.txt',
    'url_44': 'https://unitru.edu.pe/webfiles///Convocatoria/2022/9//60_DOC_CONVO_170920220743.txt',
    'url_45': 'https://unitru.edu.pe/webfiles///Convocatoria/2022/9//60_DOC_CONVO_170920220742.txt',
    'url_46': 'https://unitru.edu.pe/webfiles///Convocatoria/2022/9//60_DOC_CONVO_170920220741.txt',
    'url_47': 'https://unitru.edu.pe/webfiles///Convocatoria/2022/9//60_DOC_CONVO_170920220740.txt',
    'url_48': 'https://unitru.edu.pe/webfiles///Convocatoria/2022/9//60_DOC_CONVO_170920220739.txt',
    'url_49': 'https://unitru.edu.pe/webfiles///Convocatoria/2022/9//60_DOC_CONVO_150920220615.txt',
    'url_50': 'https://unitru.edu.pe/webfiles///Convocatoria/2022/9//60_DOC_CONVO_150920220614.txt',
    'url_51': 'https://unitru.edu.pe/webfiles///Convocatoria/2022/9//60_DOC_CONVO_150920220613.txt',
    'url_52': 'https://unitru.edu.pe/webfiles///Convocatoria/2022/9//59_DOC_CONVO_100920220547.txt',
    'url_53': 'https://unitru.edu.pe/webfiles///Convocatoria/2022/9//59_DOC_CONVO_100920220545.txt',
    'url_54': 'https://unitru.edu.pe/webfiles///Convocatoria/2022/4//49_DOC_CONVO_090420220633.txt',
    'url_55': 'https://unitru.edu.pe/webfiles///Convocatoria/2022/4//49_DOC_CONVO_090420220632.txt',
    'url_56': 'https://unitru.edu.pe/webfiles///Convocatoria/2022/4//49_DOC_CONVO_090420220631.txt',
    'url_57': 'https://unitru.edu.pe/webfiles///Convocatoria/2022/4//49_DOC_CONVO_090420221146.txt',
    'url_58': 'https://unitru.edu.pe/webfiles///Convocatoria/2022/4//49_DOC_CONVO_090420221144.txt',
    'url_59': 'https://unitru.edu.pe/webfiles///Convocatoria/2022/4//49_DOC_CONVO_080420220646.txt',
    'url_60': 'https://unitru.edu.pe/webfiles///Convocatoria/2022/4//49_DOC_CONVO_080420220645.txt',
    'url_61': 'https://unitru.edu.pe/webfiles///Convocatoria/2022/4//49_DOC_CONVO_070420220646.txt',
    'url_62': 'https://unitru.edu.pe/webfiles///Convocatoria/2022/4//49_DOC_CONVO_070420220645.txt',
    'url_63': 'https://unitru.edu.pe/webfiles///Convocatoria/2022/4//49_DOC_CONVO_070420220644.txt',
    'url_64': 'https://unitru.edu.pe/webfiles///Convocatoria/2022/3//45_DOC_CONVO_190320220534.txt',
    'url_65': 'https://unitru.edu.pe/webfiles///Convocatoria/2022/3//45_DOC_CONVO_190320220533.txt',
    'url_66': 'https://unitru.edu.pe/webfiles///Convocatoria/2022/3//45_DOC_CONVO_190320220528.txt',
    'url_67': 'https://unitru.edu.pe/webfiles///Convocatoria/2022/3//45_DOC_CONVO_180320220608.txt',
    'url_68': 'https://unitru.edu.pe/webfiles///Convocatoria/2022/3//45_DOC_CONVO_180320220607.txt',
    'url_69': 'https://unitru.edu.pe/webfiles///Convocatoria/2022/3//45_DOC_CONVO_180320220606.txt',
    'url_70': 'https://unitru.edu.pe/webfiles///Convocatoria/2022/3//45_DOC_CONVO_170320220639.txt',
    'url_71': 'https://unitru.edu.pe/webfiles///Convocatoria/2022/3//45_DOC_CONVO_170320220638.txt',
    'url_72': 'https://unitru.edu.pe/webfiles///Convocatoria/2022/3//45_DOC_CONVO_170320220605.txt',
    'url_73': 'https://unitru.edu.pe/webfiles///Convocatoria/2022/3//44_DOC_CONVO_110320221248.txt',
    'url_74': 'https://unitru.edu.pe/webfiles///Convocatoria/2022/3//44_DOC_CONVO_110320221247.txt',
    'url_75': 'https://unitru.edu.pe/webfiles///Convocatoria/2022/3//44_DOC_CONVO_110320221246.txt',
    'url_76': 'https://unitru.edu.pe/webfiles///Convocatoria/2022/3//44_DOC_CONVO_110320221245.txt',
    'url_77': 'https://unitru.edu.pe/webfiles///Convocatoria/2022/3//44_DOC_CONVO_110320221242.txt',
    'url_78': 'https://unitru.edu.pe/webfiles///Convocatoria/2022/3//44_DOC_CONVO_110320221241.txt',
    'url_79': 'https://unitru.edu.pe/webfiles///Convocatoria/2021/10//35_DOC_CONVO_30102021063012.txt',
    'url_80': 'https://unitru.edu.pe/webfiles///Convocatoria/2021/10//35_DOC_CONVO_30102021062954.txt',
    'url_81': 'https://unitru.edu.pe/webfiles///Convocatoria/2021/10//35_DOC_CONVO_29102021062634.txt',
    'url_82': 'https://unitru.edu.pe/webfiles///Convocatoria/2021/10//35_DOC_CONVO_29102021062612.txt',
    'url_83': 'https://unitru.edu.pe/webfiles///Convocatoria/2021/10//35_DOC_CONVO_28102021064154.txt',
    'url_84': 'https://unitru.edu.pe/webfiles///Convocatoria/2021/10//35_DOC_CONVO_28102021064136.txt',
    'url_85': 'https://unitru.edu.pe/webfiles///Convocatoria/2021/10//32_DOC_CONVO_09102021053558.txt',
    'url_86': 'https://unitru.edu.pe/webfiles///Convocatoria/2021/10//32_DOC_CONVO_09102021053540.txt',
    'url_87': 'https://unitru.edu.pe/webfiles///Convocatoria/2021/10//32_DOC_CONVO_09102021053521.txt',
    'url_88': 'https://unitru.edu.pe/webfiles///Convocatoria/2021/10//32_DOC_CONVO_08102021062503.txt',
    'url_89': 'https://unitru.edu.pe/webfiles///Convocatoria/2021/10//32_DOC_CONVO_08102021062444.txt',
    'url_90': 'https://unitru.edu.pe/webfiles///Convocatoria/2021/10//32_DOC_CONVO_08102021062424.txt',
    'url_91': 'https://unitru.edu.pe/webfiles///Convocatoria/2021/10//32_DOC_CONVO_08102021052833.txt',
    'url_92': 'https://unitru.edu.pe/webfiles///Convocatoria/2021/10//32_DOC_CONVO_08102021052814.txt',
    'url_93': 'https://unitru.edu.pe/webfiles///Convocatoria/2021/10//32_DOC_CONVO_08102021052753.txt',
    'url_94': 'https://unitru.edu.pe/webfiles///Convocatoria/2021/9//30_DOC_CONVO_18092021052838.txt',
    'url_95': 'https://unitru.edu.pe/webfiles///Convocatoria/2021/6//22_DOC_CONVO_02062021062732.txt',
    'url_96': 'https://unitru.edu.pe/webfiles///Convocatoria/2021/6//22_DOC_CONVO_02062021062712.txt',
    'url_97': 'https://unitru.edu.pe/webfiles///Convocatoria/2021/6//22_DOC_CONVO_02062021062656.txt',
    'url_98': 'https://unitru.edu.pe/webfiles///Convocatoria/2021/5//22_DOC_CONVO_29052021062643.txt',
    'url_99': 'https://unitru.edu.pe/webfiles///Convocatoria/2021/5//22_DOC_CONVO_29052021062624.txt',
    'url_100': 'https://unitru.edu.pe/webfiles///Convocatoria/2021/5//22_DOC_CONVO_29052021062556.txt',
    'url_101': 'https://unitru.edu.pe/webfiles///Convocatoria/2021/5//22_DOC_CONVO_28052021072407.txt',
    'url_102': 'https://unitru.edu.pe/webfiles///Convocatoria/2021/5//22_DOC_CONVO_28052021072346.txt',
    'url_103': 'https://unitru.edu.pe/webfiles///Convocatoria/2021/5//22_DOC_CONVO_28052021072325.txt',
    'url_104': 'https://unitru.edu.pe/webfiles///Convocatoria/2021/5//22_DOC_CONVO_28052021072259.txt',
    'url_105': 'https://unitru.edu.pe/webfiles///Convocatoria/2021/5//20_DOC_CONVO_15052021053207.txt',
    'url_106': 'https://unitru.edu.pe/webfiles///Convocatoria/2021/5//20_DOC_CONVO_15052021053149.txt',
    'url_107': 'https://unitru.edu.pe/webfiles///Convocatoria/2021/5//20_DOC_CONVO_15052021053128.txt',
    'url_108': 'https://unitru.edu.pe/webfiles///Convocatoria/2021/5//20_DOC_CONVO_14052021052008.txt',
    'url_109': 'https://unitru.edu.pe/webfiles///Convocatoria/2021/5//20_DOC_CONVO_14052021051951.txt',
    'url_110': 'https://unitru.edu.pe/webfiles///Convocatoria/2021/5//20_DOC_CONVO_14052021051931.txt',
    'url_111': 'https://unitru.edu.pe/webfiles///Convocatoria/2021/5//20_DOC_CONVO_13052021054510.txt',
    'url_112': 'https://unitru.edu.pe/webfiles///Convocatoria/2021/5//20_DOC_CONVO_13052021054456.txt',
    'url_113': 'https://unitru.edu.pe/webfiles///Convocatoria/2021/5//20_DOC_CONVO_13052021054440.txt',
    'url_114': 'https://unitru.edu.pe/webfiles///Convocatoria/2021/5//19_DOC_CONVO_12052021064957.txt',
    'url_115': 'https://unitru.edu.pe/webfiles///Convocatoria/2021/5//19_DOC_CONVO_12052021064938.txt',
    'url_116': 'https://unitru.edu.pe/webfiles///Convocatoria/2021/5//19_DOC_CONVO_12052021064918.txt',
    'url_117': 'https://unitru.edu.pe/webfiles///Convocatoria/2021/5//19_DOC_CONVO_12052021064857.txt',
    'url_118': 'https://unitru.edu.pe/webfiles///Convocatoria/2021/5//19_DOC_CONVO_12052021063943.txt',
    'url_119': 'https://unitru.edu.pe/webfiles///Convocatoria/2020/12//11_DOC_CONVO_051220200124.txt',
    'url_120': 'https://unitru.edu.pe/webfiles///Convocatoria/2020/12//11_DOC_CONVO_051220200122.txt',
    'url_121': 'https://unitru.edu.pe/webfiles///Convocatoria/2020/12//10_DOC_CONVO_041220200336.txt',
    'url_122': 'https://unitru.edu.pe/webfiles///Convocatoria/2020/12//10_DOC_CONVO_041220200237.txt',
    'url_123': 'https://unitru.edu.pe/webfiles///Convocatoria/2020/12//9_DOC_CONVO_031220200233.txt',
    'url_124': 'https://unitru.edu.pe/webfiles///Convocatoria/2020/12//9_DOC_CONVO_031220200232.txt',
    'url_125': 'https://unitru.edu.pe/webfiles///Convocatoria/2020/12//8_DOC_CONVO_021220200232.txt',
    'url_126': 'https://unitru.edu.pe/webfiles///Convocatoria/2020/12//8_DOC_CONVO_021220200231.txt',
    'url_127': 'https://unitru.edu.pe/webfiles///Convocatoria/2020/11//7_DOC_CONVO_301120200950.txt',
    'url_128': 'https://unitru.edu.pe/webfiles///Convocatoria/2020/11//6_DOC_CONVO_301120201018.txt',
    'url_129': 'https://unitru.edu.pe/webfiles///Convocatoria/2020/11//6_DOC_CONVO_301120201017.txt',
    'url_130': 'https://unitru.edu.pe/webfiles///Convocatoria/2020/11//6_DOC_CONVO_301120201016.txt',
    }