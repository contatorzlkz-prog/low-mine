# Plano de desenvolvimento LowMine

## Concluído — v0.5.0
- [x] Criar identidade própria LowMine Equilibrado 8x.
- [x] Criar 38 texturas de bloco originais em 8×8.
- [x] Criar ícone e elementos próprios de interface.
- [x] Tornar inventário, crafting e baús mais transparentes, preservando legibilidade.
- [x] Adaptar 14 emissores de partículas com controles configuráveis.
- [x] Adaptar água sem cáusticas/ondas e sombras blocadas, mantendo créditos.
- [x] Manter um único perfil, sem PvP.
- [x] Remover scripts/loops do pacote de recursos.
- [x] Auditar as licenças dos quatro pacotes enviados.

## Próxima etapa — teste dentro do Minecraft
- [ ] Importar o v0.5.0 na versão exata do Bedrock usada.
- [ ] Conferir nome, versão, UUID e configurações.
- [ ] Testar inventário, crafting, baús e interface pocket.
- [ ] Conferir água e sombras no modo gráfico compatível.
- [ ] Verificar vegetação e blocos 8×8 em biomas diferentes.
- [ ] Verificar se os efeitos de partículas continuam legíveis.
- [ ] Registrar erros do Content Log e capturas de tela.
- [ ] Medir FPS e frame time com e sem LowMine na mesma cena.

## Otimização guiada por medições
- [ ] Separar geração de terreno novo, renderização e simulação de entidades.
- [ ] Medir a memória das texturas com ferramenta apropriada.
- [ ] Testar limites de partículas 4, 6 e 8 em situações equivalentes.
- [ ] Ajustar transparência somente após testar todos os contêineres.
- [ ] Fazer uma mudança por versão e manter builds anteriores para regressão.

## Fora do escopo de um Resource Pack
- Alterar o gerador ou cache de chunks.
- Forçar frustum/occlusion culling no RenderDragon.
- Mudar a distância de renderização ou simulação.
- Executar Rust dentro do cliente Bedrock.
