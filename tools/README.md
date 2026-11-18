# Ferramentas de compilação e validação

## Gerar o pacote
O comando `tools/gerar_pacote.py` carrega a implementação compactada em `tools/construir_pacote_impl_v050.zlib.b64` e gera:
- `build/LowMine-Equilibrado-8x-v0.5.0.mcpack`
- `build/LowMine-Texturas-8x8.png`

Execute na raiz do repositório:

```bash
python -m pip install Pillow
python tools/gerar_pacote.py
```

É possível indicar outros caminhos:

```bash
python tools/gerar_pacote.py --saida build/teste.mcpack --previa build/previa.png
```

## Validar o pacote

```bash
python tools/validar_pacote.py build/LowMine-Equilibrado-8x-v0.5.0.mcpack
```

O validador confere o ZIP, manifesto v3, UUIDs, versão, créditos, configurações Molang, limites de partículas, ausência de scripts no Resource Pack, arquivos de UI e dimensões das texturas 8×8.

As implementações estão armazenadas comprimidas para manter o repositório compacto; os dois comandos acima são os pontos de entrada legíveis. Os códigos executam somente durante a compilação/validação no computador, não dentro do Minecraft.

A validação estática não substitui a importação e o teste no Minecraft.
