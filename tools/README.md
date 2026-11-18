# Ferramentas de compilação e validação

O LowMine possui um construtor-base, uma etapa de redesign e validadores estáticos. Todos executam no computador/CI do projeto; nenhum código Python é incluído ou executado dentro do Minecraft.

## Gerar a versão 0.6.1

Requisitos: Python 3.10+ e Pillow.

Na raiz do repositório:

~~~bash
python -m pip install Pillow
python tools/gerar_pacote.py
python tools/redesenhar_v060.py
python tools/validar_pacote_v060.py build/LowMine-Equilibrado-8x-v0.6.0.mcpack
python tools/redesenhar_v061.py
python tools/validar_pacote_v061.py build/LowMine-Equilibrado-8x-v0.6.1.mcpack
~~~

A primeira etapa compila a base 0.5.0. A etapa v0.6.0 aplica 137 texturas de bloco autorais, vegetação, nuvens/sol e perfil de partículas. A etapa v0.6.1 refina os troncos existentes em 8×8, cria sete conjuntos de armaduras com mapas UV 64×32 e ícones pixel art 8×8 exportados em 16×16.

Arquivos gerados:
- build/LowMine-Equilibrado-8x-v0.6.1.mcpack
- build/LowMine-Preview-v0.6.1.png

Para destinos diferentes:

~~~bash
python tools/redesenhar_v061.py --base build/LowMine-Equilibrado-8x-v0.6.0.mcpack --saida build/teste.mcpack --previa build/previa.png
python tools/validar_pacote_v061.py build/teste.mcpack
~~~

As implementações compactadas em *_impl.zlib.b64 são fontes versionadas do projeto, descompactadas localmente pelos pontos de entrada Python.

## Integração contínua
O GitHub Actions compila, valida as duas etapas e publica artefatos de teste por 14 dias. Na branch main, cria uma pré-release lowmine-v0.6.1 com o MCpack e uma prévia da arte.
A validação estática não substitui importação, teste visual e medição de desempenho dentro do Minecraft.
