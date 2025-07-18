# Documentação do Projeto: Automação de Listas

Este documento serve como um guia detalhado para o projeto "Automação de Listas", descrevendo seu propósito, estrutura, funcionalidades e o histórico de desenvolvimento, incluindo os desafios e soluções implementadas.

## 1. Visão Geral do Projeto

O projeto "Automação de Listas" é uma aplicação Streamlit desenvolvida para automatizar o processamento e a distribuição de listas de leads. Ele oferece três funcionalidades principais: a higienização de dados de clientes (original do projeto), a divisão de grandes listas de leads em arquivos menores, formatados em Excel e PDF, distribuídos por consultores e datas, e a nova funcionalidade de geração de arquivos de negócios para robôs.

## 2. Estrutura Atual do Projeto

O projeto está organizado da seguinte forma:

```
/home/gabriel/Downloads/automacao_de_lista_python/
├───create_pdf.py             # Módulo para criação de PDFs (usado pela aba de Higienização)
├───data_cleaning.py          # Módulo para limpeza e filtragem de dados
├───data_ingestion.py         # Módulo para ingestão inteligente de dados (CSV)
├───report_generator.py       # **Arquivo principal da aplicação Streamlit**
├───temp_uploaded.csv         # Arquivo temporário para upload de CSV (usado pela aba de Higienização)
├───temp_uploaded.xlsx        # Arquivo temporário para upload de XLSX (usado pela aba de Divisor de Listas)
├───__pycache__/              # Cache de módulos Python
├───.venv/                    # Ambiente virtual Python
├───Relatorios/               # Diretório de saída para os arquivos gerados (PDFs e XLSX)
├───fonts/                    # Diretório para armazenar arquivos de fontes TTF (ex: Noto Sans)
│   ├───NotoSans-Bold.ttf     # Fonte Noto Sans Bold (necessária para PDFs)
│   └───NotoSans-Regular.ttf  # Fonte Noto Sans Regular (necessária para PDFs)
└───.streamlit/               # Configurações do Streamlit
    └───config.toml           # Configurações para desativar o prompt de e-mail do Streamlit
```

## 3. Aplicação Streamlit (`report_generator.py`)

O `report_generator.py` é o coração da aplicação, orquestrando as diferentes funcionalidades através de um sistema de abas.

### 3.1. Aba "Higienização de Dados"

Esta aba é a funcionalidade original do projeto.

*   **Propósito:** Permite ao usuário fazer upload de um arquivo CSV contendo dados de clientes. O sistema então higieniza e filtra esses dados, exibindo uma pré-visualização.
*   **Processamento:** Utiliza `data_ingestion.py` para ler o CSV de forma inteligente (inferindo delimitador e codificação) e `data_cleaning.py` para limpar e padronizar as informações.
*   **Exportação:** Oferece opções para exportar os dados higienizados para:
    *   **PDF:** Utiliza a função `create_pdf` (do módulo `create_pdf.py`) para gerar um relatório em PDF.
    *   **Excel (XLSX):** Exporta os dados para um arquivo Excel simples.

### 3.2. Aba "Divisor de Listas"

Esta é a nova funcionalidade implementada.

*   **Propósito:** Permite ao usuário fazer upload de um arquivo XLSX grande contendo leads. O sistema divide essa lista em lotes de 50 leads, atribuindo-os sequencialmente a uma lista predefinida de consultores, e gera um par de arquivos (Excel e PDF) para cada lote.
*   **Lista de Consultores:** A lista de consultores é definida internamente no `report_generator.py` (`CONSULTORES`).
*   **Lógica de Distribuição:**
    *   A lista de leads é processada em ciclos. Em cada ciclo, cada consultor recebe um lote de 50 leads.
    *   Após todos os consultores receberem seus lotes, a data de referência avança para o próximo dia útil (pulando sábados e domingos).
    *   Este ciclo se repete até que todos os leads da lista original sejam distribuídos.
*   **Geração de Arquivos:**
    *   **Excel (XLSX):** Cada lote de 50 leads é salvo em um arquivo XLSX.
        *   **Formatação:** As planilhas Excel possuem um cabeçalho mesclado (`Leads Automoveis - {Nome_Consultor} {DD}/{MM}`), cores de linha alternadas (azul claro e branco) e bordas pretas finas em todas as células com conteúdo. As larguras das colunas são ajustadas automaticamente.
    *   **PDF:** Para cada arquivo Excel gerado, um PDF correspondente é criado.
        *   **Formatação:** Os PDFs replicam o estilo visual do Excel, incluindo o título, cores alternadas e larguras de coluna adaptadas para os campos de leads.
        *   **Fontes:** Utiliza a família de fontes Noto Sans (Regular e Bold) para garantir a compatibilidade com caracteres Unicode, evitando problemas de codificação.
