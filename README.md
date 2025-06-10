# Recalqula - Calculadora para projetos de recalque
Recalqula é uma calculadora web para projetos de recalque que ingere alguns dados básicos, como diâmetro e materiais das tubulações, vazão alvo, características dos fluidos, e retorna a altura manométrica e potência útil mínima para a bomba que será usada no projeto.

## Requisitos
- Python 3.13
- Navegador
- Terminal (CMD, Powershell, etc.)

## Execução
1. Baixe e extraia o projeto no seu computador ou clone o repositório usando:
```
git clone https://github.com/hossokawa/recalqula-backend.git
```
2. Abra a pasta do projeto no seu terminal
```
cd caminho/para/o/projeto
```
3a. Caso não tenha a ferramenta `uv` instalada, instale as dependências usando o pip:
```
pip install .
```
Ou se estiver usando Windows:
```
py -m pip install .
```
3b. Caso tenha `uv` instalado, basta executar este comando:
```
uv run .\manage.py runserver
```
4. Após instalar as dependências, basta executar este comando:
```
python .\manage.py runserver
```
Ou se estiver usando Windows:
```
py .\manage.py runserver
```
5. Acesse a url local mostrada no seu terminal (o padrão é http://localhost:8000)

## Funcionalidades
A calculadora cuida de todos os cálculos essenciais (conversão das unidades, perdas de carga, altura manométrica e potência útil) e dos cálculos intermediários (número de Reynolds, fator de atrito, etc.), basta inserir os dados pedidos e clicar no botão "Calcular". Após o cálculo, será mostrada uma seção com todos os resultados, intermediários e finais, obtidos para verificação do usuário caso queira ou simplesmente para ciência.
