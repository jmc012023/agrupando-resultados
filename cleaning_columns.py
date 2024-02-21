def transform_tipo_y_lugar_column(final_result):
    cleaned_tipo_y_lugar = (
        final_result['tipo_y_lugar']
        .str.replace(r'.+EXAMEN(ES)?\s', '', regex=True)
        .str.replace(r'DE\sADMISION\s|SUMATIVOS\s', '', regex=True)
        .str.replace(r"\sPag.+", ' ', regex=True)
        .str.strip()
        .str.replace(r"\s\*\s", "|", regex=True)
        .str.replace(r"CEPUNT\s", "CEPUNT_", regex=True)
        .str.replace(r'-\s', '/', regex=True)
        .str.replace(r'\s/', ' ', regex=True)
        .str.replace(r"/|_", '-', regex=True)
        .str.replace("V A L L E", "VALLE", regex=False)
        .str.replace("|", " ", regex=False)
        .str.replace("STGO.DE CHUCO", "STGO_DE_CHUCO", regex=False)
    )

    periodo = (
        cleaned_tipo_y_lugar
        .str.extract(r'(\d+-I+)')
    )

    tipo_exam = (
        cleaned_tipo_y_lugar
        .str.extract(r'(ORDINARIO|CEPUNT|EXTRAORDINARIO)')        
    )

    sede = (
        cleaned_tipo_y_lugar
        .str.extract(r'(TRUJILLO|VALLE|JEQUETEPEQUE|HUAMACHUCO|STGO_DE_CHUCO)')        
    )

    return periodo[0], tipo_exam[0], sede[0]

def transform__third_column(final_result):
    cleaned_third_column = (
        final_result['third_row']
        .str.replace('* AREA P.A.D.* ', '', regex=False)
        .str.replace('* UNIDAD P.A.D.* ', '', regex=False)
        .str.replace(r"RESULTADOS\sGENERALES\sPOR\sESCUELA\sPROFESIONAL\s-?\s?|RELACION\sDE\sINGRESANTES\sPOR\sESCUELA\sPROFESIONAL\s", '', regex=True)
        .str.replace(r"<<\s|\s>>|Modalidad\s:\s", "", regex=True)
        .str.replace("QUINTO GRADO DE EDUCACION SECUNDARIA ", "QUINTO_GRADO ", regex=False)
        .str.replace("VICTIMAS DE LA VIOLENCIA ", "VICTIMAS_VIOLENCIA ")
        .str.replace("DEPORTISTAS CALIFICADOS", "DEPORTISTAS_CALIFICADOS")
        .str.replace(r'\d+/\d+/\d+', '', regex=True)
        .str.strip()
        .str.replace("AREAS", "AREA", regex=False)
        .str.replace(r'\s\*\s|\s:\s', ' ', regex=True)
        .str.replace("AREA", "", regex=False)
        .str.replace(r"\s", "", regex=True)
        .str.replace(r"^-", "", regex=True)
    )

    tipo_postulante = (
        cleaned_third_column
        .str.extract(r'(QUINTO_GRADO|DISCAPACITADOS|VICTIMAS_VIOLENCIA|DEPORTISTAS_CALIFICADOS)')
    )

    sede = (
        cleaned_third_column
        .str.extract(r'(TRUJILLO|VALLE|HUAMACHUCO)')
    )

    area = (
        cleaned_third_column
        .str.replace(r'QUINTO_GRADO|DISCAPACITADOS|VICTIMAS_VIOLENCIA|DEPORTISTAS_CALIFICADOS|TRUJILLO|VALLE|HUAMACHUCO', '', regex=True)
    )

    return tipo_postulante[0], sede[0], area


def transform_fourth_column(final_result):
    return (
        final_result['fourth_row']
        .str.split("AREA", expand=True)[1]
        .str.strip()
        .str.replace("S ", "", regex=False)
        .str.replace("* ", "", regex=False)
        .str.replace("- ", "", regex=False)
        .str.replace(" ", "-", regex=False)
    )

def transform_4_last_columns(final_result):
    periodo, tipo_exam, sede_1 = transform_tipo_y_lugar_column(final_result)
    tipo_postulante, sede_2, area_1 = transform__third_column(final_result)
    area_2 = transform_fourth_column(final_result)
    
    sede = sede_1.str.cat(sede_2, na_rep="")
    area = area_1.str.cat(area_2, na_rep="")

    summary = final_result.drop(['tipo_y_lugar', 'third_row', 'fourth_row'], axis=1)
    
    summary['periodo'] = periodo
    summary['tipo_exam'] = tipo_exam
    summary['tipo_postulante'] = tipo_postulante
    summary['sede'] = sede
    summary['area'] = area

    return summary

def cleaning_summary(summary):
    summary['nombres'] = summary['nombres'].str.strip()
    summary['escuela'] = summary['escuela'].str.strip().str.upper()
    summary['observacion'] = (
        summary['observacion']
        .str.strip()
        .str.replace('NO INGRESA', 'NO', regex=False)
        .str.replace('NO', 'NO INGRESA', regex=False)
        .str.replace('SI', 'INGRESA', regex=False)
        )
    summary['universidad'] = summary['universidad'].str.strip()
    summary['periodo'] = summary['periodo'].str.strip()
    summary['tipo_exam'] = summary['tipo_exam'].str.strip()
    summary['tipo_postulante'] = summary['tipo_postulante'].str.strip()
    summary['sede'] = summary['sede'].str.strip()
    summary['area'] = summary['area'].str.strip()

    return summary