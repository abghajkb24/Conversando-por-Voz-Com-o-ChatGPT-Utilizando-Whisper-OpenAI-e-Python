# Voz <-> ChatGPT (Whisper + ChatGPT + gTTS) — Exemplo funcional com módulo financeiro

Este repositório é um esqueleto funcional de uma API que:
- recebe áudio (wav/mp3/m4a),
- transcreve usando Whisper (OpenAI),
- envia a transcrição ao ChatGPT,
- sintetiza a resposta com gTTS (Google Text-to-Speech),
- retorna transcrição, resposta e áudio em base64.

Extensão: Relationship Finance Agent
- Integra funcionalidades voltadas a relacionamento financeiro: FAQ inteligente, simulações financeiras (empréstimos, poupança, parcelamento), persistência simples de contexto por sessão/usuário e regras básicas de segurança.

Novos recursos adicionados (resumo)
- Endpoints financeiros (APIs REST) para:
  - cálculos financeiros demonstrativos (/api/v1/finance/calculate),
  - FAQ inteligente via LLM e base local (/api/v1/finance/faq),
  - fluxo unificado que combina voz + contexto financeiro (/api/v1/finance/converse) — opcional.
- Persistência leve (SQLite) para sessão/ histórico (session_id).
- Modelos Pydantic e testes unitários para cálculos.
- Prompts e proteções para evitar aconselhamento financeiro impróprio (system prompts & disclaimers).

Novos endpoints (especificação resumida)

POST /api/v1/finance/calculate
- Body (application/json):
  {
    "type": "loan" | "savings" | "installment",
    "params": { ... }  // ver exemplos abaixo
  }
- Response:
  {
    "result": { ... },
    "explanation": "texto explicando"
  }

Exemplo: simulação de empréstimo
- type: "loan"
- params: { "principal": 10000, "annual_rate_pct": 12, "term_months": 24, "compounding": "monthly" }

POST /api/v1/finance/faq
- Body:
  { "question": "Qual a diferença entre CDB e poupança?" }
- Response:
  { "answer": "..." }
- Implementação: consulta local (Markdown/JSON) + fallback para LLM com prompt controlado.

POST /api/v1/finance/converse
- Integra com /api/v1/converse (voz) → detecta intenção (FAQ vs cálculo) e roteia para finance/calculate ou ChatGPT. Mantém contexto por session_id.

Banco de dados / persistência
- Arquivo SQLite simples (por default ./data/app.db)
- Tabelas: sessions (id TEXT PRIMARY KEY, created_at, updated_at, data JSON), optional users/profiles

Variáveis de ambiente novas/alteradas
- DB_PATH=./data/app.db
- FINANCE_FAQ_PATH=./data/finance_faq.json  (base de conhecimento)
- FINANCE_TRUSTED_ORGS (opcional) — políticas

Como rodar (além do já existente)
1. Criar DB inicial (script init_db será fornecido).
2. Popule ./data/finance_faq.json com perguntas/respostas (opcional).
3. Executar servidor (mesma instrução do principal).

Testes
- pytest cobrirá: funções de cálculo, validação de entrada e rotas principais.
- Tests usam valores conhecidos (fórmulas de juros simples/compostos, PMT para empréstimos).

Boas práticas / Segurança
- Exibir disclaimer em respostas financeiras: "Esta simulação é apenas demonstrativa e não substitui aconselhamento financeiro profissional."
- Não solicitar nem armazenar dados sensíveis (número de conta, CPF) sem criptografia e políticas de conformidade.
- Rate-limiting em endpoints de ChatGPT para evitar abuso e custos.
- Sanitização de inputs numéricos e limites máximos (ex: principal <= 1e8).

Critérios de avaliação (financeiro)
- Correção dos cálculos (exatidão matemática).
- Clareza das explicações (linguagem simples).
- Persistência de contexto por sessão (se implementada).
- Testes unitários cobrem casos típicos e limites.
- Prompt engineering e medidas de segurança.

Próximo passo
- Se quiser, eu gero os arquivos iniciais (esqueleto + testes) automaticamente no repositório. Quer que eu gere agora?
