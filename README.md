# LowMine Equilibrado 8x

**LowMine Equilibrado 8x v0.5.0** é um pacote de recursos do Minecraft Bedrock com identidade, texturas 8×8, ícone, interface e ferramentas desenvolvidas para o projeto LowMine. Ele combina esse conteúdo próprio com recursos adaptados de terceiros, sempre identificados em CREDITOS.md.

> **Não é uma promessa de FPS.** O pacote foi validado estruturalmente, mas ainda precisa ser importado e medido no Minecraft na máquina de destino. Texturas menores podem reduzir memória de textura; não corrigem diretamente geração de chunks, simulação ou CPU.

## O que esta versão reúne

- 38 texturas de bloco em 8×8 originais LowMine, incluindo pedra, terra, areia, madeira, grama, samambaias e variações de folhas.
- 50 imagens PNG no pacote, contando ícone e UI.
- Interface mais translúcida para inventário, crafting, baús e inventário pocket; contorno de seleção preservado.
- Água com cáusticas e ondas desativadas e concentrações de partículas aquáticas zeradas.
- Sombras blocadas (texel_size 16) nos modos que suportam essa configuração.
- 14 definições de partículas adaptadas do FPS Optimizer v2.9.2, com quantidade padrão de 50% e limite de rajada 6.
- Um único perfil; não existe subpacote PvP.
- Nenhum JavaScript, TypeScript, .mcfunction, Behavior Pack ou loop de script é incluído.

## Perfil equilibrado de partículas

| Controle | Padrão |
|---|---:|
| Quantidade de partículas | 50% |
| Limite por efeito/rajada | 6 |
| Poções | Ligado |
| Magia de bruxas/evocadores | Ligado |
| Rastros de flechas | Ligado |
| Efeitos de caldeirão | Ligado |
| Gêiseres | Desligado |
| Gás de gêiseres | Desligado |
| Partículas de enxofre | Desligado |

O limite usa Math.min nas definições adaptadas de partículas para limitar picos de emissão. num_particles aceita número ou expressão Molang na documentação da Microsoft. Isso limita apenas os emissores que o LowMine substitui; partículas nativas fora desse conjunto continuam existindo.

## Auditoria estática do pacote

| Verificação | Resultado |
|---|---:|
| Entradas no .mcpack | 72 |
| JSON válidos | 21 / 21 |
| Imagens PNG | 50 |
| Texturas de bloco 8×8 | 38 |
| Definições de partículas | 14 |
| Arquivos de interface registrados | 3 |
| Arquivos de script no pacote | 0 |
| Tamanho compactado | 32.451 bytes |

SHA-256: 68635f505fc9267b480019177e6ec2a3f1095bc9b67baa4551c6672add6ec16b.

A auditoria verifica arquivos e referências; não mede FPS nem prova o comportamento no jogo. A contagem de PNGs também não equivale à quantidade de texture handles, pois o Bedrock agrupa algumas texturas de blocos em atlas.

## Instalação e primeiro teste

1. Baixe LowMine-Equilibrado-8x-v0.5.0.mcpack.
2. Abra com Minecraft Bedrock e confirme LowMine Equilibrado 8x v0.5.0.
3. Ative o pacote na lista de Recursos Globais ou nos recursos do mundo.
4. Abra as configurações do pacote e confira os sliders e toggles.
5. Teste inventário, crafting, baús, água, sombras, grama, folhas e partículas.
6. Compare com o jogo sem LowMine usando o mesmo mundo, local, resolução e distâncias.

Veja o relatório de teste em docs/TEST_REPORT_TEMPLATE.md antes de comparar resultados.

## Configuração inicial para PC modesto

Comece com **4 chunks de renderização e 4 de simulação** no computador que congela ao explorar terreno. Se ficar estável, experimente 6 chunks de renderização mantendo simulação em 4. Desative os recursos gráficos avançados disponíveis e use um limite de FPS que a máquina consiga sustentar sem oscilações grandes.

A distância de renderização controla quantos chunks o cliente desenha; a distância de simulação controla onde entidades, plantas, líquidos e outras mecânicas são atualizadas. O resource pack não consegue mudar essas opções nem pré-gerar chunks. Consulte Configuração para CPU fraca e diagnóstico de travamentos em docs/CONFIGURACAO-CPU-FRACA.md.

## Compilar e validar

Requisitos: Python 3.10+ e Pillow.

Execute na raiz do repositório:

    python -m pip install Pillow
    python tools/gerar_pacote.py
    python tools/validar_pacote.py build/LowMine-Equilibrado-8x-v0.5.0.mcpack

O GitHub Actions também compila os scripts, gera o .mcpack, executa o validador e publica um artefato de teste em cada atualização de código relevante. Consulte tools/README.md.

## Autoria, adaptações e licenças

- **Criação LowMine:** identidade, manifesto, texturas 8×8, ícone, UI, seleção de configurações e ferramentas de build/validação.
- **Material adaptado:** 14 partículas, água e sombras do FPS Optimizer v2.9.2 de XiaoCraft, sob CC BY-NC 3.0, com namespace e configuração alterados.
- **Referências sem arquivos copiados:** PotatoCraft 8x v1.4, Embeddium Optimizer v1.6 e Vanilla × Optimizer v2.4.2.

O pacote é uma composição e não reivindica a autoria das partes de terceiros. A licença não comercial do material adaptado precisa ser respeitada; portanto, não publique ou venda esta composição para obter vantagem comercial sem outra autorização. Leia CREDITOS.md e o arquivo CREDITOS.txt dentro do pacote.

## O que o pacote não faz

- Não substitui o RenderDragon.
- Não implementa frustum/occlusion culling universal.
- Não impede a geração de chunks.
- Não controla distância de renderização ou simulação.
- Não injeta Rust no cliente.

Névoa, texturas 8×8 e água/sombras alteram recursos visuais, não o código do motor. Consulte Limites do renderizador e técnicas reais em docs/LIMITES-DO-RENDERIZADOR.md.
