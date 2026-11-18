# Configuração para CPU fraca e diagnóstico de travamentos

Um Resource Pack pode reduzir custos de alguns recursos visuais, mas não controla o carregamento nem a geração dos chunks.

## Ponto de partida

| Opção | Valor |
|---|---:|
| Distância de renderização | 4 chunks |
| Distância de simulação | 4 chunks |
| Gráficos | Simples |
| Visuais Vibrantes | Desativados |
| Folhas/iluminação sofisticadas | Desativadas, se disponíveis |
| Nuvens e efeitos de céu | Desativados, se disponíveis |
| Limite de FPS | 30 estáveis |

Se 4 chunks ficar estável, teste 6 chunks de renderização mantendo simulação em 4. Não aumente as duas opções ao mesmo tempo.

A distância de renderização define quantos chunks o cliente desenha. A distância de simulação determina onde entidades, plantas, líquidos e outras mecânicas continuam atualizando. Consulte a documentação da Microsoft sobre Render Distance, Simulation Distance e Ticking Areas:
https://learn.microsoft.com/en-us/minecraft/creator/documents/simulationrenderdistanceguide?view=minecraft-bedrock-stable

## Identifique o tipo de travamento

### Ao entrar em terreno nunca visitado
Pode ser geração de terreno, leitura/gravação do mundo e preparação dos chunks. O LowMine não substitui o gerador. Teste 4 chunks, avance mais devagar e deixe o terreno carregar. Mantenha espaço livre no SSD e feche tarefas pesadas em segundo plano.

### Ao olhar para florestas
Pode ser custo gráfico da geometria, transparência, sombras ou uma cena densa. O LowMine reduz as imagens de vegetação para 8×8, mas não remove os modelos/planos de vegetação vanilla.

### Perto de entidades, fazendas ou redstone
Pode ser custo de simulação, pathfinding, líquidos e atualizações de blocos. Mantenha a simulação em 4 e teste uma área com menos entidades.

A Microsoft explica que entidades podem continuar executando comportamentos mesmo fora da visão quando seus chunks permanecem carregados. Consulte:
https://learn.microsoft.com/en-us/minecraft/creator/documents/practices/improvingperformanceandresourceusage?view=minecraft-bedrock-stable

### Em área já carregada
Investigue memória/RAM, armazenamento, entidades, outros pacotes ativos e possíveis problemas no mundo. Faça cópia de segurança antes de alterar o mundo.

## Teste controlado
1. Faça uma cópia do mundo.
2. Anote a versão exata do Bedrock, resolução e configurações.
3. Teste sem LowMine com renderização 4 e simulação 4.
4. Repita com LowMine exatamente no mesmo ponto.
5. Teste uma área já carregada e depois terreno novo.
6. Registre se trava ao gerar terreno, ao olhar para vegetação ou perto de entidades.
7. Compare FPS médio e frame time, não apenas um número instantâneo.

## Limites
LowMine não gera chunks antecipadamente, não altera cache/streaming, não controla distâncias e não injeta código Rust no cliente. Neblina e texturas não são culling universal.
