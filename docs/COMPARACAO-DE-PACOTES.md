# Comparação dos quatro pacotes estudados

Os quatro .mcpack fornecidos foram inspecionados antes da criação do LowMine 8x. Esta página separa o que foi extraído dos arquivos do que foi usado apenas como referência de desenvolvimento.

## PotatoCraft 8x v1.4

- 2.662 entradas no arquivo.
- 2.631 PNGs; 2.550 eram 8×8.
- Manifesto dentro de My_RESOURCE_Pack/manifest.json, não na raiz.
- O manifesto do arquivo não apresentava autor/licença claros.
- O LowMine aproveita a ideia da resolução 8×8, mas suas texturas são desenhadas do zero.
- Nenhum arquivo do PotatoCraft foi copiado.

## FPS Optimizer v2.9.2

- Autor declarado: XiaoCraft.
- Licença indicada no projeto: CC BY-NC 3.0.
- Fornece controles Molang para quantidade de partículas e número máximo por rajada.
- Inclui configurações para água e sombras.
- O LowMine adapta 14 arquivos de partículas, water/water.json e shadows/global.json, muda o namespace para lowmine: e aplica novos valores padrão.
- Os créditos e a condição não comercial são mantidos no pacote.

## Embeddium Optimizer (Smart FPS Boost) v1.6

- Manifesto identifica LeviiCraft como autor.
- A cópia fornecida não apresentou licença clara de redistribuição.
- Possui grande conjunto de overrides de partículas e estrutura de otimização.
- O LowMine estudou a organização, mas não copiou arquivos ou código.

## Vanilla × Optimizer v2.4.2

- Manifesto identifica XiaoCraft.
- Licença indicada: CC BY-NC-SA 4.0.
- Referência usada para comparar estilo visual de água e sombras.
- Nenhum arquivo ou código desse pacote foi copiado para o LowMine. As definições atuais de água/sombras vêm do FPS Optimizer, sob CC BY-NC 3.0.

## Decisões para o LowMine

1. Criar identidade e arte próprias em vez de colar milhares de arquivos.
2. Limitar 8×8 às texturas que o projeto substitui, mantendo o jogo base intacto.
3. Usar 50% de partículas e limite 6 por efeito como configuração inicial, em vez de desativar todo feedback visual.
4. Desligar cáusticas/ondas de água e usar sombras blocadas como opções visuais onde suportadas.
5. Não colocar scripts, funções ou loops executados no jogo nesta versão.
6. Manter créditos e condições de licença explícitos.

A redução do tamanho de arquivos não prova aumento de FPS. O resultado precisa ser medido no Minecraft com o mesmo mundo, cena e configurações.
