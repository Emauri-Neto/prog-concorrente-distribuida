# Projeto Final

É importante ressaltar que o código foi produzido no sistema operacional `Ubuntu 22.04.5 LTS` e utilizando o Python na versão `3.10.12`.

## Como Executar

> Para que o programa funcione corretamente, posicione a pasta dos CSVs um nível acima das pastas de versão (P ou NP). Alternativamente, edite o arquivo main.py para ajustar o caminho. O caminho padrão é `CSV_PATH = "../Dados"`.

```
.
├── Dados/
├── NP_version/
├── P_version/
└── README.md
```

1.  Entre na versão que deseja executar:

    > Para garantir a execução conforme testado, é crucial excluir todos os arquivos gerados em qualquer execução anterior do código.

    * **Não paralelizada:**

        ```bash
        cd NP_version
        ```

    * **Paralelizada:**

        ```bash
        cd P_version
        ```

2. Crie um ambiente virtual e o ative

    ```bash
    python -m venv venv
    ```

    **Ativação:**

    * **Linux:**

        ```bash
        source venv/bin/activate
        ```

    * **Windows:**

        ```powershell
        .\venv\Scripts\Activate
        ```

    **Desativação:**

    Em ambos os sistemas, o comando é:

    ```bash
    deactivate
    ```

3. Instale as dependências

    ```bash
    pip install -r requirements.txt
    ```

4. Execute o código de uma das seguintes formas:

    * **Utilizando o script shell na raiz do projeto:**

        ```bash
        sh ./main.sh
        ```

        > Este arquivo apaga as execuções anteriores e é recomendado se o projeto já foi iniciado. Funciona exclusivamente no Linux.

    * **Manualmente:**

        Primeiramente, exclua todos os arquivos de execuções anteriores, mesmo que tenham falhado.

        Após isso, execute o comando:

        ```bash
        python main.py
        ```

## Considerações Importantes

O sistema inteiro foi produzido em uma máquina com um Intel i7 (8 núcleos e 16 threads) e 16 GB de memória RAM. Sendo assim, a execução do script teve de ser adaptada para essa máquina, uma vez que um upgrade não seria viável. A versão NP teve de ser separada em *chunks* de 500k linhas para garantir que o processo não fosse "morto" pelo WSL, sem aviso ou erro, como demonstra o log abaixo:

> Log gerado pelo comando `dmesg -T | grep -i "killed process"`

```c
[Wed Jun 18 14:17:32 2025] Out of memory: Killed process 62577 (python3) total-vm:23256048kB, anon-rss:15389488kB, file-rss:0kB, shmem-rss:0kB, UID:1000 pgtables:35788kB oom_score_adj:0
[Wed Jun 18 14:42:57 2025] Out of memory: Killed process 63830 (python3) total-vm:24879652kB, anon-rss:15029124kB, file-rss:0kB, shmem-rss:0kB, UID:1000 pgtables:35792kB oom_score_adj:0
[Wed Jun 18 15:11:02 2025] Out of memory: Killed process 72402 (python3) total-vm:25088080kB, anon-rss:14991964kB, file-rss:0kB, shmem-rss:0kB, UID:1000 pgtables:35844kB oom_score_adj:0
[Wed Jun 18 15:35:55 2025] Out of memory: Killed process 79286 (python3) total-vm:25205804kB, anon-rss:15316344kB, file-rss:0kB, shmem-rss:0kB, UID:1000 pgtables:36300kB oom_score_adj:0
[Wed Jun 18 15:40:38 2025] Out of memory: Killed process 86835 (python3) total-vm:23181912kB, anon-rss:15351824kB, file-rss:0kB, shmem-rss:0kB, UID:1000 pgtables:35588kB oom_score_adj:0
[Wed Jun 18 15:49:00 2025] Out of memory: Killed process 88011 (python3) total-vm:22536708kB, anon-rss:15161740kB, file-rss:0kB, shmem-rss:0kB, UID:1000 pgtables:35132kB oom_score_adj:0
[Wed Jun 18 17:57:28 2025] Out of memory: Killed process 21020 (python3) total-vm:18339608kB, anon-rss:14874272kB, file-rss:0kB, shmem-rss:0kB, UID:1000 pgtables:34608kB oom_score_adj:0
```

Além disso, a versão P e a versão NP podem ser editadas utilizando as constantes que limitam o código para garantir que o comportamento descrito anteriormente também aconteça, uma vez que processar simultaneamente muitas linhas ocasiona o mesmo problema. Sendo `CHUNK_SIZE` a quantidade de linhas a ser processada a cada vez e `MAX_WORKERS` o número de threads simultâneas que podem ser criadas. Sendo assim, há variação do desempenho baseado em como se modificam essas constantes. Em computadores mais potentes, é bem provável que o tempo de execução da versão Paralelizada seja inferior ao da Não Paralelizada. No entanto, em computadores com menor quantidade de memória RAM, é possível que haja uma inversão desse tempo, onde a versão NP ganha em tempo da versão P.

```python
    CHUNK_SIZE = 200_000
    MAX_WORKERS = 5
```