# Redesign LowMine v0.6.0

## Direção de arte
Pixel art limpa e legível em 8×8. A base geométrica das folhas e plantas é reutilizada entre espécies; paletas variam por árvore para dar identidade sem exigir imagens de alta resolução.

## Cobertura
137 texturas substituem grama, solo, pedra, cascalho, areia, samambaias, flores, brotos, folhas, troncos, madeira, arbustos, cipós, bambu, vegetação aquática, musgo e serapilheira. Folhas têm pares transparentes/opacos. Nuvens e sol usam 32×32.

## Perfil
Um perfil, partículas em 30% e limite 4 por emissão nos emissores substituídos. Água sem cáusticas/ondas e sombras blocadas. Sem shaders PBR, animações de ambiente, brilho ou partículas extras.

## Limites
Resolução menor reduz a área de pixels substituída, mas não garante FPS nem remove a geometria dos planos de vegetação. Um Resource Pack puro não inicia folhas caindo automaticamente de todas as árvores; isso exigiria lógica/entidades/Behavior Pack e ficou fora do pacote leve.

## Integridade e autoria
Novas texturas, paletas, nuvens, sol e ícone são criações LowMine. Permanecem os créditos e licença CC BY-NC 3.0 para partículas, água e sombras adaptadas do FPS Optimizer v2.9.2, de XiaoCraft. Outros packs são referências sem cópia de arquivos.
