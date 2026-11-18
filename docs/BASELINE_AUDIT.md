# Auditoria técnica — LowMine Equilibrado 8x v0.5.0

## Escopo e limites

A auditoria verifica o .mcpack pronto: manifesto, UUIDs, JSON, Molang, configurações, UI, água, sombras, créditos e imagens. Ela não abre o Minecraft, não mede FPS e não verifica o desempenho real de uma CPU/GPU específica.

## Identidade do pacote

- Arquivo: LowMine-Equilibrado-8x-v0.5.0.mcpack
- Tamanho: 32.451 bytes.
- SHA-256: 68635f505fc9267b480019177e6ec2a3f1095bc9b67baa4551c6672add6ec16b.
- Manifesto: formato 3.
- Versão do cabeçalho e módulo: string SemVer "0.5.0".
- UUID principal: 21ca0070-fc45-5c56-8812-4b1cda3172a8.
- UUID do módulo: 006202c4-abf5-58cc-8640-9c11d742a01d.
- min_engine_version: "1.26.40".
- Um único perfil, sem subpacks/PvP.

## Arquivos

| Tipo | Quantidade |
|---|---:|
| Entradas no ZIP | 72 |
| JSON | 21 |
| PNG | 50 |
| Texturas de bloco 8×8 | 38 |
| Definições de partículas | 14 |
| Arquivos de script/behavior dentro do pacote | 0 |

O ZIP passou no teste de integridade e os 21 JSON foram lidos sem erro. O pacote contém menos de 100 entradas.

## Texturas originais LowMine

As 38 texturas de bloco foram desenhadas para 8×8 pixels com uma paleta coerente:
- Grama, topo/lateral, samambaia, grama alta e versões secas.
- Folhas de carvalho, bétula, abeto, selva, acácia, carvalho escuro, mangue, cerejeira e azaleia, com variantes opacas quando o mapeamento vanilla usa essas variantes.
- Terra, pedra, pedregulho, cascalho, areia, tábuas e tronco de carvalho.

Os nomes e caminhos foram conferidos com o mapeamento de recursos do Bedrock/Mojang. Não foram redistribuídas texturas vanilla. A resolução 8×8 diminui a área de pixels das imagens modificadas; não elimina polígonos, planos de grama ou trabalho de geração de chunks.

## Configurações de partículas

| Controle | Padrão |
|---|---:|
| Quantidade de partículas | 50% |
| Limite por efeito/rajada | 6 |
| Efeitos de poções | Ligado |
| Magia de bruxas e evocadores | Ligado |
| Rastros de flechas | Ligado |
| Efeitos de caldeirão | Ligado |
| Gêiseres | Desligado |
| Gás de gêiseres | Desligado |
| Partículas de enxofre | Desligado |

- Definições adaptadas: 14 arquivos JSON.
- Todas usam consultas do namespace lowmine:.
- Consultas identificadas: partícula (14), limite de rajada (14), setas (1), caldeirão (1), magia (2), gêiseres (3), poções (4), gás (1), enxofre (2).
- As emissões instantâneas usam Math.min para respeitar o limite configurado.
- Isso controla somente os 14 emissores incluídos/substituídos pelo pacote; não desativa todos os efeitos nativos do Minecraft.

## Água e sombras

- Água: identificador minecraft:default_water.
- Cáusticas: desativadas.
- Ondas: desativadas.
- Concentrações de clorofila, sedimentos suspensos e CDOM: 0.
- Sombras: estilo blocky_shadows, texel_size: 16.

Esses recursos dependem da versão e do modo gráfico que suportam as respectivas definições. O estilo blocado é sobretudo visual; não deve ser interpretado como FPS garantido.

## Interface

- Telas registradas: inventário desktop, inventário pocket e baús.
- Alpha do fundo de tela: 0,14.
- Painéis, slots e controles usam imagens próprias LowMine.
- Contorno de slot selecionado é preservado para legibilidade.
- A estrutura JSON de UI pode variar entre versões e modos de interface do Bedrock; confirmar no jogo é obrigatório.

## Scripts e loops

- Arquivos JavaScript/TypeScript: 0.
- Arquivos .mcfunction: 0.
- Behavior Pack: nenhum.
- Scripts ou loops executados no jogo: nenhum.

O código Python do projeto serve para compilar e validar o arquivo no computador; ele não é incluído nem executado dentro do Minecraft.

## Créditos e licenças

- Conteúdo original LowMine: identidade, manifesto, arte 8×8, ícone, UI e ferramentas.
- Material adaptado de FPS Optimizer v2.9.2, XiaoCraft, CC BY-NC 3.0: 14 partículas, água e sombras. Namespace/configurações foram ajustados.
- PotatoCraft 8x v1.4, Embeddium Optimizer v1.6 e Vanilla × Optimizer v2.4.2: referência técnica; nenhum arquivo foi copiado.
- As condições não comerciais do material adaptado se aplicam à distribuição da composição. Consulte CREDITOS.md.

## Resultado e próximos testes

Validação estática aprovada:
- ZIP íntegro.
- 21/21 JSON válidos.
- Manifesto v3, SemVer e UUIDs corretos.
- 14 partículas identificadas e com consultas de configurações resolvidas.
- Água e sombras presentes com os valores esperados.
- Três telas de UI registradas.
- 38 texturas de bloco 8×8 reconhecidas.
- Créditos completos presentes.

Ainda é necessário importar no Bedrock, conferir as opções, olhar os biomas, abrir inventário/baús e comparar FPS/frame time em uma cena idêntica com e sem LowMine.
