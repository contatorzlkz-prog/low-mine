# Limites do renderizador e técnicas reais

## Recomendações de quem desenvolve para Bedrock

A documentação da Microsoft recomenda reduzir dimensões e quantidade de texturas desnecessárias, controlar texture handles, manter contagem de arquivos enxuta e evitar excesso de entidades, lógica de IA e partículas. Ela recomenda menos de 800 texture handles para add-ons; pacotes também devem evitar excesso de arquivos. Texturas de blocos podem ser agrupadas em atlas, portanto PNGs não correspondem diretamente a texture handles.

Fonte: Melhorar desempenho e uso de recursos — Microsoft Learn:
https://learn.microsoft.com/en-us/minecraft/creator/documents/practices/improvingperformanceandresourceusage?view=minecraft-bedrock-stable

O LowMine tem 72 arquivos compactados no pacote, 50 imagens PNG e 38 texturas de bloco em 8×8. Isso é uma contagem de arquivos/pixels, não um benchmark de FPS nem uma contagem de handles GPU.

## Por que as texturas 8×8 fazem sentido

Uma imagem 8×8 tem 64 texels; uma imagem 16×16 tem 256 texels. Mantendo o mesmo formato, 8×8 contém um quarto da área de pixels. O LowMine aplica isso apenas às 38 texturas modificadas; não reduz todas as texturas vanilla do jogo e não elimina geometria de blocos.

Fontes oficiais:
- Substituir recursos vanilla — Microsoft Learn:
  https://learn.microsoft.com/en-us/minecraft/creator/documents/overwritingassets?view=minecraft-bedrock-stable
- Mapeamento de texturas — Mojang Bedrock Samples:
  https://github.com/Mojang/bedrock-samples/blob/main/resource_pack/textures/terrain_texture.json
- Definições de blocos — Mojang Bedrock Samples:
  https://github.com/Mojang/bedrock-samples/blob/main/resource_pack/blocks.json

## Partículas e limites por rajada

O FPS Optimizer usa controles Molang para quantidade e número máximo de partículas por emissão. O LowMine adaptou 14 definições, alterou o namespace para lowmine: e usa um padrão de 50% com limite 6. O campo num_particles de minecraft:emitter_rate_instant aceita número ou Molang, conforme a documentação oficial:
https://learn.microsoft.com/en-us/minecraft/creator/reference/content/particlesreference/examples/particlecomponents/emitter_rate_instant?view=minecraft-bedrock-stable

O limite só atinge emissores fornecidos/substituídos pelo pacote. Não controla todas as partículas nativas do Minecraft.

## Scripts: por que não colocamos loops no pacote

A versão 0.5.0 é apenas um Resource Pack. Não possui Behavior Pack, JavaScript, TypeScript ou .mcfunction. Isso evita adicionar lógica recorrente ao mundo.

Se um futuro projeto precisar de scripts, a Microsoft recomenda medir com profiler, evitar operações caras repetidas a cada tick e distribuir tarefas periódicas em intervalos, em vez de executar tudo no mesmo tick.

Fonte: Performance in Scripting — Microsoft Learn:
https://learn.microsoft.com/en-us/minecraft/creator/documents/scripting/script-performance?view=minecraft-bedrock-stable

A Microsoft também alerta que comportamentos de entidades podem continuar ativos mesmo quando elas estão atrás de blocos ou fora da visão, desde que o chunk esteja carregado. Diminuir entidades e pathfinding pode ser mais relevante para CPU que uma textura mais simples.

## Neblina, Block Culling e RenderDragon

- Neblina é mistura visual por distância; não faz o renderizador descartar toda a geometria depois dela.
- Block Culling trata faces escondidas de modelos de blocos personalizados; não é um culling global para o mundo vanilla.
- RenderDragon pertence ao cliente Bedrock. Um .mcpack não injeta Rust nem substitui o renderizador.

## Água e sombras

O pacote adapta água sem cáusticas e ondas e sombras blocadas com texel 16 do FPS Optimizer. São configurações visuais. O efeito real depende da versão, do dispositivo e do modo gráfico que oferece suporte a esses recursos; não afirmamos que elas aumentem FPS em todo hardware.

## Método de teste

Compare sem LowMine e com LowMine na mesma versão do jogo, dispositivo, mundo, posição, resolução, distância de renderização e simulação. Separe geração de terreno novo de FPS em uma área carregada. Registre FPS médio e frame time.
