# Runbook — rodar os scripts do claude-quickstart

Passo a passo para executar qualquer script de `src/` e resolver os erros mais comuns.

## 1. Instalar as dependências (uma vez só)

O projeto usa o [uv](https://docs.astral.sh/uv/) para gerenciar o Python, o ambiente virtual e as bibliotecas.

### 1.1 uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh   # ou: brew install uv
uv --version
uv self update                                    # atualizar mais tarde
```

### 1.2 Python + bibliotecas

Na raiz do repositório:

```bash
uv sync
```

Esse comando:

- lê o `.python-version` (3.12) e baixa essa versão do Python se ela não estiver na máquina;
- cria o `.venv/`;
- instala exatamente as versões do `uv.lock`.

Arquivos envolvidos:

| Arquivo | Papel |
|---|---|
| `pyproject.toml` | Dependências diretas: `anthropic==2.9.0`, `httpx==0.28.1`, `pydantic==2.14.3` |
| `uv.lock` | Versões exatas de todas as dependências, incluindo as transitivas. Não edite à mão |
| `.python-version` | Versão do Python do projeto |

> O `uv run` (seção 3) já faz o `uv sync` automaticamente. Rodar o `uv sync` antes é opcional.

Gerenciar bibliotecas:

```bash
uv add <pacote>              # adiciona ao pyproject.toml e ao uv.lock
uv remove <pacote>           # remove
uv lock --upgrade-package anthropic && uv sync   # atualiza o SDK (ajuste o pin no pyproject.toml antes)
uv tree                      # mostra a árvore de dependências
```

### 1.3 CLI `ant` (para login OAuth)

```bash
brew install --cask ant      # instala
brew upgrade --cask ant      # atualiza
ant --version                # confere
```

> Se for usar só `ANTHROPIC_API_KEY` (opção B abaixo), o CLI `ant` é opcional.

## 2. Autenticação

O SDK procura credenciais nesta ordem:

1. Variável `ANTHROPIC_API_KEY`, se estiver definida.
2. Perfil OAuth do CLI `ant` (`~/.config/anthropic/credentials/default.json`).

### Opção A — OAuth com o CLI `ant` (recomendada)

```bash
ant auth status      # mostra se já está logado e em qual org/workspace
ant auth login       # abre o navegador; só precisa repetir se a credencial quebrar
```

O token é renovado sozinho, porque o login salva um `refresh_token`.

### Opção B — API key

```bash
export ANTHROPIC_API_KEY="sk-ant-..."   # para não repetir, coloque no ~/.zshrc
```

> Com `ANTHROPIC_API_KEY` definida, o SDK usa a chave e ignora o perfil OAuth.

## 3. Rodar um script

Sempre a partir da raiz do repositório:

```bash
uv run src/base/chamada_input_output.py
```

Outros exemplos:

```bash
uv run src/base/turnos_input_output.py
uv run src/base/stop_reason4_tool_use.py
uv run src/tools/tool1.py
```

**Resultado esperado** (`chamada_input_output.py`): o objeto `Message` completo, depois só o texto da resposta, por exemplo `Hello! What's on your mind today?`.

Se o objeto mostrar um `ThinkingBlock`, não é erro: é o raciocínio do modelo. Os scripts filtram com `if block.type == "text":`.

> Na IDE (PyCharm/VS Code), aponte o interpretador para `.venv/bin/python`.

## 4. Troubleshooting

| Sintoma | Causa | Correção |
|---|---|---|
| `WorkloadIdentityError: ... must include 'refresh_token'` | Credencial OAuth antiga/expirada e sem `refresh_token` | `ant auth login` |
| `AuthenticationError` / `401` | API key inválida ou token revogado | Conferir `ANTHROPIC_API_KEY` ou rodar `ant auth login` |
| Usa a org/workspace errada | `ANTHROPIC_API_KEY` sobrescreve o perfil OAuth, ou o perfil aponta para outra org | `unset ANTHROPIC_API_KEY`; `ant auth status`; `ant auth login --profile <nome>` |
| `NotFoundError` com o nome do modelo | Nome de modelo errado | Usar `claude-opus-5` (padrão do repo) |
| `ModuleNotFoundError` | Rodou com `python` em vez de `uv run`, ou o venv está desatualizado | Usar `uv run <script>`; se persistir, `uv sync` |
| `command not found: uv` | uv não instalado ou fora do `PATH` | Seção 1.1; abrir um terminal novo |
| venv quebrado | `.venv` corrompido ou de outra versão do Python | `rm -rf .venv && uv sync` |

### Checagem rápida (diagnóstico em 3 comandos)

```bash
echo "API key definida: ${ANTHROPIC_API_KEY:+sim}"
ant auth status
uv run src/base/chamada_input_output.py
```
