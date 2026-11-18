# LowMine Equilibrado 8x

<p align="center">
  <a href="https://github.com/contatorzlkz-prog/low-mine/releases/download/lowmine-v0.6.0/LowMine-Equilibrado-8x-v0.6.0.mcpack">
    <img src="https://img.shields.io/badge/⬇%20BAIXAR%20LOWMINE-.MCPACK-2ea44f?style=for-the-badge" alt="Baixar LowMine Equilibrado 8x">
  </a>
</p>

**LowMine Equilibrado 8x v0.6.0** é um Resource Pack independente para Minecraft Bedrock. Esta atualização redesenha a arte em pixel art 8×8, amplia a cobertura de vegetação e madeira, melhora as folhas com transparência recortada e variantes opacas e adiciona nuvens e sol compactos.

A identidade visual reutiliza formas-base entre espécies e aplica paletas próprias por árvore. As texturas de bloco substituídas usam 8×8 pixels; céu usa imagens 32×32. Não há PBR extra, scripts, loops ou Behavior Pack.

> A validação é estrutural. Ganho de FPS e comportamento visual precisam ser comparados dentro do Minecraft, no mesmo mundo, aparelho e configurações. Texturas menores podem reduzir a memória ocupada pelas imagens substituídas, mas não reduzem geração de chunks ou simulação.

## O que mudou

- **137 texturas de bloco 8×8**: grama, solo, pedra, areia, cascalho, flores, brotos, samambaias, arbustos, cipós, bambu, vegetação aquática, musgo e serapilheira.
- **Folhas e árvores redesenhadas**: carvalho, abeto, bétula, selva, acácia, carvalho escuro, mangue, cerejeira, azaleia, pale oak e álamos.
- Folhas com alpha recortado e variantes opacas correspondentes.
- Troncos, topos, madeira descascada e tábuas com paletas por espécie.
- Nuvens e sol em **32×32**, sem animação, brilho extra ou partículas.
- Partículas padrão reduzidas para **30%**, limite **4 por emissão** nos emissores substituídos.
- Água sem cáusticas/ondas; sombras blocadas mantidas conforme o modo gráfico.
- Um perfil; zero scripts no jogo.

### Auditoria estática

| Verificação | Resultado |
|---|---:|
| Entradas no MCpack | 170 |
| JSON válidos | 21 |
| PNG | 147 |
| Texturas de bloco 8×8 | 137 |
| Nuvens/sol | 2 × 32×32 |
| Definições de partículas | 14 |
| Scripts incluídos | 0 |
| Tamanho | 60.902 bytes |

SHA-256: `a10c3d4195e901740d90160bd058d71a279e66c67828a4166c4a918c9a880660`

Validação não inicia Minecraft nem mede FPS.

## Instalação e teste

1. Baixe `LowMine-Equilibrado-8x-v0.6.0.mcpack`.
2. Abra com Minecraft Bedrock e ative o pack.
3. Deixe somente um perfil LowMine ativo.
4. Teste florestas, folhas, troncos, plantas, água, céu, inventário e baús.
5. Compare com e sem LowMine na mesma cena, resolução e distâncias.

Comece com 4 chunks de renderização e 4 de simulação. O Resource Pack não controla geração de chunks, entidades ou RenderDragon.

## Limites visuais

As folhas possuem recorte transparente, mas a geometria e o número de planos continuam sendo os do Minecraft. Um Resource Pack puro não faz folhas caírem automaticamente de todas as árvores; isso exigiria lógica/entidades/Behavior Pack e não faz parte deste pacote leve.

A arte da espada e dos itens de combate permanece sem alteração nesta versão.

## Autoria e licenças

A arte de 137 texturas 8×8, paletas, ícone, nuvens e sol é LowMine. Permanecem 14 definições de partículas, água e sombras adaptadas do FPS Optimizer v2.9.2, de XiaoCraft, sob CC BY-NC 3.0. Créditos em `CREDITOS.md` e `CREDITOS.txt`.

PotatoCraft 8x, Embeddium Optimizer e Vanilla × Optimizer foram apenas referências técnicas, sem cópia de arquivos. A condição não comercial da licença CC BY-NC 3.0 deve ser respeitada. Minecraft é marca da Mojang/Microsoft; LowMine não é afiliado nem endossado por elas.
