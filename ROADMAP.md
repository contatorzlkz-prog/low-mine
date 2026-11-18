# Plano de desenvolvimento

## Concluído — versão 0.4.0
- [x] Manter um único perfil e remover o PvP.
- [x] Manter UUIDs estáveis e versão SemVer como texto no manifesto v3.
- [x] Preservar 177 limites de partículas em zero e reduzir outras 11 contagens.
- [x] Criar oito texturas 16×16 para grama e samambaias.
- [x] Aumentar a transparência do inventário, crafting, baús e hotbar.
- [x] Ajustar a neblina visual para 64–96 blocos.
- [x] Validar 933 entradas, 318 JSON, 94 biomas, 104 arquivos de neblina e telas de UI.

## Próxima etapa — teste dentro do Minecraft
- [ ] Confirmar que a importação mostra LowMine Equilibrado v0.4.0.
- [ ] Testar inventário, crafting, baús, Ender Chest, shulker e barril.
- [ ] Verificar se slots e contornos continuam claros.
- [ ] Comparar grama curta, samambaias, grama alta e versões secas em biomas diferentes.
- [ ] Testar carregamento de chunks ao andar, correr e voar.
- [ ] Registrar a versão exata do Bedrock e os erros do Content Log.
- [ ] Comparar FPS e estabilidade de frame time com e sem LowMine na mesma cena.

## Otimização futura
- [ ] Separar travamento de geração de chunks de queda de FPS por renderização.
- [ ] Medir consumo de memória das texturas com ferramentas compatíveis.
- [ ] Revisar mais texturas somente quando houver um ganho provável e sem apagar a leitura dos blocos.
- [ ] Fazer uma alteração por versão e manter um pacote estável para retorno.

## Fora do escopo de um pacote de recursos
- O resource pack não pode definir a distância de renderização ou de simulação do mundo.
- O nevoeiro não implementa frustum culling ou occlusion culling.
- O Block Culling não é um filtro global de geometria vanilla.
- Rust pode servir para ferramentas externas de análise e compilação, mas não substitui o RenderDragon por meio de um .mcpack.
