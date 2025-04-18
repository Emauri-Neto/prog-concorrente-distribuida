# Projeto 1

Este projeto está localizado na pasta `projeto1`. Após clonar o repositório, acesse a pasta com o comando:

```bash
cd projeto1
```

## Como executar

Você pode executar o projeto de duas formas:

### 1. Utilizando o script shell

Execute o script `main.sh` com o seguinte comando:

```bash
sh ./main.sh
```

### 2. Manualmente

Inicie primeiro o **servidor**:

```bash
python3 server.py
```

Depois, em outro terminal, inicie o **cliente**:

```bash
python3 client.py
```

> ⚠️ Dependendo da sua instalação do Python, especialmente no Windows, o comando pode ser apenas `python` em vez de `python3`.

## Ordem de execução

O servidor **sempre** deve ser iniciado antes do cliente.

## Testes com múltiplos usuários

Para testar as funcionalidades descritas no documento:

1. Abra **5 terminais** diferentes.
2. Em cada um deles, execute o cliente:
   ```bash
   python3 client.py
   ```
3. Após a execução, digite o comando `entrar` para ingressar na sala.

> O sistema aceita até 5 conexões simultâneas. Ao atingir esse limite, novas tentativas de entrada serão automaticamente bloqueadas.

---

Sinta-se à vontade para abrir issues ou enviar pull requests caso tenha sugestões ou melhorias!
