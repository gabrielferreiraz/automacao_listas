import pandas as pd
import chardet

def read_and_detect_encoding(file_obj):
    """Lê o conteúdo de um arquivo (ou UploadedFile) e detecta seu encoding."""
    if hasattr(file_obj, 'read'): # It's an UploadedFile or similar file-like object
        raw_data = file_obj.read()
        file_obj.seek(0) # Reset stream position for subsequent reads
    else: # Assume it's a filepath string
        try:
            with open(file_obj, 'rb') as f:
                raw_data = f.read()
        except FileNotFoundError:
            return None, None

    result = chardet.detect(raw_data)
    return raw_data, result['encoding'] or 'utf-8'

def infer_delimiter(file_obj, encoding):
    """Tenta inferir o delimitador de um arquivo CSV (ou UploadedFile)."""
    try:
        if hasattr(file_obj, 'read'): # It's an UploadedFile
            sample = file_obj.read(4096).decode(encoding, errors='ignore')
            file_obj.seek(0) # Reset stream position
        else: # Assume it's a filepath string
            with open(file_obj, 'r', encoding=encoding) as f:
                sample = f.read(4096)  # Lê uma amostra do arquivo

        delimiters = [';', ',', '\t', '|']
        counts = {d: sample.count(d) for d in delimiters}
        if not any(counts.values()):
            return ',' # Retorna um padrão se nenhum delimitador for encontrado
        return max(counts, key=counts.get)
    except Exception:
        return ',' # Retorna um padrão em caso de erro

def read_csv_smart(file_obj):
    """Lê um arquivo CSV (ou UploadedFile) com detecção inteligente de encoding e delimitador."""
    raw_data, encoding = read_and_detect_encoding(file_obj)
    if raw_data is None:
        return pd.DataFrame(), f"Arquivo não encontrado ou ilegível."

    delimiter = infer_delimiter(file_obj, encoding)
    
    try:
        df = pd.read_csv(file_obj, delimiter=delimiter, encoding=encoding, on_bad_lines='warn')
        return df, None
    except Exception as e:
        # Tenta com um encoding mais robusto como fallback
        try:
            if hasattr(file_obj, 'seek'): # For UploadedFile, reset position
                file_obj.seek(0)
            df = pd.read_csv(file_obj, delimiter=delimiter, encoding='latin-1', on_bad_lines='warn')
            return df, None
        except Exception as e_fallback:
            return pd.DataFrame(), f"Erro ao ler CSV com fallback: {e_fallback}"

def read_xlsx_smart(file_obj):
    """Lê um arquivo XLSX (ou UploadedFile), tentando várias abordagens."""
    try:
        # Tentativa padrão com o engine openpyxl
        df = pd.read_excel(file_obj, engine='openpyxl')
        return df, None
    except Exception as e_openpyxl:
        # Fallback para o engine calamine se o openpyxl falhar
        try:
            if hasattr(file_obj, 'seek'): # For UploadedFile, reset position
                file_obj.seek(0)
            df = pd.read_excel(file_obj, engine='calamine')
            return df, None
        except Exception as e_calamine:
            return pd.DataFrame(), f"Erro ao ler XLSX com ambos os engines: openpyxl ({e_openpyxl}), calamine ({e_calamine})"

def load_data(file_input):
    """Carrega dados de um arquivo, seja CSV ou XLSX, e retorna um DataFrame.
    Aceita tanto filepath (string) quanto UploadedFile object.
    """
    if file_input is None:
        return pd.DataFrame(), "Nenhum arquivo fornecido."

    # Determine the file extension
    if hasattr(file_input, 'name'): # It's an UploadedFile object
        file_extension = file_input.name.lower()
    else: # Assume it's a string filepath
        file_extension = str(file_input).lower()

    if file_extension.endswith('.csv'):
        return read_csv_smart(file_input)
    elif file_extension.endswith('.xlsx'):
        return read_xlsx_smart(file_input)
    else:
        return pd.DataFrame(), "Formato de arquivo não suportado. Use CSV ou XLSX."

def save_temp_data(df):
    """Salva um DataFrame em um arquivo temporário."""
    temp_file = "temp_uploaded.csv"
    df.to_csv(temp_file, index=False)
    return temp_file

def read_temp_data():
    """Lê dados de um arquivo temporário."""
    temp_file = "temp_uploaded.csv"
    try:
        df = pd.read_csv(temp_file)
        return df, None
    except FileNotFoundError:
        return pd.DataFrame(), "Arquivo temporário não encontrado."

