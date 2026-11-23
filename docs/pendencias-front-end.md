# Pendências do Front-end — LS Management

## Objetivo

Este documento organiza o que falta implementar na interface conforme o TAP v2.0 e os requisitos da 3ª entrega. A estratégia é desenvolver primeiro as telas e interações possíveis no front-end e, em uma etapa posterior, integrar os fluxos à API e às regras implementadas pelo back-end.

O front-end pode preparar formulários, navegação, visualização, estados, validações de entrada e protótipos com dados claramente identificados como locais. Não deve apresentar regras de negócio simuladas como decisões oficiais nem confirmar operações que ainda não foram persistidas pela API.

## Convenções de implementação

- **Front primeiro:** construir a experiência da tela, os componentes, os estados vazios/carregando/erro e a navegação entre etapas.
- **Integração posterior:** concentrar chamadas em serviços do front existentes ou novos serviços da mesma camada; não espalhar URLs e regras de API pelos componentes.
- **Sem sucesso fictício:** enquanto a API não existir, deixar a integração identificada como pendente e não mostrar uma operação como salva ou validada.
- **Regra oficial no servidor:** idade reprodutiva, parentesco, carência sanitária, elegibilidade para ordenha e autorização por perfil devem ser confirmados pelo back-end. A interface pode antecipar a experiência e exibir o resultado recebido.
- **Contratos pendentes:** nomes de campos, estados, payloads, endpoints e formatos de resposta abaixo são itens para alinhamento com o back-end, não contratos já definidos.

## O que já existe e deve ser preservado

- Cadastro de nascimento com data, peso e tipo de ocorrência, gravação pela API e associação ao animal. A ascendência mostrada depende da inseminação associada.
- Consulta de pesagens, curva de peso e registro de nova pesagem.
- Cadastro e listagem de inseminações, com indicadores de ultrassom estimado e previsão de parto.
- Registro de vacinação individual/em lote e visualização de próximas doses/reforços.
- Exportação CSV com seleção de campos e filtros existentes.
- Renovação automática da sessão JWT e tratamento compartilhado de erros da API.
- Navegação por perfil, cadastros, relatórios e painéis existentes.

Esses fluxos precisam ser ampliados; não devem ser substituídos por protótipos desconectados.

## Backlog do front-end

### 1. Nascimento e genealogia — RF-01, RF-02 e RF-03

**Já existe:** formulário de nascimento com bovino, ocorrência, data, peso e inseminação opcional; lista de nascimentos vinculados; abas separadas para Nascimento (inicial) e consulta interativa da árvore com quatro níveis, até bisavós.

**Construir no front:**

- Permitir informar pai e mãe diretamente quando não houver inseminação associada, sem duplicar opções conflitantes.
- Ampliar a árvore com dados completos até bisavós quando os vínculos correspondentes estiverem disponíveis na API.
- Permitir abrir a ficha dos animais da árvore quando houver identificação e rota de consulta disponível.
- Melhorar a seleção da mãe e do pai para que a pessoa consiga distinguir animais com nomes ou identificadores semelhantes.

**Preparar para integração posterior:**

- Combinar com o back-end como será representada a genealogia direta e a relação com uma inseminação.
- Confirmar como obter os ascendentes e como a API representa relações ausentes.
- Confirmar como o nascimento será associado a uma fêmea com prenhez confirmada.

**Preparado nesta etapa:** campos de pai/mãe sem inseminação na interface, com gravação bloqueada enquanto o endpoint não aceitar esses vínculos. A árvore também está pronta para ler pai/mãe diretos quando a API os fornecer.

**Aceite do front:** formulário e árvore funcionam visualmente com dados de demonstração identificados como tais; o salvamento só é apresentado como concluído após resposta de sucesso da API.

### 2. Desenvolvimento e marcos de pesagem — RF-04, RF-05 e RF-06; RN-07 e RN-08

**Já existe:** registro de pesagem, histórico e curva por animal.

**Construir no front:**

- Identificar pesagens como marco de 30 dias, 60 dias, desmame ou outra pesagem.
- Mostrar os marcos esperados na ficha/curva e indicar quais estão registrados ou pendentes.
- Criar estados visuais para crescimento dentro/fora do esperado, incluindo explicação acessível do alerta.
- Exibir dados insuficientes quando não houver histórico suficiente para avaliar um animal.

**Preparado nesta etapa:** marcos de 30 e 60 dias com a pesagem mais próxima; a tela explica que não classifica o crescimento sem limites oficiais. Desmame e avaliação zootécnica continuam dependentes de dados/regras da API.

