# Limites do renderizador e otimizações possíveis

Este documento separa alterações que um pacote de recursos consegue fazer das que pertencem ao motor do Minecraft Bedrock.

## Recomendações de desenvolvimento

A documentação da Microsoft recomenda:
- Reduzir dimensões de texturas e evitar espaço vazio desperdiçado.
- Agrupar texturas pequenas em atlas quando o tipo de conteúdo permite.
- Evitar arquivos e variantes desnecessários.
- Manter entidades e partículas em quantidades e complexidade controladas.
- Testar add-ons em dispositivos modestos desde o começo.

A Microsoft explica que texturas normalmente são carregadas sem compressão na memória; uma textura 1024×1024 pode ocupar 16 vezes o espaço de uma 256×256. Ela também recomenda manter menos de 800 texture handles em add-ons e alerta que muitos arquivos aumentam o custo de carregamento.

Fontes:
- [Melhorar desempenho e uso de recursos — Microsoft Learn](https://learn.microsoft.com/en-us/minecraft/creator/documents/practices/improvingperformanceandresourceusage?view=minecraft-bedrock-stable)
- [Orçamentos de textura — Microsoft Learn](https://learn.microsoft.com/en-us/minecraft/creator/documents/texturebudgets?view=minecraft-bedrock-stable)

A contagem de PNGs não é igual à quantidade de texture handles: texturas de blocos podem ser agrupadas em atlas pelo jogo.

## Distância de renderização e simulação

A distância de renderização define quantos chunks o cliente tenta desenhar. A distância de simulação define onde entidades, plantas, líquidos e outras mecânicas continuam atualizando. A distância de simulação também custa CPU porque envolve a lógica do jogo.

Fonte: [Distância de simulação, renderização e ticking areas — Microsoft Learn](https://learn.microsoft.com/en-us/minecraft/creator/documents/simulationrenderdistanceguide?view=minecraft-bedrock-stable).

Um resource pack não consegue mudar essas opções.

## Neblina não é culling

Neblina mistura a cena com uma cor à distância. Ela pode esconder visualmente o horizonte, mas não ordena ao RenderDragon que descarte todos os chunks depois do limite.

Ela não:
- Esconde apenas objetos atrás da câmera.
- Garante que blocos abaixo do solo deixem de ser processados.
- Substitui frustum culling, occlusion culling, geração de chunks ou distância de renderização.

## Block Culling

O Block Culling do Bedrock é voltado a faces de geometria de blocos personalizados que ficam cobertas por blocos vizinhos. Ele não é um interruptor global para toda a geometria vanilla ou para tudo que está atrás do jogador.

Referência: [Bedrock Wiki — Block Culling](https://wiki.bedrock.dev/blocks/block-culling).

## Geometria e texturas de vegetação

Um resource pack pode substituir imagens vanilla pelos mesmos nomes e caminhos. Isso não significa que ele possa apagar os planos de geometria nativos da grama ou samambaia.

O LowMine v0.4.0 troca oito texturas por versões 16×16 mais esparsas. Isso reduz a densidade de pixels opacos das imagens, mas não remove a geometria dos blocos e não garante ganho de FPS.

Referências:
- [Substituir recursos vanilla — Microsoft Learn](https://learn.microsoft.com/en-us/minecraft/creator/documents/overwritingassets?view=minecraft-bedrock-stable)
- [Mapeamento de texturas — Mojang Bedrock Samples](https://github.com/Mojang/bedrock-samples/blob/main/resource_pack/textures/terrain_texture.json)
- [Definições de blocos — Mojang Bedrock Samples](https://github.com/Mojang/bedrock-samples/blob/main/resource_pack/blocks.json)

## RenderDragon e Rust

Um .mcpack é um pacote de recursos, não um plugin nativo do cliente. Ele não consegue inserir código Rust no renderizador nem substituir o RenderDragon.

Rust pode ser útil em ferramentas externas do LowMine:
- Analisar dimensões e duplicatas de texturas.
- Comparar tamanho de pacotes e arquivos.
- Construir e verificar pacotes.
- Analisar relatórios de benchmark.

Isso não vira culling de cliente por meio de um pacote de recursos.

## Método de otimização do LowMine

1. Reduzir efeitos que o próprio pacote controla.
2. Reduzir imagens grandes e arquivos de textura desnecessários.
3. Remover arquivos duplicados de subpacotes.
4. Preservar legibilidade e estados de seleção da interface.
5. Comparar o jogo sem LowMine e com LowMine na mesma posição, resolução, dispositivo e distâncias.
6. Registrar FPS médio e estabilidade de frame time; não alegar ganho com base apenas no tamanho do ZIP.
