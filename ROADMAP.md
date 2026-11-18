# Plano de desenvolvimento LowMine

## Concluído — v0.6.0
- [x] Redesenhar 137 texturas de bloco em 8×8.
- [x] Reutilizar silhuetas-base de folhas/plantas com paletas específicas.
- [x] Criar pares de folhas transparentes e opacas.
- [x] Redesenhar troncos, topos, tábuas e madeira descascada.
- [x] Ampliar vegetação para flores, samambaias, arbustos, brotos, cipós, bambu, água, musgo e serapilheira.
- [x] Criar nuvens e sol compactos em 32×32.
- [x] Reduzir partículas para 30%, limite 4 por emissão nos emissores incluídos.
- [x] Preservar água, sombras, UI, créditos e licença.
- [x] Manter um perfil e nenhum script/loop no jogo.
- [x] Automatizar compilação e validação estática v0.6.0.

## Próxima etapa — teste no Minecraft
- [ ] Importar v0.6.0 na versão exata do Bedrock.
- [ ] Conferir nome, versão, UUID e controles.
- [ ] Testar folhas transparentes/opacas nos biomas.
- [ ] Testar troncos, flores, vegetação aquática, nuvens e sol.
- [ ] Testar inventário, crafting, baús e interface pocket.
- [ ] Verificar erros do Content Log.
- [ ] Medir FPS e frame time com e sem LowMine na mesma cena.

## Fora do escopo de um Resource Pack
- Alterar gerador/cache de chunks.
- Forçar culling universal no RenderDragon.
- Mudar distâncias de renderização/simulação.
- Iniciar comportamento universal de folhas caindo sem lógica/Behavior Pack.
- Injetar Rust ou outro código no cliente Bedrock.
