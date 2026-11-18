# LowMine Equilibrado 8x

<p align="center">
  <a href="https://github.com/contatorzlkz-prog/low-mine/releases/download/lowmine-v0.5.0/LowMine-Equilibrado-8x-v0.5.0.mcpack">
    <img src="https://img.shields.io/badge/⬇%20BAIXAR%20LOWMINE-.MCPACK-2ea44f?style=for-the-badge" alt="Baixar LowMine Equilibrado 8x">
  </a>
</p>

**LowMine Equilibrado 8x v0.5.0** é um pacote de recursos do Minecraft Bedrock com identidade visual e arte próprias, texturas 8×8, interface translúcida e efeitos configuráveis. O projeto combina conteúdo original LowMine com um conjunto limitado de recursos adaptados sob licença, descritos em CREDITOS.md e no arquivo CREDITOS.txt dentro do pacote.

> **Desempenho precisa ser medido no jogo.** A validação confirma a estrutura do pacote, não um ganho de FPS. Texturas menores podem reduzir a memória ocupada pelas imagens substituídas; elas não corrigem geração de chunks nem simulação do motor.

## O que esta versão contém

- 38 texturas originais de blocos em 8×8, incluindo grama, samambaias, folhas, pedra, terra, areia, cascalho e madeira.
- 46 imagens PNG no total, incluindo as texturas de bloco, a interface e o ícone.
- Inventário, crafting e baús com fundos mais transparentes; contornos e estados de seleção preservados.
- Água com cáusticas e ondas desativadas.
- Sombras blocadas, com tamanho de texel 16, nos modos que suportam essa definição.
- 14 definições de partículas adaptadas e configuráveis, com quantidade inicial de 50% e limite por emissão de 6.
- Um único perfil, sem subpacote PvP.
- Nenhum JavaScript, TypeScript, arquivo .mcfunction ou Behavior Pack no pacote.

## Configuração inicial

| Opção | Padrão |
|---|---:|
| Quantidade de partículas | 50% |
| Limite por efeito | 6 |
| Efeitos de poções | Ligado |
| Magia de bruxas e evocadores | Ligado |
| Rastros de flechas | Ligado |
| Efeitos de caldeirão | Ligado |
| Gêiseres | Desligado |
| Gás de gêiseres | Desligado |
| Partículas de enxofre | Desligado |

O limite é aplicado somente aos emissores que o LowMine inclui e substitui. Ele não controla todas as partículas nativas do Minecraft.

## Auditoria estática do pacote

| Verificação | Resultado |
|---|---:|
| Entradas no MCpack | 69 |
| JSON válidos | 21 de 21 |
| PNG | 46 |
| Texturas de bloco 8×8 | 38 |
| Definições de partículas | 14 |
| Telas de interface registradas | 3 (+ arquivo de registro) |
| Scripts executados pelo jogo | 0 |
| Tamanho compactado | 32.218 bytes |

SHA-256: 841b70ccb54acbc235e61334c7ad448bee95b1ec0cc53887b67449a21bbb240b

O manifesto não ativa capacidades PBR extras. O arquivo ui/_ui_defs.json registra as três telas personalizadas para o Bedrock. A auditoria estática não inicia o Minecraft nem mede FPS. A quantidade de PNGs não equivale à quantidade de texture handles, pois parte das texturas de blocos é agrupada em atlas pelo próprio jogo.

## Instalação e primeiro teste

1. Baixe LowMine-Equilibrado-8x-v0.5.0.mcpack.
2. Abra o arquivo com Minecraft Bedrock.
3. Confirme o nome LowMine Equilibrado 8x v0.5.0.
4. Ative o pacote como recurso global ou nos recursos do mundo.
5. Abra as configurações do pacote e confira os controles.
6. Teste inventário, crafting, baús, vegetação, água e sombras.
7. Compare com o jogo sem LowMine usando o mesmo mundo, posição e configurações.

Preencha docs/TEST_REPORT_TEMPLATE.md para registrar o resultado.

## Configuração inicial para computador modesto

Comece com 4 chunks de renderização e 4 de simulação. Se ficar estável, teste 6 chunks de renderização mantendo 4 de simulação. Use gráficos simples e desative os efeitos avançados disponíveis na sua versão.

A distância de renderização controla quantos chunks o cliente desenha. A distância de simulação controla onde entidades, plantas, líquidos e outras mecânicas continuam atualizando. O Resource Pack não muda essas opções e não pré-gera chunks. Consulte docs/CONFIGURACAO-CPU-FRACA.md.

## Autoria e licenças

- **Criação LowMine:** identidade visual, manifesto, ícone, 38 texturas 8×8, interface e ferramentas do projeto.
- **Recursos adaptados:** 14 definições de partículas, configurações de água e sombras do FPS Optimizer v2.9.2, de XiaoCraft, sob CC BY-NC 3.0. As alterações estão descritas em CREDITOS.md.
- **Referências sem arquivos copiados:** PotatoCraft 8x v1.4, Embeddium Optimizer v1.6 e Vanilla × Optimizer v2.4.2.

A composição inclui material CC BY-NC 3.0 e deve respeitar a condição não comercial dessa licença. Leia CREDITOS.md antes de redistribuir.

## Limites técnicos

O LowMine não substitui o RenderDragon, não implementa culling universal, não impede a geração de chunks, não controla a distância de renderização/simulação e não injeta Rust no cliente. Neblina, texturas e água/sombras alteram recursos visuais, não o código do motor.

Leia docs/LIMITES-DO-RENDERIZADOR.md para entender o que é possível otimizar em um Resource Pack.
