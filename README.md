# LowMine Equilibrado

**LowMine Equilibrado** é uma adaptação de pacote de recursos do Minecraft Bedrock, pensada para PCs modestos. A versão **0.4.0** mantém um único perfil, remove o PvP e procura equilibrar aparência, transparência da interface e quantidade de efeitos.

> **Importante:** um pacote de recursos não consegue corrigir a geração de chunks do motor do Minecraft. O LowMine reduz alguns custos visuais; as configurações de distância do próprio jogo continuam sendo fundamentais.

## O que mudou na versão 0.4.0

- Mantém um único perfil, sem subpacote PvP.
- Mantém 177 limites de partículas do perfil Lite em zero e reduz outras 11 contagens para valores baixos, preservando alguns efeitos importantes.
- Cria oito texturas 16×16 simplificadas para grama curta, samambaia, grama alta e versões secas.
- Deixa inventário, crafting, baús e painéis mais transparentes, preservando melhor os contornos e os estados de seleção.
- Ajusta a neblina visual para começar em 64 e terminar em 96 blocos.
- Mantém os UUIDs do LowMine e atualiza a versão do manifesto para `0.4.0`.

As texturas novas substituem **a imagem** da vegetação. Elas não removem nem alteram a geometria nativa dos blocos.

## Auditoria do pacote

| Verificação | Resultado |
|---|---:|
| Arquivos no pacote | 933 |
| Arquivos JSON | 318 válidos |
| Imagens PNG | 574 |
| Definições de partículas do pacote | 188 |
| Limites `max_particles` mantidos em zero | 177 |
| Biomas verificados | 94 |
| Definições de neblina | 104 |
| Texturas novas de vegetação | 8 |
| Perfil PvP | Removido |

Tamanho compactado: **658.214 bytes**. SHA-256: `98cdb09e379a4ce92159c7599fdd6b6967e4cf7c370e19953fe437ee5c6e15c7`.

A validação estática confirma estrutura, JSON, manifesto, texturas, referências de neblina e telas de interface. Ela não executa o Minecraft e não mede FPS.

## Configuração recomendada para PC fraco

Comece com:
- **Distância de renderização:** 6 chunks.
- **Distância de simulação:** 4 chunks.
- **Gráficos:** Simples, se essa opção existir.
- **Vibrant Visuals / Visuais vibrantes:** desativado.
- **Iluminação suave, nuvens e folhas sofisticadas:** desativadas ou no mínimo, se disponíveis.
- **Limite de FPS:** 30 se o jogo não conseguir manter 60 de forma estável; use 60 somente se conseguir sustentá-los.

Caso ainda ocorram travamentos ao carregar terreno novo, experimente 4 chunks de renderização. Veja [Configuração recomendada e diagnóstico de chunks](docs/CONFIGURACAO-CPU-FRACA.md).

A Microsoft explica que a distância de renderização determina quantos chunks o cliente desenha e que a distância de simulação também processa entidades, plantas, líquidos e atualizações do mundo. A distância de simulação tem custo adicional porque afeta a lógica do jogo e o trabalho do cliente. Consulte [Render Distance e Simulation Distance](https://learn.microsoft.com/en-us/minecraft/creator/documents/simulationrenderdistanceguide?view=minecraft-bedrock-stable).

## Instalar e testar

1. Baixe `LowMine-Equilibrado-v0.4.0-TEST.mcpack`.
2. Abra o arquivo com o Minecraft Bedrock.
3. Confirme que o nome e a versão aparecem corretamente.
4. Ative o único pacote **LowMine Equilibrado**.
5. Teste inventário, crafting, baús, hotbar, grama, samambaias e carregamento de terreno novo.
6. Compare com o jogo sem LowMine usando o mesmo mundo, posição, distância de renderização e distância de simulação.

Use o [modelo de relatório de teste](docs/TEST_REPORT_TEMPLATE.md) para anotar erros e resultados.

## Compilar e validar

Requisitos: Python 3.10+ e Pillow.

```bash
python -m pip install Pillow
python tools/gerar_pacote.py "LowMine-Ultra-Low-v0.3.2-FIXED.mcpack" "LowMine-Equilibrado-v0.4.0-TEST.mcpack"
python tools/validar_pacote.py "LowMine-Equilibrado-v0.4.0-TEST.mcpack"
```

O pacote v0.3.2 é usado como base do build e não está armazenado como binário neste repositório.

## Limites técnicos

O nevoeiro altera a aparência da distância, mas não faz o RenderDragon ignorar chunks. O Block Culling trabalha com faces encobertas de geometrias personalizadas; não é um sistema universal para esconder tudo atrás da câmera ou abaixo do solo. Um `.mcpack` também não pode injetar Rust no renderizador do Bedrock.

As possibilidades reais e as referências de desenvolvimento estão em [Limites do renderizador e otimizações possíveis](docs/LIMITES-DO-RENDERIZADOR.md).

## Créditos e licença

O pacote original é **Boosted FPS (Optimized Performance) v2.4.1**, criado por **XiaoCraft**.

- Projeto original: https://www.curseforge.com/minecraft-bedrock/texture-packs/boosted-fps-optimized-performance
- Licença original: **Creative Commons Attribution-NonCommercial 3.0 Unported (CC BY-NC 3.0)** — https://creativecommons.org/licenses/by-nc/3.0/

O LowMine é uma adaptação, não um projeto original ou endossado por XiaoCraft. Os créditos e as condições não comerciais da licença original devem ser mantidos. Consulte [ATTRIBUTION.txt](ATTRIBUTION.txt).