*   **Download:** Todos os arquivos Excel e PDF gerados são compactados em um único arquivo ZIP, que o usuário pode baixar.

### 3.3. Aba "Automação Pessoas Agendor"

*   **Propósito:** Gera arquivos Excel no formato "Pessoas" para importação no Agendor CRM, distribuindo leads entre consultores.
*   **Entrada:** Arquivo XLSX com leads.
*   **Configurações:** Permite definir cargo padrão, descrição, UF padrão e um nicho para o nome do arquivo.
*   **Mapeamento de Colunas:** Tenta mapear automaticamente colunas como 'NOME', 'Whats', 'CEL', 'Rua', 'Número', 'Bairro', 'Cidade' com base em sugestões e nomes de colunas existentes.
*   **Lógica de Distribuição:** Similar à aba "Divisor de Listas", distribui leads em lotes para consultores selecionados, gerando um arquivo Excel "Pessoas" para cada lote/consultor.
*   **Nome do Arquivo:** O formato do nome do arquivo é `PESSOAS_{NICHO}_{LOCALIDADE}_{CONSULTOR}_{DATA}.xlsx`.
*   **Saída:** Arquivos Excel "Pessoas" (individualmente ou em ZIP se múltiplos).

### 3.4. Aba "Gerador de Negócios para Robôs" (NOVA FUNCIONALIDADE)

*   **Propósito:** Gerar arquivos Excel no formato "Negócios" para importação em sistemas de robôs, utilizando os leads já processados e distribuídos nos arquivos "Pessoas Agendor".
*   **Entrada:** Os arquivos Excel de "Pessoas Agendor" gerados pela aba "Automação Pessoas Agendor".
*   **Configuração do Usuário:**
    *   **Número de Negócios por Consultor:** O usuário definirá quantos leads (negócios) cada arquivo de negócio deve conter.
    *   **Data de Início:** O usuário definirá a data de início para a primeira planilha de negócios. As datas subsequentes serão incrementadas automaticamente, pulando finais de semana.
    *   **Nicho:** O usuário fornecerá o nicho (ex: AUTO, MED, ADV) que será usado na formatação do "Título do negócio".
*   **Colunas da Planilha de Negócios:**
    *   `Título do negócio`: Formato `MM/YY - RB - NICHO - NOME_PESSOA/ESPs`
    *   `Empresa relacionada`: Será deixada em branco.
    *   `Pessoa relacionada`: Preenchido com o `Nome` do lead do arquivo de Pessoas.
    *   `Usuário responsável`: Preenchido com o `Usuário responsável` do lead do arquivo de Pessoas.
    *   `Data de início`: Data definida pelo usuário, incrementada para arquivos subsequentes.
    *   `Data de conclusão`: Preenchido temporariamente com o número de WhatsApp do lead (como texto).
    *   `Valor Total`: Será deixada em branco.
    *   `Funil`: "Funil de Vendas" (valor fixo)
    *   `Etapa`: "Prospecção" (valor fixo)
    *   `Status`: "Em andamento" (valor fixo)
    *   `Motivo de perda`: Será deixada em branco.
    *   `Descrição do motivo de perda`: Será deixada em branco.
    *   `Ranking`: Será deixada em branco.
    *   `Descrição`: Será deixada em branco.
    *   `Produtos e Serviços`: Será deixada em branco.
*   **Processamento:**
    *   O script lerá os leads de cada arquivo "Pessoas Agendor" (um por consultor).
    *   Dividirá os leads em lotes com base no "Número de Negócios por Consultor" especificado.
    *   Para cada lote, um novo arquivo Excel de "Negócios" será gerado.
*   **Lógica de Data:**
    *   A coluna de data nos arquivos de "Negócios" será preenchida automaticamente.
    *   Para cada arquivo de negócio gerado para o *mesmo consultor*, a data será incrementada, pulando sábados e domingos.
*   **Saída:** Os arquivos Excel de "Negócios" gerados serão salvos na mesma pasta do arquivo de "Pessoas Agendor" correspondente.

## 4. Funções Chave e Módulos

