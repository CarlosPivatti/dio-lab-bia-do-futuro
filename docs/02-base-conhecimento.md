# Base de Conhecimento

## Dados Utilizados


| Arquivo | Formato | Utilização no Agente |
|---------|---------|---------------------|
| `historico_atendimento.csv` | CSV | Contexto Conversacional: Resgata solicitações anteriores de simulação, dúvidas pendentes sobre o envio de documentos ou recusas prévias para dar continuidade ao suporte sem repetir perguntas. |
| `perfil_usuario.json` | JSON | Segmentação do Proponente: Identifica a categoria do usuário (Motorista de App, Taxista ou Caminhoneiro Autônomo), tempo de atuação e gênero (essencial para aplicar os incentivos de taxas reduzidas para mulheres).|
| `produtos_financeiros.json` | JSON | Regras de Negócio e Linhas de Crédito: Funciona como a "tabela oficial" do agente. Contém as taxas de juros, prazos máximos, períodos de carência e critérios de elegibilidade do BNDES para cada categoria.|
| `transacoes.csv` | CSV | Histórico de Contratos: Registra financiamentos ativos ou passados vinculados ao CPF do usuário, permitindo ao agente informar saldos devedores, parcelas pagas e contratos em andamento. |



---

## Adaptações nos Dados

> Você modificou ou expandiu os dados mockados? Descreva aqui.

Sim. A massa de dados original (voltada para investimentos bancários tradicionais) foi totalmente adaptada para o ecossistema de mobilidade e crédito público do programa Move Brasil:

O arquivo perfil_investidor.json foi renomeado para perfil_usuario.json e modificado para conter variáveis como categoria_motorista (App/Taxista/Caminhoneiro), tempo_cadastro_meses, media_corridas_mensais e score_credito.

O arquivo produtos_financeiros.json foi reformulado para conter as três linhas de crédito oficiais operadas pelo BNDES no programa, detalhando juros diferenciados por gênero, tetos de financiamento (ex: até R$ 150 mil para apps) e exigências sustentáveis do Programa Mover (eficiência energética).

O arquivo transacoes.csv foi limpo de despesas cotidianas e preenchido com registros de liberações de crédito de frota, pagamento de parcelas de financiamento de veículos e subsídios governamentais.

---

## Estratégia de Integração

### Como os dados são carregados?

O agente utiliza uma estratégia híbrida. No início da sessão, o backend da aplicação realiza a leitura dos arquivos perfil_usuario.json, transacoes.csv e historico_atendimento.csv filtrando estritamente pelo CPF/ID do usuário logado. O arquivo produtos_financeiros.json (que é estático e serve como manual de regras) é carregado na memória do sistema como a fonte única de verdade sobre as condições do governo.

### Como os dados são usados no prompt?

Os dados são injetados dinamicamente no Contexto de Prompt a cada nova iteração, utilizando a seguinte divisão:

System Prompt (Fixo): Contém as instruções de comportamento da IA, tom de voz (didático e prestativo) e a estrutura imutável de regras do produtos_financeiros.json.

User Context (Dinâmico): Injetado logo acima da mensagem atual do usuário, contendo os dados estruturados do perfil dele, o resumo resumido das últimas transações de financiamento e o histórico dos últimos atendimentos relevantes.

---

## Exemplo de Contexto Montado

[INSTRUÇÕES DO SISTEMA: Você é o assistente virtual do Move Brasil 2026. Use os dados abaixo para responder o usuário de forma personalizada.]

DADOS DO PROPONENTE LOGADO:
- Nome: Carlos Pivatti
- Categoria: Motorista de Aplicativo
- Tempo de Atividade: 14 meses
- Histórico de Corridas: Atende ao requisito (Média de 120 corridas/mês)
- Gênero para Benefício: Masculino (Taxa padrão da linha: 12.6% a.a.)

HISTÓRICO DE CONTRATOS ATIVOS (transacoes.csv):
- Contrato nº 4892-X: Financiamento de Veículo Flex (Ativo)
- Última parcela paga: 15/05/2026 — Valor: R$ 1.450,00 (Status: OK)

ÚLTIMO ATENDIMENTO RELEVANTE (historico_atendimento.csv):
- Data: 28/05/2026: "Usuário demonstrou interesse em refinanciar ou buscar uma segunda linha de crédito para troca de veículo da esposa."

PERGUNTA DO USUÁRIO: "Consigo puxar mais um crédito pelo programa para um segundo carro?"
