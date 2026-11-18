# Ferramentas de compilação e validação

O LowMine possui um construtor reproduzível e um validador estático. Ambos executam no computador do desenvolvedor; nenhum código Python é incluído ou executado dentro do Minecraft.

## Fontes usadas no build

O arquivo `recursos/fontes_adaptadas.zlib.b64` contém um JSON compactado com os 16 recursos selecionados do FPS Optimizer v2.9.2: 14 definições de partículas, a configuração de água e a configuração de sombras. O construtor descompacta esse bundle, converte as referências de configuração para o namespace LowMine e gera os overrides finais.

As 38 texturas 8×8, o ícone e os elementos visuais da UI são gerados por código próprio LowMine. O projeto não extrai texturas dos outros três pacotes usados como referência.

## Gerar o pacote

Requisitos: Python 3.10+ e Pillow.

Na raiz do repositório:

```bash
python -m pip install Pillow
python tools/gerar_pacote.py
```

Arquivos gerados:
- `build/LowMine-Equilibrado-8x-v0.5.0.mcpack`
- `build/LowMine-Texturas-8x8-v0.5.0.png`

Para alterar os destinos:

```bash
python tools/gerar_pacote.py --saida build/teste.mcpack --previa build/previa.png
```

A implementação do construtor fica compactada em `tools/construir_pacote_impl_v050.zlib.b64`; o ponto de entrada legível é `tools/gerar_pacote.py`.

## Validar o pacote

```bash
python tools/validar_pacote.py build/LowMine-Equilibrado-8x-v0.5.0.mcpack
```

O validador confere CRC e caminhos do ZIP, manifesto v3, UUIDs, versão, créditos, 14 emissores, referências Molang, nove controles editáveis, água, sombras, registro de UI e as 38 imagens 8×8.

## Integração contínua

O GitHub Actions executa compilação, validação estática e publica um artefato de teste por 14 dias. A execução aprovada da versão 0.5.0 está em:

https://github.com/contatorzlkz-prog/low-mine/actions/runs/44287343412

A validação estática não substitui a importação e o teste visual/desempenho no Minecraft.
