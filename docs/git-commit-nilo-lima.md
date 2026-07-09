# git commit

## O que é um Commit?
Um commit é um "snapshot" (fotografia) do estado do repositório em um determinado
momento. Cada commit tem um hash SHA único, um autor, uma data e uma mensagem
descrevendo a mudança.

## O que o comando `git commit` faz
Registra as alterações que estão na área de staging (adicionadas com `git add`)
como um novo commit no histórico do repositório local.

## Quando utilizar
Sempre que você concluir uma unidade lógica de trabalho (uma correção, uma
funcionalidade, um ajuste) e quiser salvar esse progresso no histórico do Git.

## Exemplo de uso
```
git add arquivo.txt
git commit -m "fix: corrige validação do formulário de login"
```

