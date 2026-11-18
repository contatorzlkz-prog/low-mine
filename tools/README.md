# Ferramentas de compilação e validação

O LowMine possui um construtor-base, uma etapa de redesign e validadores estáticos. Todos executam no computador/CI do projeto; nenhum código Python é incluído ou executado dentro do Minecraft.

## Gerar a versão 0.6.2

Requisitos: Python 3.10+ e Pillow.

Na raiz do repositório:

~~~bash
python -m pip install Pillow
python tools/gerar_pacote.py
python tools/redesenhar_v061.py
python tools/validar_pacote_v061.py build/LowMine-Equilibrado-8x-v0.6.2.mcpack
~~~

A primeira etapa compila a base 0.5.0. A etapa v0.6.2 redesenha troncos existentes em 8×8, cria sete conjuntos de armaduras com mapas UV 64×32 e ícones pixel art 8×8 exportados em 16×16, além de espadas, arco, besta, flecha e tridente. O pacote preserva as 38 texturas de bloco já fornecidas, a interface transparente e os recursos licenciados da base.

Arquivos gerados:
- build/LowMine-Equilibrado-8x-v0.6.2.mcpack
- build/LowMine-Preview-v0.6.2.png

Para destinos diferentes:

~~~bash
python tools/redesenhar_v061.py --base build/LowMine-Equilibrado-8x-v0.5.0.mcpack --saida build/teste.mcpack --previa build/previa.png
python tools/validar_pacote_v061.py build/teste.mcpack
~~~

A geração v0.6.0 anterior não faz parte do pipeline atual porque seu bundle-fonte comprimido está inválido. As implementações compactadas permanecem versionadas para recuperação futura.

## Integração contínua
O GitHub Actions compila a base, aplica o redesign 0.6.2, valida ZIP/manifesto/dimensões/UI e publica artefatos de teste por 14 dias. Na branch main, cria uma pré-release lowmine-v0.6.2 com o MCpack e a prévia da arte.
A validação estática não substitui importação, teste visual e medição de desempenho dentro do Minecraft.
