# Ferramentas de compilação e validação

O LowMine possui um construtor-base, uma etapa de redesign e validadores estáticos. Todos executam no computador do desenvolvedor; nenhum código Python é incluído ou executado dentro do Minecraft.

## Gerar a versão 0.6.0

Requisitos: Python 3.10+ e Pillow.

Na raiz do repositório:

```bash
python -m pip install Pillow
python tools/gerar_pacote.py
python tools/redesenhar_v060.py
python tools/validar_pacote_v060.py build/LowMine-Equilibrado-8x-v0.6.0.mcpack
```

O primeiro comando compila a base 0.5.0. A etapa `redesenhar_v060.py` aplica 137 texturas autorais, nuvens/sol, manifesto 0.6.0 e perfil de partículas reduzido.

Arquivos gerados:
- `build/LowMine-Equilibrado-8x-v0.6.0.mcpack`
- `build/LowMine-Texturas-8x8-v0.6.0.png`

Para destinos diferentes:

```bash
python tools/redesenhar_v060.py --base build/LowMine-Equilibrado-8x-v0.5.0.mcpack --saida build/teste.mcpack --previa build/previa.png
python tools/validar_pacote_v060.py build/teste.mcpack
```

As implementações compactadas em `*_impl.zlib.b64` são fontes versionadas do projeto, descompactadas localmente pelos pontos de entrada Python.

## Integração contínua
O GitHub Actions compila, valida e publica artefato de teste por 14 dias. Na branch `main`, cria/atualiza uma pré-release com o download permanente v0.6.0.

A validação estática não substitui importação, teste visual e medição de desempenho dentro do Minecraft.