**Preparar para integração posterior:**

- Definir com o back-end como o marco será armazenado ou calculado a partir da idade/data.
- Solicitar o resultado de avaliação do crescimento e a explicação/limites usados. Não inventar uma curva ou limite zootécnico no front.
- Manter o peso atual derivado do histórico, evitando criar um campo paralelo de peso no cadastro do animal.

**Aceite do front:** marcos e alertas ficam visíveis e compreensíveis; a interface diferencia “sem dados” de “fora do esperado”.

### 3. Sanidade e carência — RF-07, RF-08 e RF-09; RN-05 e RN-11

**Já existe:** lançamentos de vacinação e acompanhamento de próximas doses/reforços; atendimento veterinário com motivo em texto.

**Construir no front:**

- No detalhe/lista de vacinação, apresentar duração da carência e data prevista de liberação para ordenha.
- Mostrar um estado sanitário claro para o animal: em carência, liberado ou informação indisponível.
- Trocar o motivo veterinário livre por seleção de motivos predefinidos; manter observação livre apenas se validado como campo complementar.
- Apresentar próxima dose/reforço em formulários, histórico e painel com estados vencido, próximo e em dia.

**Preparado nesta etapa:** o formulário veterinário usa a lista de motivos predefinidos da API (`veterinary_occurrences/`) e envia a ocorrência selecionada. A interface de ordenha deixa explícito que carência e data de liberação não são fornecidas pela API atual; não calcula nem presume liberação.

**Preparar para integração posterior:**

- Confirmar com o back-end qual recurso fornece duração da carência, data de aplicação e data calculada de liberação.
- Obter a lista oficial de motivos veterinários e seus identificadores.
- Confirmar campos e resposta de próxima dose para que a interface não recalcule ou contradiga a API.

**Aceite do front:** as telas mostram o período e a liberação retornados pelo servidor; erro ou ausência de dados não é interpretado como liberação automática.

### 4. Reprodução — RF-10 a RF-15; RN-01 a RN-06

**Já existe:** registro/listagem de inseminação artificial e alertas estimados de ultrassom e parto.

**Construir no front:**

- Separar a seleção do tipo de procedimento: inseminação artificial ou transplante de embrião.
- Preparar formulário e histórico para os estados reprodutivos previstos: Vazia, Inseminada Artificialmente e Transplante de Embrião.
- Criar fluxo para registrar diagnóstico de prenhez (resultado, data e informações clínicas definidas pelo negócio).
- Criar fluxo visual de secagem para fêmeas com prenhez confirmada, mostrando datas e estado do período.
- Exibir lista de ultrassons pendentes e permitir abrir o fluxo de diagnóstico.
- Iniciar o registro de nascimento a partir de uma fêmea prenha, carregando a relação com a gestação/procedimento.
- Exibir bloqueios e motivos retornados pela API para idade ou parentesco, permitindo corrigir a seleção antes de reenviar.

**Preparado nesta etapa:** seleção do tipo de procedimento, rascunhos visuais de diagnóstico e secagem, indicação de que idade (13 meses) e parentesco são regras do servidor e exibição das rejeições recebidas. Transplante, diagnóstico e secagem não são enviados enquanto não houver endpoints/contratos.
O atalho para iniciar um nascimento a partir de uma prenhez também permanece indisponível até a API relacionar o nascimento à gestação confirmada.

**Preparar para integração posterior:**

- Confirmar os campos e estados aceitos para cada tipo de procedimento.
- O servidor deve validar idade mínima de 13 meses e parentesco até bisavô antes de persistir o procedimento.
- Confirmar como o sistema identifica inseminações com mais de 30 dias sem diagnóstico e como a prenhez é confirmada.
- Não inferir prenhez automaticamente após 90 dias. Exibir “aguardando diagnóstico” ou o estado oficial recebido da API.
- Confirmar os campos de diagnóstico, previsão de parto, secagem e associação do nascimento.

**Aceite do front:** não mostra prenhez como confirmada sem registro; erros de elegibilidade/parentesco são específicos e não deixam a operação parecer concluída.

### 5. Ordenha e produção — RF-16, RF-17 e RF-18; RN-09

**Já existe:** lançamento individual de produção, importação CSV e gráfico por período.

**Construir no front:**

