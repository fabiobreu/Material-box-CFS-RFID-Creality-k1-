# Material BOX para Creality K1

Este projeto reúne os arquivos JSON usados para configurar materiais da impressora Creality K1 no formato da pasta BOX.

## Arquivos principais

- `box/material_option.json` — define as marcas e os materiais disponíveis por categoria.
- `box/material_database.json` — contém as entradas detalhadas do catálogo, incluindo ID, nome, temperaturas e parâmetros do material.
- `box/material_editor.html` — página simples para revisar e editar os dois arquivos acima.

## Objetivo

Permitir organizar, revisar e adicionar materiais de marcas como eSUN e 3DFila de forma mais prática, sem precisar editar manualmente os JSONs diretamente.

## Como usar

1. Abra o arquivo `box/material_editor.html` em um navegador.
2. Carregue os dois arquivos JSON da pasta `box`.
3. Edite os materiais e exporte os arquivos atualizados.

## Instalação na impressora

Depois de editar e exportar os arquivos, coloque-os na impressora no caminho:

- `/usr/data/creality/userdata/box/material_option.json`
- `/usr/data/creality/userdata/box/material_database.json`

Certifique-se de substituir os arquivos existentes apenas se souber o que está fazendo.

## Aviso de responsabilidade

As alterações neste repositório e na impressora são feitas por sua conta e risco. Não nos responsabilizamos por problemas, danos ou falhas causados por modificações ou por mudanças não testadas.

