# Configuração recomendada para CPU fraca

Este guia separa travamentos ao carregar terreno de quedas de FPS durante o jogo. **Um pacote de recursos não controla o carregamento nem a geração de chunks.** Essas etapas pertencem ao motor do Minecraft.

## Ponto inicial equilibrado

| Opção | Valor inicial | Ajuste |
|---|---:|---|
| Distância de renderização | **6 chunks** | Se ainda travar ao explorar terreno novo, teste 4. Só aumente para 8 depois de ficar estável. |
| Distância de simulação | **4 chunks** | Mantenha em 4 em um PC fraco. |
| Gráficos | Simples | Use o modo mais leve disponível na sua versão. |
| Visuais Vibrantes | Desativado | Caso essa opção exista. |
| Folhas/iluminação sofisticadas | Desativadas ou no mínimo | Caso essas opções existam. |
| Nuvens e efeitos de céu | Desativados | Reduza efeitos cosméticos. |
| Limite de FPS | 30 estáveis | Use 60 apenas se o computador conseguir manter 60 sem oscilações grandes. |

A distância de renderização determina quantos chunks o cliente desenha. A distância de simulação determina onde entidades, crescimento de plantas, líquidos e outras atualizações do mundo continuam ativas. A simulação também custa CPU; diminuir apenas o nevoeiro não diminui essa carga. Consulte a [documentação da Microsoft sobre distância de renderização, simulação e ticking areas](https://learn.microsoft.com/en-us/minecraft/creator/documents/simulationrenderdistanceguide?view=minecraft-bedrock-stable).

## Identifique qual travamento acontece

### 1. Só trava ao entrar em terreno nunca visitado

O jogo está gerando e preparando terreno novo, lendo e gravando dados do mundo. Um resource pack não pré-gera chunks nem acelera diretamente o gerador.

Teste renderização em 4 chunks. Avance mais devagar e espere o terreno aparecer antes de continuar explorando. Mantenha o mundo em SSD, deixe espaço livre no disco e feche tarefas pesadas em segundo plano.

### 2. O FPS cai quando olha para florestas ou áreas cheias de plantas

Isso aponta mais para desenho de cena, transparência, geometria visível ou muitos elementos na tela. O LowMine v0.4.0 simplifica oito texturas de grama e samambaias, mas não remove os planos/ modelos de geometria dos blocos vanilla. Portanto, o ganho de FPS não é garantido.

### 3. Trava perto de mobs, fazendas, aldeias ou redstone

Pode ser custo de simulação, comportamento de entidades, pathfinding, líquidos e atualizações de blocos. Reduza a distância de simulação e evite excesso de entidades e mecanismos ativos.

Em mundos com cheats, consulte as áreas de ticking com:

```mcfunction
/tickingarea list all-dimensions
```

Remova apenas áreas que você reconhece como desnecessárias; não remova uma área usada por uma fazenda ou sistema que precisa continuar ativo.

A Microsoft recomenda limitar entidades e comportamentos desnecessários, porque entidades podem continuar executando comportamentos mesmo quando estão fora da visão do jogador. Consulte [Improving performance and resource usage](https://learn.microsoft.com/en-us/minecraft/creator/documents/practices/improvingperformanceandresourceusage?view=minecraft-bedrock-stable).

### 4. Continua travando em uma área que já foi carregada

Investigue memória, disco, outros pacotes ativos, entidades e possíveis problemas no mundo. Faça uma cópia de segurança antes de testar sem outros add-ons.

## Teste controlado

1. Faça uma cópia de segurança do mundo.
2. Anote a versão exata do Bedrock, o dispositivo e as configurações.
3. Teste sem LowMine com renderização 6 e simulação 4.
4. Repita com LowMine, na mesma posição e com as mesmas opções.
5. Teste primeiro uma área já visitada e depois um trecho novo.
6. Anote se a travada acontece ao gerar terreno, ao olhar para vegetação ou perto de mobs/fazendas.

Não compare FPS de mundos, posições ou distâncias diferentes como se fosse um teste controlado.

## O que o LowMine não consegue fazer

- Definir a distância de renderização ou simulação.
- Pré-gerar ou manter chunks em cache.
- Impedir o jogo de gerar terreno novo.
- Transformar neblina em culling real.
- Mandar o RenderDragon ignorar tudo atrás da câmera ou abaixo do solo.
- Injetar Rust no cliente Bedrock.

A neblina 64–96 do LowMine é visual; a redução de texturas afeta imagens específicas, não a geração de chunks.
