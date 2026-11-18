# Ferramentas de compilação e validação

O LowMine possui um construtor-base, etapas versionadas de redesign e validadores estáticos. Todos executam no computador/CI do projeto; nenhum código Python é incluído ou executado dentro do Minecraft.

## Gerar a versão 0.6.4

Requisitos: Python 3.10+ e Pillow.

Na raiz do repositório:

~~~bash
python -m pip install Pillow
python tools/gerar_pacote.py
python tools/redesenhar_v061.py
python tools/redesenhar_v063.py
python tools/finalizar_pacote_v064.py
python tools/validar_pacote_v064.py build/LowMine-Equilibrado-8x-v0.6.4.mcpack
~~~

A etapa final converte o manifesto para o formato estável 2, remove configurações Preview e zera o canal alfa das imagens de fundo, bordas, slots, toolbar e hotbar. Também ajusta screen_background_alpha em todas as telas customizadas.

Arquivo gerado:
- build/LowMine-Equilibrado-8x-v0.6.4.mcpack

## Integração contínua

O GitHub Actions compila a base, prepara as versões intermediárias, aplica o acabamento 0.6.4, valida manifesto/ZIP/dimensões/UI/transparência e publica um artefato de teste. Na branch main, cria a release lowmine-v0.6.4.

A validação estática não substitui o teste de importação e a conferência visual dentro do Bedrock.
