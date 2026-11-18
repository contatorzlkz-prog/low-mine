# Ferramentas de compilação e validação

O LowMine possui um construtor-base, etapas versionadas de redesign e validadores estáticos. Todos executam no computador/CI do projeto; nenhum código Python é incluído ou executado dentro do Minecraft.

## Gerar a versão 0.6.3

Requisitos: Python 3.10+ e Pillow.

Na raiz do repositório:

~~~bash
python -m pip install Pillow
python tools/gerar_pacote.py
python tools/redesenhar_v061.py
python tools/redesenhar_v063.py
python tools/validar_pacote_v063.py build/LowMine-Equilibrado-8x-v0.6.3.mcpack
~~~

A compilação parte da base 0.5.0, prepara a versão 0.6.2 preservada e aplica o refinamento 0.6.3. A etapa nova redesenha troncos e blocos selecionados em 8×8 e atualiza sete conjuntos de armaduras com mapas UV 64×32 e ícones pixel art 8×8 ampliados para 16×16. Os arquivos de UI transparente e os visuais de itens já existentes são mantidos.

Arquivos gerados:
- build/LowMine-Equilibrado-8x-v0.6.3.mcpack
- build/LowMine-Preview-v0.6.3.png

## Integração contínua

O GitHub Actions compila a base, prepara a versão anterior, aplica o redesign 0.6.3, valida ZIP/manifesto/dimensões/UI e publica artefatos de teste por 14 dias. Na branch main, cria a pré-release lowmine-v0.6.3 com o MCpack e a prévia da arte.

A validação estática não substitui importação, teste visual e medição de desempenho dentro do Bedrock.
