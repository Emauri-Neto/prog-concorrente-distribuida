import pandas as pd
import glob
import os
import matplotlib.pyplot as plt
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

CSV_PATH = "../Dados"
CHUNK_SIZE = 200_000
MAX_WORKERS = 5

def get_files(dir):
    return glob.glob(os.path.join(dir, "*.csv"))

class DataProcessor:
    def __init__(self, files):
        self.files = files
        self.summary = pd.DataFrame()

    def extract(self):
        print("📦 Iniciando EXTRAÇÃO dos dados...")
        start_time = time.perf_counter()
        data = []
        data_lock = threading.Lock()

        def process_file(file):
            print(f"📥 Lendo {file}")
            df = pd.read_csv(file)
            print(f"✅ Finalizado {file}")
            colunas_numericas = [col for col in df.columns if col.startswith(('julg', 'dist', 'susp'))]
            for col in colunas_numericas:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
            with data_lock:
                data.append(df)

        threads = []
        for file in self.files:
            t = threading.Thread(target=process_file, args=(file,))
            threads.append(t)
            t.start()

            while threading.active_count() > MAX_WORKERS:
                for t_check in threads:
                    if not t_check.is_alive():
                        threads.remove(t_check)

        for t in threads:
            t.join()

        all_data = pd.concat(data, ignore_index=True)
        print("🚚 Gerando arquivo consolidado...")
        all_data.to_csv('Consolidado.csv', index=False)
        print("📁 Arquivo Consolidado.csv gerado com sucesso.")
        elapsed = time.perf_counter() - start_time
        print(f"⏱️ EXTRAÇÃO concluída em {elapsed:.2f} segundos.\n")
        return all_data

    def calculate_chunk(self, chunk, formulas):
        start_time = time.perf_counter()
        for meta, fn in formulas.items():
            print(f"🔧 [Chunk {chunk.index[0]}-{chunk.index[-1]}] Iniciando cálculo da {meta}...")
            resultados = []
            for _, row in chunk.iterrows():
                try:
                    resultado = round(fn(row), 2)
                except Exception:
                    resultado = "NA"
                resultados.append(resultado)
            chunk[meta] = resultados
            print(f"✅ [Chunk {chunk.index[0]}-{chunk.index[-1]}] Meta {meta} finalizada.")
        elapsed = time.perf_counter() - start_time
        print(f"⏱️ Chunk {chunk.index[0]}-{chunk.index[-1]} calculado em {elapsed:.2f} segundos.\n")
        return chunk

    def transform(self, df):
        print("⚙️ Iniciando TRANSFORMAÇÃO das metas...")
        start_time = time.perf_counter()

        formulas = {
            # Comuns a quase todos os ramos
            'Meta1': lambda r: (r['julgadom1'] / (r['cnm1'] + r['desm1'] - r['susm1'])) * 100,
            'Meta2A': lambda r: (r['julgm2_a'] / (r['distm2_a'] - r['suspm2_a'])) * (1000 / 8),
            'Meta2B': lambda r: (r['julgm2_b'] / (r['distm2_b'] - r['suspm2_b'])) * (1000 / 9),
            'Meta2C': lambda r: (r['julgm2_c'] / (r['distm2_c'] - r['suspm2_c'])) * (1000 / 9.5),
            'Meta2ANT': lambda r: (r['julgm2_ant'] / (r['distm2_ant'] - r['suspm2_ant'])) * 100,
            'Meta4A': lambda r: (r['julgm4_a'] / (r['distm4_a'] - r['suspm4_a'])) * (1000 / 6.5),
            'Meta4B': lambda r: (r['julgm4_b'] / (r['distm4_b'] - r['suspm4_b'])) * 100,
            'Meta6': lambda r: (r['julgm6_a'] / (r['distm6_a'] - r['suspm6_a'])) * 100,
            'Meta7A': lambda r: (r['julgm7_a'] / (r['distm7_a'] - r['suspm7_a'])) * (1000 / 5),
            'Meta7B': lambda r: (r['julgm7_b'] / (r['distm7_b'] - r['suspm7_b'])) * (1000 / 5),
            'Meta8A': lambda r: (r['julgm8_a'] / (r['distm8_a'] - r['suspm8_a'])) * (1000 / 7.5),
            'Meta8B': lambda r: (r['julgm8_b'] / (r['distm8_b'] - r['suspm8_b'])) * (1000 / 9),
            'Meta10A': lambda r: (r['julgm10_a'] / (r['distm10_a'] - r['suspm10_a'])) * (1000 / 9),
            'Meta10B': lambda r: (r['julgm10_b'] / (r['distm10_b'] - r['suspm10_b'])) * (1000 / 10),

            # Justiça Federal
            'Meta2AF': lambda r: (r['julgm2_a'] / (r['distm2_a'] - r['suspm2_a'])) * (1000 / 8.5),
            'Meta2BF': lambda r: (r['julgm2_b'] / (r['distm2_b'] - r['suspm2_b'])) * 100,
            'Meta4AF': lambda r: (r['julgm4_a'] / (r['distm4_a'] - r['suspm4_a'])) * (1000 / 7),
            'Meta6F': lambda r: (r['julgm6_a'] / (r['distm6_a'] - r['suspm6_a'])) * (1000 / 3.5),
            'Meta7AF': lambda r: (r['julgm7_a'] / (r['distm7_a'] - r['suspm7_a'])) * (1000 / 3.5),
            'Meta7BF': lambda r: (r['julgm7_b'] / (r['distm7_b'] - r['suspm7_b'])) * (1000 / 3.5),

            # Justiça Militar da União e Estadual
            'Meta2AM': lambda r: (r['julgm2_a'] / (r['distm2_a'] - r['suspm2_a'])) * (1000 / 9.5),
            'Meta2BM': lambda r: (r['julgm2_b'] / (r['distm2_b'] - r['suspm2_b'])) * (1000 / 9.9),
            'Meta4AM': lambda r: (r['julgm4_a'] / (r['distm4_a'] - r['suspm4_a'])) * (1000 / 9.5),
            'Meta4BM': lambda r: (r['julgm4_b'] / (r['distm4_b'] - r['suspm4_b'])) * (1000 / 9.9),

            # Justiça Eleitoral
            'Meta2AE': lambda r: (r['julgm2_a'] / (r['distm2_a'] - r['suspm2_a'])) * (1000 / 7),
            'Meta2BE': lambda r: (r['julgm2_b'] / (r['distm2_b'] - r['suspm2_b'])) * (1000 / 9.9),
            'Meta4AE': lambda r: (r['julgm4_a'] / (r['distm4_a'] - r['suspm4_a'])) * (1000 / 9),
            'Meta4BE': lambda r: (r['julgm4_b'] / (r['distm4_b'] - r['suspm4_b'])) * (1000 / 5),

            # TST (Tribunal Superior do Trabalho)
            'Meta2AT': lambda r: (r['julgm2_a'] / (r['distm2_a'] - r['suspm2_a'])) * (1000 / 9.5),
            'Meta2BT': lambda r: (r['julgm2_b'] / (r['distm2_b'] - r['suspm2_b'])) * (1000 / 9.9),

            # STJ (Superior Tribunal de Justiça)
            'Meta4ASTJ': lambda r: (r['julgm4_a'] / (r['distm4_a'] - r['suspm4_a'])) * (1000 / 9),
            'Meta4BSTJ': lambda r: (r['julgm4_b'] / (r['distm4_b'] - r['suspm4_b'])) * 100,
            'Meta6STJ': lambda r: (r['julgm6_a'] / (r['distm6_a'] - r['suspm6_a'])) * (1000 / 7.5),
            'Meta7ASTJ': lambda r: (r['julgm7_a'] / (r['distm7_a'] - r['suspm7_a'])) * (1000 / 7.5),
            'Meta7BSTJ': lambda r: (r['julgm7_b'] / (r['distm7_b'] - r['suspm7_b'])) * (1000 / 7.5),
            'Meta8STJ': lambda r: (r['julgm8_a'] / (r['distm8_a'] - r['suspm8_a'])) * (1000 / 10),
            'Meta10STJ': lambda r: (r['julgm10_a'] / (r['distm10_a'] - r['suspm10_a'])) * (1000 / 10),
        }

        total = len(df)
        chunks = [(i, df.iloc[i:i + CHUNK_SIZE].copy()) for i in range(0, total, CHUNK_SIZE)]
        results = []

        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = {executor.submit(self.calculate_chunk, chunk, formulas): i for i, chunk in chunks}
            for future in as_completed(futures):
                result = future.result()
                results.append(result)

        self.df = pd.concat(results, ignore_index=True)
        elapsed = time.perf_counter() - start_time
        print(f"✅ TRANSFORMAÇÃO concluída em {elapsed:.2f} segundos.\n")

    def load(self):
        print("💾 Iniciando CARGA dos dados...")
        start_time = time.perf_counter()
        cols = ['sigla_tribunal', 'ramo_justica'] + [c for c in self.df.columns if c.startswith('Meta')]
        self.summary = self.df[cols].copy()
        self.summary.fillna("NA", inplace=True)
        self.summary.to_csv('ResumoMetas.csv', index=False)
        elapsed = time.perf_counter() - start_time
        print("📁 Arquivo ResumoMetas.csv gerado com sucesso.")
        print(f"⏱️ CARGA concluída em {elapsed:.2f} segundos.\n")

    def show_graph(self):
        print("📊 Iniciando GERAÇÃO DE GRÁFICO...")
        start_time = time.perf_counter()
        metas = [col for col in self.summary.columns if col.startswith("Meta")]
        medias = []

        for meta in metas:
            col_data = pd.to_numeric(self.summary[meta], errors='coerce')
            medias.append(col_data.mean(skipna=True))

        plt.figure(figsize=(14, 7))
        plt.bar(metas, medias, color='skyblue')
        plt.xticks(rotation=45, ha='right')
        plt.ylabel("Média de desempenho")
        plt.title("Desempenho médio por Meta")

        observacao = (
            "Observação: As metas com variação de nome foram diferenciadas com sufixos como F (Federal), "
            "M (Militar), E (Eleitoral), T (Trabalho), STJ, etc., para evitar conflitos e permitir cálculos "
            "separados por ramo da justiça."
        )
        plt.figtext(0.5, -0.05, observacao, wrap=True, horizontalalignment='center', fontsize=9)

        plt.tight_layout()
        plt.savefig("grafico_metas.png", bbox_inches='tight')
        plt.show()

        elapsed = time.perf_counter() - start_time
        print(f"✅ Gráfico gerado com sucesso (grafico_metas.png) em {elapsed:.2f} segundos.\n")

if __name__ == "__main__":
    arquivos = get_files(CSV_PATH)
    print("🟢 Arquivos localizados:", arquivos)

    etl = DataProcessor(arquivos)

    print("🚀 Etapa: Extração")
    df = etl.extract()

    print("🛠️ Etapa: Transformação")
    etl.transform(df)

    print("🚚 Etapa: Carga")
    etl.load()

    print("📑 Etapa: Gráfico")
    etl.show_graph()

    print("✅ Processo inteiro completo")