*   **`report_generator.py`:**
    *   `CONSULTORES`: Lista de strings com os nomes dos consultores.
    *   `proximo_dia_util(data_atual)`: Calcula o próximo dia útil.
    *   `formatar_planilha(writer, df)`: Aplica formatação visual a uma planilha Excel (bordas, cores, auto-largura).
    *   `gerar_excel_em_memoria(df_lote, consultor, data)`: Gera um arquivo Excel em memória com o lote de leads e aplica a formatação.
    *   `criar_pdf_leads(df, titulo)`: Gera um arquivo PDF em memória com o lote de leads, aplicando formatação e usando fontes UTF-8.
    *   `aba_higienizacao()`: Função que encapsula a lógica da primeira aba do Streamlit.
    *   `aba_divisor_listas()`: Função que encapsula a lógica da segunda aba do Streamlit.
    *   `aba_automacao_pessoas_agendor()`: Função que encapsula a lógica da terceira aba do Streamlit.
    *   `aba_robos_lista()`: Função que encapsula a lógica da aba "Gerador de Lista para Robôs" (já existente, mas será adaptada para "Negócios").
    *   `main()`: Função principal que configura as abas do Streamlit.
*   **`data_ingestion.py`:**
    *   `read_csv_smart(filepath)`: Lê arquivos CSV, tentando inferir codificação e delimitador.
*   **`data_cleaning.py`:**
    *   `clean_and_filter_data(df, distancia_padrao)`: Limpa, filtra e padroniza os dados do DataFrame.
*   **`create_pdf.py`:**
    *   `create_pdf(df, filename, title)`: Função original para criação de PDFs, usada pela aba de Higienização.

## 5. Tratamento de Erros e Robustez

Esta seção documenta os erros encontrados durante o desenvolvimento, suas causas e as soluções implementadas ou propostas.

### Erros Comuns

#### Erro: `MergedCell' object has no attribute 'column_letter'`
- **Causa:** Ocorre na função `formatar_planilha` ao tentar ajustar a largura das colunas. A iteração sobre `worksheet.columns` pode retornar objetos `MergedCell` (células mescladas) que não possuem o atributo `column_letter`, necessário para o ajuste de largura.
- [x] **Alternativa 1 (Implementada):** A lógica de iteração foi ajustada para obter as letras das colunas a partir da segunda linha (onde os cabeçalhos da tabela estão), evitando conflito com a célula mesclada do cabeçalho principal.

#### Erro: Prompt de E-mail do Streamlit Persiste
- **Causa:** Apesar das configurações `browser.gatherUsageStats = false` (no `config.toml` e via linha de comando), o Streamlit ainda solicita o e-mail na inicialização.
- [ ] **Alternativa 1 (Re-tentar):** Garantir que o comando de execução inclua `--browser.gatherUsageStats false` e `--server.headless true` para evitar interatividade e forçar a desativação do prompt. Pode ser que a execução anterior tenha sido interrompida antes que a configuração fosse totalmente aplicada.
- [ ] **Alternativa 2:** Verificar a versão do Streamlit e, se necessário, tentar uma reinstalação limpa ou verificar se há alguma variável de ambiente que possa estar sobrescrevendo a configuração.

#### Erro: `UnicodeEncodeError: 'latin-1' codec can't encode character`
- **Causa:** Ocorre na geração do PDF quando há caracteres no DataFrame que não podem ser representados pela codificação `latin-1` ou pela fonte padrão do FPDF (Arial).
- [x] **Alternativa 1 (Tentada):** Usar `pdf.output(dest='S').encode('latin-1', 'replace')` para substituir caracteres não mapeáveis por `?`. **Status: Não resolveu completamente o problema de renderização.**
- [x] **Alternativa 2 (Implementada): Incorporar uma fonte UTF-8 no PDF.**
    - [x] **Passo 1:** Instruir o usuário a baixar os arquivos da fonte **Noto Sans** (`NotoSans-Regular.ttf` e `NotoSans-Bold.ttf`) e colocá-los na pasta `fonts/`.
    - [x] **Passo 2:** Modificar a função `criar_pdf_leads` para carregar e usar a fonte Noto Sans.
    - **Status Atual:** O erro `UnicodeEncodeError` persiste *se* os arquivos da fonte `Noto Sans` não estiverem presentes na pasta `fonts/`, pois o sistema faz fallback para Arial, que não suporta os caracteres.

