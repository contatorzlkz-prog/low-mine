# Auditoria técnica — LowMine Equilibrado 8x

## Base reproduzível
A compilação v0.6.2 parte de LowMine-Equilibrado-8x-v0.5.0.mcpack, gerado pelo construtor estável. A base contém 38 texturas de bloco em 8×8, arquivos de UI, recursos de água/sombras/partículas e créditos.

## Delta v0.6.2
- Troncos laterais e topos recebem arte 8×8 com quatro tons por paleta e veios irregulares.
- Sete conjuntos de armadura recebem dois mapas UV 64×32 e quatro ícones 16×16 cada.
- Ícones de itens de PvP incluem sete espadas, arco, besta, flecha e tridente, todos em 16×16 derivados de arte 8×8.
- A interface da base é preservada: inventário desktop/mobile, baú pequeno/grande, Ender, shulker e barril.
- O validador verifica dimensões de texturas, existência das armaduras, manifesto 0.6.2, arquivos de interface e integridade do ZIP.
- O GitHub Actions imprime tamanho, contagem de entradas e SHA-256 do artefato construído.

## Pipeline anterior
O pipeline v0.6.0 foi retirado da compilação porque seu bundle comprimido atual falha ao descompactar. As afirmações anteriores sobre 137 texturas 8×8 não se aplicam ao artefato v0.6.2 compilado a partir da base reproduzível 0.5.0.

## Limites
A validação não inicia Minecraft e não mede FPS. Ainda é necessário importar no Bedrock, testar visualmente troncos/armaduras/UI e comparar FPS/frame time em cenas equivalentes.

As texturas de bloco mantidas têm 8×8 pixels. Mapas de armadura usam 64×32 para respeitar o UV do modelo Bedrock.
