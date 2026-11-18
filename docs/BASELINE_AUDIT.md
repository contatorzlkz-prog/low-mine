# Auditoria técnica — LowMine Equilibrado 8x

## Registro histórico v0.6.0
A auditoria estática da versão 0.6.0 verificou manifesto formato 3, ZIP/CRC, 21 arquivos JSON, UI, partículas, água, sombras, créditos, dimensões e ausência de scripts. O pacote histórico possuía 137 texturas de bloco em 8×8 e duas texturas ambientais 32×32.

O tamanho e o SHA-256 registrados na auditoria original pertencem exclusivamente ao artefato v0.6.0 e não devem ser usados para identificar a nova versão.

## Delta v0.6.1
- Troncos laterais e topos recebem arte 8×8 com quatro tons por paleta e veios irregulares.
- Sete conjuntos de armadura recebem dois mapas UV 64×32 e quatro ícones 16×16 cada.
- A interface anterior é preservada: inventário desktop/mobile, baú pequeno/grande, Ender, shulker e barril.
- A validação nova verifica as dimensões das texturas, a existência das armaduras, o manifesto 0.6.1, os arquivos de interface e a integridade do ZIP.
- O GitHub Actions imprime tamanho, contagem de entradas e SHA-256 do artefato construído.

## Limites
A validação não inicia Minecraft e não mede FPS. Ainda é necessário importar no Bedrock, testar visualmente troncos/armaduras/UI e comparar FPS/frame time em cenas equivalentes.

Texturas de bloco 8×8 reduzem a área de pixels das imagens substituídas, mas não alteram geometria, planos de vegetação, geração de chunks ou simulação. Mapas de armadura usam 64×32 para respeitar o UV do modelo Bedrock.