#### Erro: `TTF Font file not found: fonts/DejaVuSans.ttf` (ou Noto Sans)
- **Causa:** O arquivo da fonte (`NotoSans-Regular.ttf` ou `NotoSans-Bold.ttf`) não foi encontrado no caminho especificado (`fonts/`). Isso impede que o FPDF carregue a fonte UTF-8.
- [x] **Alternativa 1 (Implementada):** Adicionada uma verificação no código para a existência dos arquivos da fonte. Se não encontrados, um aviso claro é emitido na interface do Streamlit, e o sistema faz um fallback para a fonte Arial para evitar a quebra da aplicação.
- [ ] **Alternativa 2:** Fornecer instruções mais explícitas ao usuário sobre onde e como colocar os arquivos da fonte, talvez com um link direto para download de uma fonte confiável.

#### Erro: `a bytes-like object is required, not 'str'`
- **Causa:** Ocorre na função `criar_pdf_leads` quando `pdf.output(dest='S')` retorna uma string, mas `pdf_output_buffer.write()` espera bytes. Isso aconteceu após a remoção do `.encode()` na tentativa de usar fontes UTF-8.
- [x] **Alternativa 1 (Implementada):** A string retornada por `pdf.output(dest='S')` é explicitamente codificada para bytes (UTF-8) antes de ser escrita no buffer: `pdf.output(dest='S').encode('utf-8')`.

#### Erro: PDF Gerado em Branco (Sem Conteúdo)
- **Causa:** O PDF é gerado, mas não exibe o conteúdo da tabela. As causas podem ser: larguras de coluna incorretas, posicionamento do cursor, conteúdo vazio no DataFrame, ou problemas de fonte/codificação.
- [x] **Alternativa 1 (Implementada):** Adicionadas verificações e ajustes na lógica de largura de coluna:
    - [x] Impressão (comentada) das larguras de coluna calculadas e cabeçalhos para depuração.
    - [x] Adicionado um `min_width` para garantir que as colunas sempre tenham uma largura mínima.
    - [x] Verificação se o DataFrame passado para `criar_pdf_leads` não está vazio.
- [x] **Alternativa 2 (Nova Abordagem):** Simplificar a função `criar_pdf_leads` para desenhar apenas um texto fixo e verificar se o PDF não está mais em branco. Se funcionar, reintroduzir a lógica da tabela passo a passo.

#### Aviso: `UserWarning: Data Validation extension is not supported and will be removed`
- **Causa:** Este é um aviso do `openpyxl` ao ler um arquivo Excel que contém validação de dados. Não é um erro que impede a execução, mas indica que essa funcionalidade específica do Excel não é totalmente suportada pela biblioteca ou será descontinuada.
- [ ] **Alternativa 1:** Ignorar o aviso, pois ele não afeta a funcionalidade principal do script.
- [ ] **Alternativa 2:** Suprimir o aviso programaticamente usando o módulo `warnings` do Python. Isso pode ser feito adicionando `import warnings; warnings.filterwarnings("ignore", category=UserWarning, module='openpyxl')` no início do script.

### Erros Exóticos

#### Erro: `KeyError` para colunas essenciais
- **Causa:** O arquivo de entrada não possui as colunas esperadas (`NOME`, `Whats`, `CEL`, etc.) ou elas estão com nomes ligeiramente diferentes.
- [ ] **Alternativa 1:** Fornecer uma interface para o usuário mapear as colunas do arquivo de entrada para as colunas esperadas pelo sistema.
- [ ] **Alternativa 2:** Implementar uma lógica de "fuzzy matching" para tentar encontrar colunas similares, ou um aviso claro sobre as colunas esperadas.

#### Erro: Falha na geração de PDF devido a caracteres especiais
- **Causa:** Caracteres não suportados pela fonte padrão do FPDF ou problemas de codificação ao gerar o PDF.
- [ ] **Alternativa 1:** Usar uma fonte que suporte uma gama mais ampla de caracteres (ex: `DejaVuSans` ou `NotoSans` se instaladas e configuradas).
- [ ] **Alternativa 2:** Sanitizar strings antes de passá-las para o FPDF, removendo ou substituindo caracteres problemáticas.

#### Erro: PDF Gerado em Branco (Reincidente)
- **Causa:** Após correções anteriores, os PDFs da aba "Divisor de Listas" voltaram a ser gerados em branco. A causa provável é um erro na lógica de cálculo de largura das colunas (`col_widths`) em `create_pdf.py`, que pode não estar atribuindo uma largura a todas as colunas, fazendo com que a renderização da tabela falhe silenciosamente.
- [ ] **Alternativa 1:** Simplificar a lógica de cálculo de largura das colunas em `create_pdf_robust` para garantir que todas as colunas recebam um valor de largura válido, evitando a falha na renderização.
