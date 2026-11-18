# Configuração para CPU fraca e diagnóstico de travamentos

Este guia separa geração de terreno, renderização e simulação. Um Resource Pack não controla o carregador de chunks nem muda as opções internas do mundo.

## Ponto de partida

Para um PC modesto, comece com:

| Opção | Valor inicial |
|---|---:|
| Distância de renderização | 4 chunks |
| Distância de simulação | 4 chunks |
| Gráficos | Simples |
| Visuais Vibrantes | Desativados |
| Folhas/iluminação sofisticadas | Desativadas |
| Nuvens e efeitos de céu | Desativados |
| Limite de FPS | 30 estáveis |

Se 4 chunks ficar estável e o jogo continuar fluido, experimente 6 chunks de renderização, mantendo simulação em 4. Não aumente renderização e simulação ao mesmo tempo.

A distância de renderização define quantos chunks o cliente desenha; a distância de simulação define onde entidades, plantas, líquidos e outras mecânicas atualizam. Consulte a documentação da Microsoft sobre Render Distance, Simulation Distance e Ticking Areas:
https://learn.microsoft.com/en-us/minecraft/creator/documents/simulationrenderdistanceguide?view=minecraft-bedrock-stable

## Descubra onde trava

### Travada ao entrar em terreno nunca visitado

Pode ser geração de terreno, leitura/gravação do mundo e preparação de chunks. Um resource pack não substitui o gerador. Teste renderização em 4 chunks e avance mais devagar, deixando o terreno carregar. Mantenha espaço livre no SSD e feche tarefas pesadas em segundo plano.

### FPS cai ao olhar para florestas

Pode ser custo gráfico de geometria, transparência, sombras ou cena muito densa. O LowMine simplifica as imagens de vegetação e reduz alguns efeitos, mas não remove os planos/vértices dos modelos vanilla.

### Congela perto de mobs, aldeias, fazendas ou redstone

Pode ser custo de simulação, pathfinding, entidades, líquidos e atualizações de bloco. Mantenha a simulação em 4 e teste uma área com menos entidades.

A Microsoft observa que entidades podem continuar executando comportamentos mesmo fora da visão ou atrás de blocos quando estão em chunks carregados. Reduzir quantidade de entidades e trabalho de IA pode ser mais importante que trocar a textura. Consulte:
https://learn.microsoft.com/en-us/minecraft/creator/documents/practices/improvingperformanceandresourceusage?view=minecraft-bedrock-stable

### Travamento também em um lugar já carregado

Investigue memória/RAM, disco, pacotes adicionais, entidades e possíveis problemas do mundo. Faça uma cópia de segurança antes de testar alterações.

## Como testar sem confundir resultados

1. Faça uma cópia do mundo.
2. Anote versão exata do Bedrock, resolução e configurações.
3. Teste sem LowMine com renderização 4 e simulação 4.
4. Repita com LowMine exatamente no mesmo ponto.
5. Teste uma área já carregada e depois terreno novo.
6. Registre se trava ao gerar terreno, ao olhar para vegetação ou perto de entidades.
7. Compare FPS médio e frame time, não apenas um número instantâneo.

## O que o LowMine faz e não faz

O LowMine reduz o tamanho de 38 texturas de bloco para 8×8, controla 14 emissores incluídos, simplifica alguns recursos visuais e oferece interface própria. Ele não:
- Gera chunks antecipadamente.
- Controla render distance ou simulation distance.
- Altera cache/streaming do jogo.
- Faz culling universal atrás da câmera.
- Injeta código Rust no cliente Bedrock.
