# 🤖 Automação de eventos com IA — Fase 1 (Sugestão → IA → Pull Request)

## Como funciona

```
Issue "Sugerir evento" ──► comitê aplica o label `processar` ──► Action lê a página
   ──► IA extrai os dados ──► valida + checa duplicata ──► Pull Request ──► revisão humana ──► merge ──► site atualizado
```

A IA **nunca publica**: ela só propõe um PR. Quem faz o merge é uma pessoa.

## Arquivos (copie para a raiz do repositório, mantendo as pastas)

| Arquivo | Função |
|:--|:--|
| `.github/ISSUE_TEMPLATE/sugerir-evento.yml` | Formulário "Sugerir evento" |
| `.github/workflows/sugestao-evento.yml` | Dispara com o label `processar`, chama a IA e abre o PR |
| `.github/workflows/validador.yml` | **Substitui o atual.** Agora valida campos, custo, datas e links (e roda em PRs) |
| `scripts/eventos_lib.py` | Leitura/escrita do JSON, validação, duplicatas |
| `scripts/validar.py` | Fiscal usado pelo CI (também roda local: `python3 scripts/validar.py`) |
| `scripts/processar_sugestao.py` | Lê a issue, busca a página, chama o LLM |
| `scripts/requirements.txt` | Dependências do script de IA |

## Configuração (uma vez só)

1. **Chave da API:** *Settings → Secrets and variables → Actions → New repository secret* → nome `ANTHROPIC_API_KEY` (chave criada em console.anthropic.com).
2. **Permitir que Actions abram PRs:** *Settings → Actions → General → Workflow permissions* → marque **Read and write permissions** e **Allow GitHub Actions to create and approve pull requests**.
3. **(Recomendado) Token para o validador rodar nos PRs:** PRs abertos com o token padrão do GitHub *não* disparam outros workflows. Crie um *fine-grained personal access token* restrito a este repositório com permissões **Contents: Read and write** e **Pull requests: Read and write**, e salve como secret `PR_TOKEN`. Sem ele tudo funciona, mas o ✅ do validador não aparece no PR (o script já valida antes de gerar o PR de qualquer forma).
4. **Labels:** crie `sugestao-evento` (o formulário aplica sozinho) e `processar` (você aplica manualmente). O label `evento-ia` é criado pela própria Action.
5. **(Recomendado) Proteger a `main`:** *Settings → Branches → Add rule* para `main` exigindo o check **verificacao-de-dados** antes do merge. Se o Pages publica direto da `main`, é isso que faz o ❌ realmente impedir uma publicação quebrada.

## Como usar

1. Alguém abre *Issues → New issue → 📅 Sugerir evento* e cola o link.
2. Você aplica o label **`processar`**.
3. Em ~1 minuto a Action comenta na issue com o resultado e, se deu certo, abre o Pull Request com uma tabela dos dados e um checklist de revisão.
4. Revise (abra o link, confira data/custo) e faça o merge. A issue fecha sozinha.

Se a IA não conseguir ler a página (comum no LinkedIn), ela avisa na issue: cole o texto do evento em *Informações adicionais*, reaplique `processar`.

## Ajustes úteis

- **Modelo:** padrão `claude-haiku-5-5` (barato e suficiente para extração). Para trocar, defina `MODELO_IA` no passo "Extrair dados do evento com IA" do workflow.
- **Categorias/estados/custos:** constantes no topo de `scripts/eventos_lib.py`.
- **Processar sem label:** troque o gatilho para `types: [opened]` e a condição do job — mas qualquer pessoa passará a gastar sua cota da API.
