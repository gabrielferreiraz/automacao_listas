import pandas as pd
import unicodedata
import logging
import numpy as np

# Colunas essenciais para a estrutura Assertiva
ASSERTIVA_ESSENTIAL_COLS = [
    "Razao", "Fantasia", "Logradouro", "Numero", "Bairro", "Cidade", "UF",
    "SOCIO1Nome", "SOCIO1Celular1", "SOCIO1Celular2", "CNPJ"
]

# Colunas essenciais para a estrutura Lemit
LEMIT_ESSENTIAL_COLS = [
    "CPF/CNPJ", "NOME/RAZAO_SOCIAL", "EMPRESAS_ASSOCIADAS", "Endereco", "Numero", "BAIRRO", "CIDADE", "UF",
    "DDD1", "CELULAR1", "DDD2", "CELULAR2"
]

# Ordem final das colunas de saída
FIXED_OUTPUT_ORDER = [
    "Razao", "Logradouro", "Numero", "Bairro", "Cidade", "UF",
    "SOCIO1Nome", "SOCIO1Celular1", "SOCIO1Celular2"
]

def normalize_colname(name):
    """Remove acentos, espaços e converte para minúsculas."""
    nfkd = unicodedata.normalize('NFKD', str(name))
    return ''.join([c for c in nfkd if not unicodedata.combining(c)]).replace(' ', '').lower()

def map_essential_columns(df, essential_cols):
    """Mapeia nomes de colunas normalizados para os nomes originais."""
    norm_to_orig = {normalize_colname(col): col for col in df.columns}
    found = {}
    for col in essential_cols:
        norm = normalize_colname(col)
        if norm in norm_to_orig:
            found[col] = norm_to_orig[norm]
    return found

def _clean_phone_number(number_str):
    """Limpa e valida um número de telefone, retornando NaN se inválido."""
    if pd.isna(number_str) or number_str == '':
        return np.nan
    cleaned = ''.join(filter(str.isdigit, str(number_str)))
    # Considera um número inválido se tiver menos de 8 dígitos (ex: só DDD ou número incompleto)
    if len(cleaned) < 8:
        return np.nan
    return cleaned

def identify_structure(df):
    """Identifica a estrutura do DataFrame (Assertiva ou Lemit)."""
    norm_cols = {normalize_colname(col) for col in df.columns}
    
    # Contar quantas colunas essenciais de cada tipo estão presentes
    assertiva_matches = sum(1 for col in ASSERTIVA_ESSENTIAL_COLS if normalize_colname(col) in norm_cols)
    lemit_matches = sum(1 for col in LEMIT_ESSENTIAL_COLS if normalize_colname(col) in norm_cols)

    # Decidir com base na contagem de correspondências
    if lemit_matches > assertiva_matches:
        return "Lemit"
    else:
        return "Assertiva"

