# LowMine Equilibrado 8x v0.6.1

<p align="center">
  <a href="https://github.com/contatorzlkz-prog/low-mine/releases/download/lowmine-v0.6.1/LowMine-Equilibrado-8x-v0.6.1.mcpack">
    <img src="https://img.shields.io/badge/⬇%20BAIXAR%20LOWMINE-.MCPACK-2ea44f?style=for-the-badge" alt="Baixar LowMine Equilibrado 8x">
  </a>
</p>

**LowMine Equilibrado 8x v0.6.1** é um Resource Pack independente para Minecraft Bedrock. A base mantém as texturas autorais de blocos em 8×8 e agora refina os troncos com veios irregulares, paletas compactas e cortes com anéis de madeira. Sete conjuntos de armaduras recebem arte pixelada própria.

A interface transparente da versão anterior é preservada: inventário desktop, inventário mobile e telas de contêineres (baú pequeno/grande, baú do End, shulker e barril). As texturas de bloco continuam em 8×8; os mapas de armadura usam 64×32 porque essa é a dimensão UV esperada pelo modelo Bedrock. Os ícones de armadura são pixel art 8×8 ampliada por nearest-neighbor para 16×16.

> A validação é estrutural. Ganho de FPS e comportamento visual precisam ser comparados dentro do Minecraft, no mesmo mundo, aparelho e configurações. Texturas menores podem reduzir memória das imagens substituídas, mas não reduzem geração de chunks ou simulação.

## O que mudou

- **Troncos redesenhados em 8×8**: veios interrompidos e levemente curvos, pequenas marcas de nó e paletas de quatro tons por espécie, sem listras verticais contínuas.
- **Topo dos troncos**: anéis quadrados compactos com centro levemente deslocado, mantendo leitura de madeira cortada em 8×8.
- **Sete conjuntos de armaduras**: couro, malha, ferro, ouro, diamante, netherita e cobre.
- Mapas UV das armaduras em **64×32**, com transparência preservada e detalhes de placa/costura adequados a cada material.
- Ícones de capacete, peitoral, calças e botas em pixel art 8×8, exportados em 16×16 para o atlas Bedrock.
- **Interface transparente mantida** para inventário desktop, pocket/mobile e todos os contêineres incluídos na UI do pack.
- As 137 texturas de bloco 8×8, folhas recortadas, vegetação, nuvens/sol e perfil de partículas da v0.6.0 continuam como base.
- Sem shaders PBR extras, scripts executados no jogo, loops ou partículas adicionais.

## Interface

A transparência é mantida nas telas inventory_screen.json, inventory_screen_pocket.json e chest_screen.json. Os overrides de contêiner incluem baús pequeno e grande, baú do End, shulker e barril. A atualização preserva esses arquivos e os registros em _ui_defs.json.

## Instalação e teste

1. Baixe LowMine-Equilibrado-8x-v0.6.1.mcpack pela seção Releases.
2. Abra com Minecraft Bedrock e ative o pack.
3. Deixe somente um perfil LowMine ativo.
4. Confira troncos de diferentes espécies, armaduras equipadas, ícones, inventário e baús.
5. Compare com e sem LowMine na mesma cena, resolução e distâncias.

Comece com 4 chunks de renderização e 4 de simulação. O Resource Pack não controla geração de chunks, entidades ou RenderDragon.

## Limites visuais

As folhas mantêm a geometria e o número de planos do Minecraft. Um Resource Pack puro não faz folhas caírem automaticamente de todas as árvores; isso exigiria lógica/entidades/Behavior Pack e não faz parte deste pacote leve.

A resolução 8×8 reduz a área das imagens substituídas, mas não altera geometria, culling, geração de chunks ou simulação. Não há promessa de FPS sem medição dentro do Bedrock.

## Autoria e licenças

As novas paletas e texturas de troncos, os mapas de armaduras e os ícones desta atualização são criações LowMine. Permanecem 14 definições de partículas, água e sombras adaptadas do FPS Optimizer v2.9.2, de XiaoCraft, sob CC BY-NC 3.0. Créditos em CREDITOS.md e CREDITOS.txt.

PotatoCraft 8x, Embeddium Optimizer e Vanilla × Optimizer foram apenas referências técnicas, sem cópia de arquivos. A condição não comercial da licença CC BY-NC 3.0 deve ser respeitada. Minecraft é marca da Mojang/Microsoft; LowMine não é afiliado nem endossado por elas.
