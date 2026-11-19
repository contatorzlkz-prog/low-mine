# Ferramentas de compilação

Requisitos: Python 3.10+ e Pillow.

A versão de recuperação 0.6.6 reaproveita os arquivos da 0.6.4 sem reprocessar seus assets:

~~~bash
python -m pip install Pillow
python tools/gerar_pacote.py
python tools/redesenhar_v061.py
python tools/redesenhar_v063.py
python tools/finalizar_pacote_v064.py
python tools/restaurar_base_v066.py
python tools/validar_restauracao_v066.py build/LowMine-Equilibrado-8x-v0.6.4.mcpack build/LowMine-Equilibrado-8x-v0.6.6.mcpack
~~~

O validador exige que todos os arquivos internos, exceto manifest.json, sejam idênticos à base 0.6.4.
