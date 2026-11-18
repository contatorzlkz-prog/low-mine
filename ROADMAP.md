# Plano de desenvolvimento LowMine

## Concluído — v0.5.0
- [x] Criar identidade própria LowMine Equilibrado 8x.
- [x] Desenhar 38 texturas de bloco originais em 8×8, com paletas consistentes.
- [x] Criar ícone, painéis e elementos de UI LowMine.
- [x] Adaptar 14 definições de partículas do FPS Optimizer com namespace próprio e limite por rajada.
- [x] Adaptar água sem cáusticas/ondas e sombras blocadas, com créditos/licença.
- [x] Manter apenas um perfil, sem PvP.
- [x] Criar validador de manifesto, JSON, UI, partículas, licença e texturas.
- [x] Manter o pacote sem scripts/loops executados pelo jogo.
- [x] Documentar referências e direitos dos quatro pacotes estudados.

## Próxima etapa — teste no Minecraft
- [ ] Importar o v0.5.0 na versão exata do Bedrock usada.
- [ ] Conferir nome, versão, UUID e opções do pacote.
- [ ] Testar inventário, crafting, baús e inventário pocket em desktop/toque.
- [ ] Conferir a água e as sombras em dispositivos/modos compatíveis.
- [ ] Verificar se partículas mantêm leitura sem criar picos em poções e combates.
- [ ] Conferir folhas, grama, samambaias e blocos 8×8 em vários biomas.
- [ ] Registrar erros do Content Log, travamentos e prints.
- [ ] Medir FPS e estabilidade de frame time em cenas equivalentes, com e sem LowMine.

## Otimização guiada por medições
- [ ] Distinguir geração de terreno novo, renderização de cena e simulação de entidades.
- [ ] Medir a carga de texturas com ferramenta de inspeção apropriada quando disponível.
- [ ] Verificar se o limite de rajada precisa ser 4, 6 ou 8 usando testes reais.
- [ ] Ajustar transparência somente após conferir legibilidade/seleção.
- [ ] Fazer uma mudança por versão e manter builds anteriores para regressão.

## Fora do escopo de um Resource Pack
- Alterar o gerador de chunks ou cache do Minecraft.
- Forçar frustum/occlusion culling do RenderDragon.
- Mudar render distance ou simulation distance.
- Rodar Rust dentro do cliente Bedrock.
