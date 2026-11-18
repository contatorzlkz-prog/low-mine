# Plano de desenvolvimento LowMine

## Concluído — v0.6.1
- [x] Redesenhar troncos e topos com veios não retilíneos em 8×8.
- [x] Usar quatro tons por paleta de espécie para manter leitura com poucos pixels.
- [x] Adicionar mapas UV e ícones de sete conjuntos de armaduras.
- [x] Preservar transparência do inventário desktop/mobile e de baús, Ender, shulker e barril.
- [x] Adicionar prévia visual e validador estático para a nova versão.
- [x] Preservar um perfil e nenhum script/loop executado no jogo.

## Concluído — v0.6.0
- [x] Redesenhar 137 texturas de bloco em 8×8.
- [x] Reutilizar silhuetas-base de folhas/plantas com paletas específicas.
- [x] Criar pares de folhas transparentes e opacas.
- [x] Redesenhar troncos, topos, tábuas e madeira descascada.
- [x] Ampliar vegetação para flores, samambaias, arbustos, brotos, cipós, bambu, água, musgo e serapilheira.
- [x] Criar nuvens e sol compactos em 32×32.
- [x] Reduzir partículas para 30%, limite 4 por emissão nos emissores incluídos.
- [x] Preservar água, sombras, UI, créditos e licença.
- [x] Automatizar compilação e validação estática v0.6.0.

## Próxima etapa — teste no Minecraft
- [ ] Importar v0.6.1 na versão exata do Bedrock.
- [ ] Conferir armaduras equipadas em personagens e ícones no inventário.
- [ ] Testar troncos de todas as espécies e suas faces superiores.
- [ ] Testar folhas, vegetação, água, nuvens e sol nos biomas.
- [ ] Testar inventário, crafting, pocket, baús, Ender, shulker e barril.
- [ ] Verificar erros do Content Log.
- [ ] Medir FPS e frame time com e sem LowMine na mesma cena.

## Fora do escopo de um Resource Pack
- Alterar gerador/cache de chunks.
- Forçar culling universal no RenderDragon.
- Mudar distâncias de renderização/simulação.
- Iniciar comportamento universal de folhas caindo sem lógica/Behavior Pack.
- Injetar Rust ou outro código no cliente Bedrock.