- Trocar/expandir o formulário para registrar por estábulo, data e horários inicial/final.
- Selecionar o estábulo e, quando aplicável ao fluxo definido, os animais elegíveis para ordenha.
- Exibir animais impedidos por carência em uma lista separada, com motivo e data de liberação; não permitir selecioná-los para o lançamento.
- Apresentar indicadores de média de produção para últimos 10 dias, mês e ano.
- Exibir estados vazios quando não houver registros no intervalo.

**Preparado nesta etapa:** formulário com data, início e fim; médias diárias dos últimos 10 dias, mês atual e ano atual. O estábulo serve apenas como contexto de seleção: a API atual não o associa ao registro. A elegibilidade e a carência seguem sem confirmação do servidor.

**Preparar para integração posterior:**

- Confirmar como a ordenha será relacionada ao estábulo e se cada registro representa uma sessão, um animal ou ambos.
- Combinar campos e formatos dos horários, datas e produção.
- O back-end deve ser a fonte de elegibilidade de ordenha e da carência; o front não deve confiar apenas em um filtro local.
- Confirmar a definição da média (por animal, sessão, dia ou rebanho) antes de nomear o indicador.
- Preservar o fluxo CSV existente até validar compatibilidade com o novo formato.

**Aceite do front:** não oferece animal em carência como elegível; mostra o período e a definição da média usada.

### 6. Exportação configurável — RF-19 e RF-20

**Já existe:** CSV com escolha de campos, filtros e exportação de animais e históricos existentes.

**Construir no front:**

- Permitir ordenar os campos/colunas, por exemplo com controles de mover para cima/baixo.
- Permitir personalizar o nome exibido no cabeçalho de cada coluna.
- Permitir salvar um layout com nome, listar layouts salvos, aplicar um layout e atualizar/remover um layout conforme permissões.
- Exibir uma prévia do cabeçalho e dos dados antes de baixar.

**Preparado nesta etapa:** reordenação de campos, rótulos personalizados aplicados ao cabeçalho CSV, prévia do cabeçalho e layouts reutilizáveis. A persistência dos layouts é local ao navegador; sincronização entre usuários ainda depende da API.

**Preparar para integração posterior:**

- Definir se layouts são pessoais ou compartilhados e quais perfis podem gerenciá-los.
- Combinar o formato de persistência (identificador, nome, campos, ordem, rótulos e filtros).
- Confirmar como a API valida campos ainda disponíveis e como trata layouts incompatíveis após mudanças.

**Aceite do front:** ordem e rótulos escolhidos aparecem no arquivo; layout salvo pode ser recuperado sem perder os filtros selecionados.

### 7. Análise preditiva e apoio por IA — RF-21 a RF-24

**Já existe:** não foi localizada uma tela de análise preditiva dedicada. O menu “Reprodução & IA” atualmente direciona para reprodução e nascimento.

**Construir no front:**

- Criar uma área de análise com seleção do animal/período e ação explícita para solicitar uma análise.
- Apresentar resultados de desempenho e risco reprodutivo com explicação, data, dados considerados e estado de processamento/erro.
- Criar histórico consultável de análises anteriores.
- Exibir alertas de parentesco e tornar clara a ação recomendada/bloqueada.
- Na exportação, criar uma interface para descrever o layout desejado e revisar a sugestão de colunas antes de aplicá-la.
- Distinguir sugestão de IA de configuração salva ou regra confirmada pelo sistema.

**Preparado nesta etapa:** nova tela com seleção de animal/período, áreas para resultado explicável, alertas de parentesco, histórico e solicitação de sugestão de layout. As ações permanecem indisponíveis até existir API; não há resultados fabricados.

**Preparar para integração posterior:**

- Definir contratos da análise, histórico, explicações e sugestões de layout; confirmar limites de tamanho e estados de processamento.
- Confirmar quais dados históricos (peso, ECC e ocorrências) podem ser usados e como são identificados.
- Resultados de IA precisam trazer explicação e origem; o front não deve fabricar previsões nem usar uma resposta genérica como sucesso.
- O alerta de parentesco e o bloqueio do procedimento devem ser confirmados pela API.

**Aceite do front:** cada resultado mostra quando foi gerado, a explicação disponível e eventual falha; sugestões não são persistidas sem confirmação do usuário.

### 8. Tarefas, notificações e acesso — RF-25 e RF-26; RN-12

**Já existe:** telas e rotas de administrador/operador, relatórios, cadastros e cartões de lembretes no painel.

**Verificar e completar no front:**

