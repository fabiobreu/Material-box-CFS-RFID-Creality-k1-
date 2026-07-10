# Material BOX para Creality K1

Este projeto reúne os arquivos JSON usados para configurar materiais da impressora Creality K1 no formato da pasta BOX.

## Arquivos principais

- `box/material_option.json` — define as marcas e os materiais disponíveis por categoria.
- `box/material_database.json` — contém as entradas detalhadas do catálogo, incluindo ID, nome, temperaturas e parâmetros do material.
- `box/material_editor.html` — página simples para revisar e editar os dois arquivos acima.

## Objetivo

Permitir organizar, revisar e adicionar materiais de marcas como eSUN e 3DFila de forma mais prática, sem precisar editar manualmente os JSONs diretamente.

## Como usar

1. Abra o arquivo `box/material_editor.html` em um navegador moderno.
2. Carregue os dois arquivos JSON da pasta `box`.
3. Selecione um material existente e use o botão `Duplicar material selecionado` para criar entradas novas.
4. Preencha `Marca`, `Tipo`, `Nome` e `ID`.
5. Verifique se o ID não está em uso antes de salvar.
6. Exporte os arquivos e revise o JSON gerado antes de copiar para a impressora.

## Backup e segurança

- Sempre faça backup dos arquivos originais antes de substituir qualquer material.
- O editor Web não grava nada diretamente no disco; ele apenas gera arquivos para download.
- Nunca use IDs repetidos. O editor sinaliza IDs duplicados e bloqueia edição de ID ao modificar materiais existentes.
- Use `box/update_box_materials.py` apenas se você souber como executar scripts Python. Esse script já cria backups automáticos de:
  - `box/material_option.json`
  - `box/material_options.json`
  - `box/material_database.json`

## Instalação na impressora

Depois de editar e exportar os arquivos, coloque-os na impressora no caminho:

- `/usr/data/creality/userdata/box/material_option.json`
- `/usr/data/creality/userdata/box/material_database.json`

Antes de reiniciar ou usar na impressora, confirme que:

- os arquivos são válidos JSON;
- as entradas têm IDs únicos;
- as temperaturas e parâmetros estão corretos para o filamento usado.

## Aviso de responsabilidade

As alterações neste repositório e na impressora são feitas por sua conta e risco. Não há garantia de compatibilidade ou desempenho com sua impressora K1. Use este projeto apenas como ponto de partida e sempre teste materiais com cuidado em pequenas impressões antes de confiar completamente neles.

