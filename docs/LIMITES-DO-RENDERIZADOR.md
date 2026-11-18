# Limites do renderizador e técnicas reais

## Recomendações oficiais

A Microsoft recomenda controlar o tamanho e a quantidade de texturas, evitar arquivos desnecessários, considerar texture handles e reduzir trabalho repetido de entidades/IA. A documentação recomenda menos de 800 texture handles para add-ons; texturas de blocos podem ser agrupadas em atlas, portanto número de PNGs e número de handles não são a mesma coisa.

Fonte:
https://learn.microsoft.com/en-us/minecraft/creator/documents/practices/improvingperformanceandresourceusage?view=minecraft-bedrock-stable

As texturas são carregadas sem compressão para memória gráfica. Uma imagem 8×8 possui 64 texels, enquanto uma 16×16 possui 256; portanto, a imagem 8×8 tem um quarto da área de pixels. Isso se aplica apenas às imagens substituídas pelo LowMine, não a todas as texturas do jogo.

## Partículas
O LowMine adapta 14 emissores do FPS Optimizer v2.9.2. Os controles de quantidade e limite usam as configurações do pacote e expressões Molang. O limite afeta apenas os emissores incluídos; outros efeitos nativos continuam podendo aparecer.

Documentação da propriedade num_particles:
https://learn.microsoft.com/en-us/minecraft/creator/reference/content/particlesreference/examples/particlecomponents/emitter_rate_instant?view=minecraft-bedrock-stable

## Água e sombras
O LowMine adapta a configuração de água sem cáusticas/ondas e sombras blocadas do FPS Optimizer. O efeito depende da versão e do modo gráfico compatível. Isso não garante aumento de FPS em qualquer computador.

## Interface
Overrides pequenos são usados para preservar o layout vanilla e alterar apenas a opacidade de fundo. A estrutura de UI pode mudar entre versões; teste desktop, pocket e contêineres no jogo.

## Scripts e loops
A versão 0.5.0 é somente Resource Pack: não possui Behavior Pack, JavaScript, TypeScript ou .mcfunction. Não adiciona loops no mundo.

Em projetos futuros com scripts, a Microsoft recomenda usar profiler, evitar operações caras repetidas a cada tick e distribuir trabalho periódico em vez de executá-lo todo no mesmo tick.

Fonte:
https://learn.microsoft.com/en-us/minecraft/creator/documents/scripting/script-performance?view=minecraft-bedrock-stable

## Neblina, Block Culling e RenderDragon
- Neblina altera a aparência da distância; não manda o RenderDragon descartar toda a geometria depois dela.
- Block Culling é voltado a faces de blocos personalizados encobertas por blocos vizinhos; não é culling global para todo o mundo vanilla.
- Um .mcpack não injeta Rust no cliente nem substitui o RenderDragon.

## Como medir
Compare sem LowMine e com LowMine na mesma versão, dispositivo, mundo, posição, resolução e distâncias. Separe a geração de terreno novo da renderização em área já carregada. Registre FPS médio e frame time.