- Confirmar com a equipe se os cartões de tarefas do painel são dados reais da API ou resumos calculados no cliente.
- Se não houver tela dedicada, criar lista de tarefas/notificações com estados não lida, lida, vencida e concluída conforme o contrato do back-end.
- Conferir que o Operador encontra lançamentos de campo, consulta do rebanho, saúde e tarefas sem receber ações administrativas indevidas.
- Conferir que menus, rotas e ações da tela refletem os perfis sem tratar a guarda do front como autorização de segurança.

**Preparar para integração posterior:**

- Definir endpoints, estados, filtros e ações de tarefa/notificação.
- O back-end deve validar permissões em cada operação; o front apenas apresenta as capacidades devolvidas/definidas para o perfil.

**Aceite do front:** tarefas/notificações exibem dados da API e atualizam seu estado após confirmação do servidor; tentativa sem permissão apresenta erro claro.

### 9. Qualidade transversal — RNF-01, RNF-02 e RNF-06

- Revisar responsividade das telas novas em celular, tablet e desktop.
- Manter padrão visual e componentes compartilhados para formulários, alertas, tabelas, modais e estados vazios.
- Garantir mensagens específicas para validação por campo, falta de permissão, sessão expirada, indisponibilidade da API e conflitos de dados.
- Preservar dados digitados após erros corrigíveis.
- Testar navegação por teclado, rótulos de formulário, foco em modais e anúncios de carregamento/erro.
- Validar que renovação de sessão não perde formulário nem repete gravação já concluída.

## Etapas sugeridas

### Etapa A — Front-end sem dependência de endpoints novos

1. Manter as telas integradas existentes e preparar as áreas de marcos de desenvolvimento, reprodução, ordenha, análise e motivos veterinários sem declarar gravações/decisões que a API não confirma.
2. Preservar dados vazios/indisponíveis como tais; não usar previsões ou fixtures que possam parecer dados reais.
3. Continuar revisão de responsividade, acessibilidade, estados de carregamento/vazio/erro e navegação ao homologar cada tela.

### Etapa B — Contratos e integração com o back-end

1. Revisar a lista “Preparar para integração posterior” de cada módulo com a equipe do back-end.
2. Fechar endpoints, nomes/tipos de campos, relacionamentos, estados, paginação, validações e mensagens de erro.
3. Trocar fixtures por chamadas da API e remover qualquer comportamento de demonstração do fluxo de produção.
4. Confirmar no servidor regras de idade, parentesco, prenhez, carência, elegibilidade, perfis e persistência de layouts.

### Etapa C — Homologação

1. Testar fluxos completos com dados reais de teste e perfis Administrador/Operador.
2. Verificar regras de bloqueio e que a interface apresenta a resposta real da API.
3. Testar celular, erros de rede, sessão renovada, campos inválidos e ausência de dados.
4. Atualizar documentação e registro de validações com o estado efetivamente integrado.

## Checklist de acompanhamento

- [ ] Nascimento: campos de pai/mãe diretos preparados; persistência depende da API.
- [x] Genealogia: interface consultável até bisavós, com ascendência ausente identificada; integração completa depende dos vínculos fornecidos pela API.
- [x] Desenvolvimento: marcos visuais de 30/60 dias, curva e explicação; desmame e limite zootécnico dependem da API.
- [ ] Sanidade: carência e data de liberação dependem da API.
- [x] Sanidade: motivo veterinário selecionado de lista predefinida disponível pela API.
- [ ] Reprodução: UI de tipo de procedimento, diagnóstico e secagem preparada; persistência/estado clínico depende da API.
- [x] Reprodução: interface pronta para exibir as validações de idade e parentesco devolvidas pelo servidor.
- [ ] Ordenha: data/horários e médias diárias de 10 dias/mês/ano prontos; estábulo persistido e elegibilidade dependem da API.
- [x] Exportação: ordem, rótulos personalizados e layouts locais salvos/reutilizáveis; sincronização com servidor pendente.
- [ ] IA: tela para análise explicável, histórico, alertas e sugestão de layout criada; resultados e ações dependem da API.
- [ ] Operação: confirmar tarefas/notificações reais e cobertura por perfil.
- [ ] Qualidade: responsividade, acessibilidade, erros específicos e integração homologada.

## Referências

- TAP v2.0: requisitos funcionais RF-01 a RF-26, não funcionais RNF-01 a RNF-10 e regras RN-01 a RN-13.
- Template da 3ª entrega: requisitos e regras do Apêndice B; itens de refinamento de modelo na página 17.
- Estado atual do front: `frontend/src/views/`, `frontend/src/router/index.js` e `frontend/src/services/api.js`.
