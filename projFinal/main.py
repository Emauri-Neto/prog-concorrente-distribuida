import pandas as pd
import glob
import os

CSV_PATH = "./dados"

def get_files(dir):
    return glob.glob(os.path.join(dir, "*.csv"))


class DataProcessor:
    def __init__(self, files):
        self.files = files
        self.df = pd.DataFrame()
        self.summary = pd.DataFrame()

    def get_data(self):
        data = []

        for file in self.files:
            print(f"Arquivo {file} - Processando")
            dt = pd.read_csv(file)
            data.append(dt)
            print(f"Arquivo {file} - Finalizado")
        
        self.df = pd.concat(data, ignore_index=True)
        self.df.to_csv('resumo.csv', index=False)

        print("Arquivo gerado com sucesso.")

    def transform(self):
        formulas = {
            # ISSO EH SO JUSTICA ESTADUAL :D
            'Meta1': lambda row: (row['julgados_2025'] / (row['casos_novos_2025'] + row['dessobrestados_2025'] - row['suspensos_2025'])) * 100,
            'Meta2A': lambda row: (row['julgados_m2_a'] / (row['distribuidos_m2_a'] - row['suspensos_m2_a'])) * (1000 / 8),
            'Meta2B': lambda row: (row['julgados_m2_b'] / (row['distribuidos_m2_b'] - row['suspensos_m2_b'])) * (1000 / 9),
            'Meta2C': lambda row: (row['julgados_m2_c'] / (row['distribuidos_m2_c'] - row['suspensos_m2_c'])) * (1000 / 9.5),
            'Meta2ANT': lambda row: (row['julgados_m2_ant'] / (row['distribuidos_m2_ant'] - row['suspensos_m2_ant'])) * 100,
            'Meta4A': lambda row: (row['julgados_m4_a'] / (row['distribuidos_m4_a'] - row['suspensos_m4_a'])) * (1000 / 6.5),
            'Meta4B': lambda row: (row['julgados_m4_b'] / (row['distribuidos_m4_b'] - row['suspensos_m4_b'])) * 100,
            'Meta6': lambda row: (row['julgados_m6'] / (row['distribuidos_m6'] - row['suspensos_m6'])) * 100,
            'Meta7A': lambda row: (row['julgados_m7_a'] / (row['distribuidos_m7_a'] - row['suspensos_m7_a'])) * (1000 / 5),
            'Meta7B': lambda row: (row['julgados_m7_b'] / (row['distribuidos_m7_b'] - row['suspensos_m7_b'])) * (1000 / 5),
            'Meta8A': lambda row: (row['julgados_m8_a'] / (row['distribuidos_m8_a'] - row['suspensos_m8_a'])) * (1000 / 7.5),
            'Meta8B': lambda row: (row['julgados_m8_b'] / (row['distribuidos_m8_b'] - row['suspensos_m8_b'])) * (1000 / 9),
            'Meta10A': lambda row: (row['julgados_m10_a'] /  (row['distribuidos_m10_a'] - row['suspensos_m10_a'])) * (1000 / 9),
            'Meta10B': lambda row: (row['julgados_m10_b'] /  (row['distribuidos_m10_b'] - row['suspensos_m10_b'])) * (1000 / 10),
        }

        for name, fn in formulas.items():
            print(f"{name} - Iniciando calculo")
            self.df[name] = self.df.apply(
                lambda row: self.calculate(row, fn), axis=1
            )
            print(f"{name} - Calculado")

    def calculate(self, row, fn):
        try:
            return fn(row)
        except (ZeroDivisionError, KeyError):
            return "NA"
        except Exception as e:
            print(f"Erro calculando a meta -> {e}")
            return "NA"

    def load_data(self):
        cols = ['tribunal', 'ramo_justica'] + [col for col in self.df.columns if col.startswith('Meta')]
        self.summary = self.df[cols].copy()
        self.summary.fillna('NA', inplace=True)
        print("Resumo gerado com sucesso")

    def show_data(self):
        pass

if __name__ == "__main__":
    files = get_files(CSV_PATH)

    nv = DataProcessor(files)
    nv.get_data()
    nv.transform()
    nv.load_data()