# Ferramentas de compilação

Requisitos: Python 3.10+ e Pillow.

Para gerar LOW BATATA:

~~~bash
python -m pip install Pillow
python tools/gerar_pacote.py
python tools/redesenhar_v061.py
python tools/redesenhar_v063.py
python tools/finalizar_pacote_v064.py
python tools/lowmine_batata_v065.py
python tools/validar_pacote_v065.py build/LowMine-Batata-8x-v0.6.5.mcpack
~~~

A etapa LOW BATATA cria padrões de baixa frequência, sprites de plantas em 8×8, armaduras de dois tons, overrides da interface e emissores de partículas desativados.

Arquivo final:
- build/LowMine-Batata-8x-v0.6.5.mcpack

A validação automatizada não substitui a importação e a medição de desempenho no Bedrock.
