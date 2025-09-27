import pandas as pd

class GerenciarArquivos():
  
  def __init__(self):
    self.processarArquivos('Datasets\Tabela 1.13.1.xls','EmpoderamentoEconomico_HomensMulheres_PorCargo')
    self.processarArquivos('Datasets\Tabela 1.13.xls','EmpoderamentoEconomico_HomensMulheres_PorRegiao')
  
  def processarArquivos(self, arquivo, nome):
    xls = pd.ExcelFile(arquivo)

    df_total = pd.DataFrame()

    for aba in xls.sheet_names:
        df = pd.read_excel(arquivo, sheet_name=aba)
        ano = aba
        df.dropna(inplace=True)
        df = df.rename(columns={df.columns[0]: "Indicadores",df.columns[1]:'Total',df.columns[2]:'Homens', df.columns[3]:'Mulheres', df.columns[4]:'Razao'})
        df['Ano'] = ano
        df_total = pd.concat([df_total, df], ignore_index=True)

    df_total['Razao'] = pd.to_numeric(df_total['Razao'], errors='coerce')
    df_total.dropna(inplace=True)
    df_total.to_csv(f"Datasets\{nome}.csv", index=False, encoding='utf-8-sig')


