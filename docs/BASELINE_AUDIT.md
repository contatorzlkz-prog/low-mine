# Auditoria técnica — LowMine Equilibrado v0.4.0

## Escopo

A auditoria verifica apenas os arquivos do .mcpack: manifesto, JSON, imagens, telas, partículas e referências de biomas/neblina. Ela não inicia o Minecraft, não mede FPS e não confirma o comportamento das telas em uma versão específica do Bedrock.

## Identidade do pacote

- Arquivo: `LowMine-Equilibrado-v0.4.0-TEST.mcpack`
- Tamanho: 658.214 bytes.
- SHA-256: `898a63dc7b221d8e0a2ab489f3f41b965ddc3a2cf6c05658beb8d25940a6f91a`
- Manifesto: formato 3.
- Versão do cabeçalho e do módulo: string SemVer `"0.4.0"`.
- UUIDs: mantidos da identidade LowMine.
- Um único perfil; sem `subpacks`, PvP ou configurações experimentais no manifesto.
- Créditos de XiaoCraft e licença CC BY-NC 3.0 preservados.

## Inventário de arquivos

| Tipo | Quantidade |
|---|---:|
| Entradas no ZIP | 933 |
| JSON | 318 |
| PNG | 574 |
| Arquivos de idioma | 29 |
| Definições de partículas | 188 |
| Texturas novas de vegetação | 8 |

Todos os 318 arquivos JSON foram lidos sem erro. O ZIP passou no teste de integridade e não contém caminhos duplicados ou inseguros.

## Partículas

- 177 campos `max_particles` continuam em zero, como já acontecia no subpacote Lite da base.
- 11 campos `num_particles` foram reduzidos para quantidades baixas:
  - Flechas, caldeirão, evocador, bruxa e efeitos de poções: 1.
  - Poção persistente: 2.
  - Poção arremessável: 4 (antes a definição usava 30).
  - Gás de gêiser e partículas de enxofre: 0.

Esses valores limitam as definições substituídas pelo pacote. Efeitos nativos que não são substituídos pelo LowMine ainda podem aparecer. A auditoria conta definições, não partículas em execução nem economia real de CPU.

## Texturas de vegetação

Foram criadas oito substituições 16×16:
- `tallgrass.png` e `fern.png`.
- `double_plant_grass_top.png` e `double_plant_grass_bottom.png`.
- `double_plant_fern_top.png` e `double_plant_fern_bottom.png`.
- `short_dry_grass.png` e `tall_dry_grass.png`.

Os nomes e caminhos seguem os identificadores de texturas usados pelo mapeamento vanilla de Bedrock. As imagens têm fundo transparente e menos pixels opacos. A geometria dos blocos vanilla não foi alterada; portanto, isso reduz a densidade visual da textura, não o número de faces/planos do modelo.

## Interface

- Inventário e crafting (desktop): `$screen_background_alpha = 0.05`.
- Inventário pocket/toque: `$screen_background_alpha = 0.05`.
- Baús pequenos/grandes, Ender Chest, shulker e barril: `$screen_background_alpha = 0.05` no ramo desktop.
- Contêineres data-driven: mesmo valor.
- Textura de fundo externo e painéis: alpha máximo 38/255.
- Fundo dos slots: alpha máximo 50/255.
- Barra de itens e fundos de hotbar: ajustados para transparência maior; contornos/estados de seleção são mantidos.

A UI JSON do Bedrock é sensível à versão e ao modo de interface. A validação confirma a estrutura dos arquivos, não o funcionamento no jogo.

## Biomas e neblina

- 94 entradas em `biomes_client.json`.
- 104 definições de neblina.
- Nenhuma referência personalizada `lowmine:` sem definição.
- Campos de neblina do ar ajustados para início em 64 e término em 96 blocos, onde esses campos existem.

A neblina é visual. Ela não manda o RenderDragon deixar de processar chunks, não oculta apenas o que está atrás da câmera e não substitui o controle de distância de renderização.

## Validação final

A validação estática local passou:
- Integridade do ZIP e caminhos únicos/seguros.
- Manifesto v3 e versões SemVer como texto.
- UUIDs válidos e únicos.
- 318/318 JSON válidos.
- 188 arquivos de partículas verificados.
- 94 biomas e 104 arquivos de neblina; sem referências personalizadas ausentes.
- Quatro arquivos de interface registrados em `ui/_ui_defs.json`.
- Oito texturas de vegetação 16×16 e com transparência real.
- Créditos e licença presentes.

## O que ainda precisa ser testado

1. Importar o pacote na versão exata do Minecraft Bedrock utilizada.
2. Conferir nome, versão e UUID na tela de importação.
3. Abrir inventário, crafting, baús e contêineres.
4. Verificar se a vegetação continua reconhecível nos biomas.
5. Testar carregamento de chunks novos com as distâncias recomendadas.
6. Comparar FPS médio e estabilidade de frame time, no mesmo mundo e na mesma cena, com e sem LowMine.

Nenhum aumento de FPS é declarado antes desse teste.
