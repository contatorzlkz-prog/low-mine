# Auditoria técnica — LowMine Equilibrado 8x v0.6.0

## Escopo
Auditoria estrutural do ZIP, manifesto, JSON, partículas, UI, água, sombras, créditos e dimensões. Não inicia Minecraft nem mede FPS.

## Identidade
- Arquivo: `LowMine-Equilibrado-8x-v0.6.0.mcpack`
- Tamanho: 60.902 bytes
- SHA-256: `a10c3d4195e901740d90160bd058d71a279e66c67828a4166c4a918c9a880660`
- Manifesto formato 3; versão 0.6.0
- UUID cabeçalho: `21ca0070-fc45-5c56-8812-4b1cda3172a8`
- UUID módulo: `006202c4-abf5-58cc-8640-9c11d742a01d`
- Versão mínima declarada: 1.26.40
- Um perfil

## Contagem

| Tipo | Quantidade |
|---|---:|
| Entradas ZIP | 170 |
| JSON | 21 |
| PNG | 147 |
| Texturas bloco 8×8 | 137 |
| Partículas | 14 |
| Nuvens/sol 32×32 | 2 |
| Scripts no pacote | 0 |

ZIP passou CRC. Todos JSON foram lidos sem erro. As 137 texturas de bloco medem 8×8; nuvens e sol medem 32×32.

## Texturas
Cobertura inclui grama, solo, pedra, areia, cascalho, samambaias, flores, brotos, folhas, troncos, madeira, arbustos, cipós, bambu, vegetação aquática, musgo e serapilheira. Folhas reutilizam uma silhueta-base com paletas por espécie e pares transparentes/opacos.

Texturas não foram copiadas de pacotes de referência. 8×8 reduz área de pixels das imagens substituídas, mas não altera geometria, planos de vegetação, geração de chunks ou simulação.

## Ambiente e partículas
- Nuvens e sol: 32×32, sem animação.
- 14 arquivos de partículas adaptados do FPS Optimizer v2.9.2, namespace `lowmine:`.
- Quantidade padrão 30%; limite 4 por emissão nos emissores substituídos.
- Água `minecraft:default_water`, cáusticas/ondas desativadas.
- Sombras blocky_shadows, texel_size 16.
- Não há PBR/shader extra.

O controle de partículas não afeta todos emissores nativos. Água/sombras dependem da versão/modo gráfico e não garantem FPS maior.

## Interface, scripts e créditos
Inventário desktop, pocket e baús preservados. Não há JS, TS, `.mcfunction` ou Behavior Pack. Python serve apenas para compilar/validar fora do jogo. Folhas caindo globalmente exigiriam lógica/Behavior Pack.

Arte autoral: 137 texturas, paletas, nuvens, sol, ícone e UI. Material adaptado: partículas, água e sombras do FPS Optimizer v2.9.2, XiaoCraft, CC BY-NC 3.0. PotatoCraft, Embeddium e Vanilla × são somente referências. Consulte `CREDITOS.md`.

## Resultado
Validação estática aprovada para o SHA acima. Ainda é necessário importar no Bedrock, testar visualmente folhas/vegetação/água/UI e medir FPS/frame time em cenas equivalentes.
