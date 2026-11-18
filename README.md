# LowMine Equilibrado 8x v0.6.2

<p align="center">
  <a href="https://github.com/contatorzlkz-prog/low-mine/releases/download/lowmine-v0.6.2/LowMine-Equilibrado-8x-v0.6.2.mcpack">
    <img src="https://img.shields.io/badge/⬇%20BAIXAR%20LOWMINE-.MCPACK-2ea44f?style=for-the-badge" alt="Baixar LowMine Equilibrado 8x">
  </a>
</p>

**LowMine Equilibrado 8x v0.6.2** é um Resource Pack para Minecraft Bedrock. Esta compilação parte da base reproduzível v0.5.0, mantendo suas 38 texturas de bloco autorais em 8×8, a interface translúcida e os recursos existentes. A atualização redesenha os troncos incluídos com veios irregulares e paletas compactas e adiciona sete conjuntos de armaduras.

A interface transparente preservada inclui inventário desktop, inventário mobile e telas de contêineres: baú pequeno/grande, baú do End, shulker e barril. Os blocos existentes continuam em 8×8. Mapas de armadura usam 64×32 porque essa é a dimensão UV esperada pelo modelo Bedrock; ícones de armadura usam pixel art 8×8 ampliada por nearest-neighbor para 16×16.

> A validação é estrutural. Ganho de FPS e comportamento visual precisam ser comparados dentro do Minecraft, no mesmo mundo, aparelho e configurações. Texturas pequenas reduzem a memória das imagens substituídas, mas não reduzem geração de chunks ou simulação.

## O que mudou

- **Troncos redesenhados em 8×8**: veios interrompidos e levemente curvos, pequenas marcas de nó e quatro tons por espécie, sem listras verticais contínuas.
- **Topo dos troncos**: anéis quadrados compactos com centro levemente deslocado.
- **Sete conjuntos de armaduras**: couro, malha, ferro, ouro, diamante, netherita e cobre.
- Mapas UV das armaduras em **64×32**, com transparência e detalhes de placa/costura.
- Ícones de capacete, peitoral, calças e botas em pixel art 8×8, exportados em 16×16 para o atlas Bedrock.
- **Itens visuais de PvP**: sete espadas por material, animações estáticas do arco e da besta, flechas e tridente, com arte 8×8 ampliada por nearest-neighbor.
- **Interface transparente mantida** para inventário desktop, pocket/mobile e contêineres incluídos no pack.
- As 38 texturas de bloco 8×8 da base 0.5.0 são preservadas.
- Sem shaders PBR extras, scripts executados no jogo, loops ou partículas adicionais.

## Interface

A atualização preserva os arquivos inventory_screen.json, inventory_screen_pocket.json e chest_screen.json, além dos registros em _ui_defs.json. Os overrides de contêiner incluem baús pequeno e grande, baú do End, shulker e barril.

## Instalação e teste

1. Baixe LowMine-Equilibrado-8x-v0.6.2.mcpack pela seção Releases.
2. Abra com Minecraft Bedrock e ative o pack.
3. Deixe somente um perfil LowMine ativo.
4. Confira troncos de diferentes espécies, armaduras equipadas, ícones, inventário e baús.
5. Compare com e sem LowMine na mesma cena, resolução e distâncias.

## Limites e compatibilidade

Esta compilação usa a base reproduzível 0.5.0. O pipeline antigo de geração 0.6.0 possui um bundle-fonte comprimido inválido e foi retirado do caminho de compilação desta atualização; por isso, a expansão de 137 texturas que aparecia na documentação anterior não faz parte deste artefato. As 38 texturas 8×8 da base são mantidas.

As folhas mantêm a geometria e o número de planos do Minecraft. Um Resource Pack puro não faz folhas caírem automaticamente de todas as árvores; isso exigiria lógica/entidades/Behavior Pack.

A resolução 8×8 reduz a área das imagens substituídas, mas não altera geometria, culling, geração de chunks ou simulação. Não há promessa de FPS sem medição dentro do Bedrock.

## Autoria e licenças

As novas paletas e texturas de troncos, os mapas de armaduras e os ícones desta atualização são criações LowMine. Permanecem os créditos e a licença CC BY-NC 3.0 do material adaptado já presente na base; consulte CREDITOS.md e CREDITOS.txt.

Minecraft é marca da Mojang/Microsoft; LowMine não é afiliado nem endossado por elas.
