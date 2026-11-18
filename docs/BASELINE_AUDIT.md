# Auditoria técnica — LowMine Equilibrado 8x v0.5.0

## Escopo
Esta auditoria verifica estrutura do ZIP, manifesto, JSON, partículas, interface, água, sombras, créditos e dimensões das imagens. Ela não inicia o Minecraft, não mede FPS e não confirma o comportamento de cada tela em uma versão específica do Bedrock.

## Identidade
- Arquivo: LowMine-Equilibrado-8x-v0.5.0.mcpack
- Tamanho compactado: 32.218 bytes
- SHA-256: 841b70ccb54acbc235e61334c7ad448bee95b1ec0cc53887b67449a21bbb240b
- Manifesto: formato 3
- Versão: string SemVer 0.5.0
- UUID do cabeçalho: 21ca0070-fc45-5c56-8812-4b1cda3172a8
- UUID do módulo: 006202c4-abf5-58cc-8640-9c11d742a01d
- Versão mínima declarada: 1.26.40
- Um único perfil, sem subpacote PvP

## Contagem de arquivos

| Tipo | Quantidade |
|---|---:|
| Entradas no ZIP | 69 |
| JSON | 21 |
| PNG | 46 |
| Texturas de bloco 8×8 | 38 |
| Definições de partículas | 14 |
| Arquivos de interface | 3 |
| Scripts de jogo | 0 |

O ZIP passou pelo teste CRC. Todos os 21 arquivos JSON foram lidos sem erro. Todas as 38 texturas de bloco medem 8×8 pixels.

## Texturas LowMine
As 38 imagens de bloco foram desenhadas para o LowMine com uma paleta de cores coerente. Incluem grama, samambaias, folhas de diferentes árvores, terra, pedra, pedregulho, cascalho, areia, tábuas e tronco.

Os nomes/caminhos foram conferidos com o mapeamento atual de texturas do Bedrock/Mojang. As imagens não foram extraídas dos quatro pacotes estudados. A resolução 8×8 reduz a área de pixels das imagens substituídas; não remove geometria, planos de vegetação ou trabalho de geração de chunks.

## Partículas
- 14 arquivos JSON adaptados do FPS Optimizer v2.9.2.
- Consultas de configuração convertidas de opt: para lowmine:.
- Quantidade padrão: 50%.
- Limite padrão por emissão: 6.
- Poções, magia, caldeirões e rastros visuais ativados por padrão.
- Gêiseres, gás e partículas de enxofre desativados por padrão.

O limite afeta apenas os emissores que o LowMine substitui; não controla todos os efeitos nativos do Minecraft.

## Água e sombras
- Identificador de água: minecraft:default_water.
- Cáusticas: desativadas.
- Ondas: desativadas.
- Concentrações de clorofila, sedimentos suspensos e CDOM: 0.
- Sombras: blocky_shadows.
- Tamanho de texel: 16.

O suporte depende da versão e do modo gráfico. Essas configurações são principalmente visuais e não são garantia de ganho de FPS em todo hardware.

## Interface
- Telas: inventário desktop, inventário pocket e baús.
- As três telas estão registradas em ui/_ui_defs.json.
- O manifesto não ativa capacidades PBR extras.
- Alpha de fundo configurado: 0,10.
- Texturas próprias para painéis, slots e barra de itens.
- Contorno de seleção preservado.
- A estrutura de UI JSON pode variar entre versões e modos de interface; confirmar no jogo é obrigatório.

## Scripts
Não há JavaScript, TypeScript, .mcfunction ou Behavior Pack no arquivo. O código Python do projeto serve para compilar e validar o pacote no computador; não é incluído nem executado dentro do Minecraft.

## Créditos
- Conteúdo original LowMine: identidade, ícone, interface e arte 8×8.
- Material adaptado: 14 partículas, água e sombras do FPS Optimizer v2.9.2, XiaoCraft, CC BY-NC 3.0.
- PotatoCraft, Embeddium Optimizer e Vanilla × Optimizer: referência técnica; nenhum arquivo foi copiado.
- A composição mantém a condição não comercial do material adaptado. Consulte CREDITOS.md.

## Resultado
Validação estática aprovada para o arquivo identificado pelo SHA-256 acima. Ainda é necessário importar no Bedrock, abrir inventário/baús, verificar vegetação, água/sombras e medir desempenho em cenas iguais com e sem LowMine.