def clean_and_filter_data(df, distancia_padrao="100 km"):
    if df.empty:
        logging.warning("DataFrame de entrada está vazio.")
        return df, [], "Unknown"

    structure = identify_structure(df)
    logging.info(f"Estrutura de dados identificada: {structure}")

    if structure == "Assertiva":
        essential_cols = ASSERTIVA_ESSENTIAL_COLS
        col_map = map_essential_columns(df, essential_cols)
        
        if "Razao" not in col_map and "Fantasia" in col_map:
            df.rename(columns={col_map["Fantasia"]: "Razao"}, inplace=True)
            col_map = map_essential_columns(df, essential_cols)

    elif structure == "Lemit":
        essential_cols = LEMIT_ESSENTIAL_COLS
        col_map = map_essential_columns(df, essential_cols)

        df_standard = pd.DataFrame()

        if "EMPRESAS_ASSOCIADAS" in col_map:
            df_standard["Razao"] = df[col_map["EMPRESAS_ASSOCIADAS"]].fillna('').astype(str)
        else:
            df_standard["Razao"] = ''

        if "NOME/RAZAO_SOCIAL" in col_map:
            df_standard["SOCIO1Nome"] = df[col_map["NOME/RAZAO_SOCIAL"]].fillna('').astype(str)
        else:
            df_standard["SOCIO1Nome"] = ''

        ddd1_col = col_map.get("DDD1")
        cel1_col = col_map.get("CELULAR1")
        if ddd1_col and cel1_col and ddd1_col in df.columns and cel1_col in df.columns:
            ddd1_series = pd.to_numeric(df[ddd1_col], errors='coerce').fillna(0).astype(int).astype(str)
            cel1_series = pd.to_numeric(df[cel1_col], errors='coerce').fillna(0).astype(int).astype(str)
            df_standard["SOCIO1Celular1"] = ddd1_series + cel1_series
        else:
            df_standard["SOCIO1Celular1"] = ''

        ddd2_col = col_map.get("DDD2")
        cel2_col = col_map.get("CELULAR2")
        if ddd2_col and cel2_col and ddd2_col in df.columns and cel2_col in df.columns:
            ddd2_series = pd.to_numeric(df[ddd2_col], errors='coerce').fillna(0).astype(int).astype(str)
            cel2_series = pd.to_numeric(df[cel2_col], errors='coerce').fillna(0).astype(int).astype(str)
            df_standard["SOCIO1Celular2"] = ddd2_series + cel2_series
        else:
            df_standard["SOCIO1Celular2"] = ''
            
        direct_mapping = {
            "Logradouro": "Endereco", "Bairro": "BAIRRO",
            "Cidade": "CIDADE", "UF": "UF"
        }
        for std_col, lemit_col in direct_mapping.items():
            if lemit_col in col_map:
                df_standard[std_col] = df[col_map[lemit_col]].fillna('').astype(str)
            else:
                df_standard[std_col] = ''

        # Handle 'Numero' column specifically
        numero_col = col_map.get("Numero")
        if numero_col and numero_col in df.columns:
            df_standard["Numero"] = pd.to_numeric(df[numero_col], errors='coerce').fillna(0).astype(int).astype(str)
        else:
            df_standard["Numero"] = ''

        # Handle 'CNPJ' column specifically
        cnpj_col = col_map.get("CPF/CNPJ")
        if cnpj_col and cnpj_col in df.columns:
            df_standard["CNPJ"] = pd.to_numeric(df[cnpj_col], errors='coerce').fillna(0).astype(int).astype(str)
        else:
            df_standard["CNPJ"] = ''
        
        df = df_standard
        essential_cols = ASSERTIVA_ESSENTIAL_COLS
        col_map = map_essential_columns(df, essential_cols)

    missing = [col for col in essential_cols if col not in col_map]
    for col in missing:
        logging.warning(f"Coluna essencial ausente: {col}")

    cols_to_select = [col_map[c] for c in essential_cols if c in col_map]
    df_sel = df[cols_to_select].copy()

    df_sel = df_sel.dropna(how='all', subset=cols_to_select)

    # Aplica a limpeza e validação de números de telefone
    for c in ["SOCIO1Celular1", "SOCIO1Celular2"]:
        if c in col_map:
            col = col_map[c]
            df_sel[col] = df_sel[col].apply(_clean_phone_number)

    # Remove linhas onde SOCIO1Celular1 está vazio (após a limpeza)
    if "SOCIO1Celular1" in col_map:
        df_sel = df_sel.dropna(subset=[col_map["SOCIO1Celular1"]])
        # Remove duplicatas com base no SOCIO1Celular1
        df_sel = df_sel.drop_duplicates(subset=[col_map["SOCIO1Celular1"]], keep='first')

    if "CNPJ" in col_map:
        cnpj_col = col_map["CNPJ"]
        df_sel[cnpj_col] = df_sel[cnpj_col].astype(str).str.strip()
        df_sel = df_sel.drop_duplicates(subset=[cnpj_col], keep='first')
    elif all(c in col_map for c in ["Razao", "Logradouro"]):
        df_sel = df_sel.drop_duplicates(
            subset=[col_map["Razao"], col_map["Logradouro"]], keep='first'
        )

    text_cols = [col_map[c] for c in ["Razao", "Logradouro", "Bairro", "Cidade", "UF", "SOCIO1Nome"] if c in col_map]
    for col in text_cols:
        df_sel[col] = df_sel[col].fillna('').astype(str).str.strip()
    
    df_sel['Distancia'] = distancia_padrao

    ordered_output_cols = []
    for fixed_col_name in FIXED_OUTPUT_ORDER:
        if fixed_col_name in col_map:
            ordered_output_cols.append(col_map[fixed_col_name])
        elif fixed_col_name == "SOCIO1Nome" and "SOCIO1Nome" in df_sel.columns:
             ordered_output_cols.append("SOCIO1Nome")

    df_final = df_sel[ordered_output_cols].copy()

    sort_cols = []
    if "Bairro" in col_map:
        sort_cols.append(col_map["Bairro"])
    if "Razao" in col_map:
        sort_cols.append(col_map["Razao"])

    if sort_cols:
        df_final = df_final.sort_values(by=sort_cols, ascending=True)

    return df_final.reset_index(drop=True), missing, structure
