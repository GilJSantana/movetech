# Glossário Git

## Commit
Um "snapshot" (fotografia) do estado do repositório em um determinado momento,
identificado por um hash SHA único. Registra as alterações que estavam na área
de staging junto com autor, data e mensagem descritiva.

## Branch
Uma linha de desenvolvimento independente dentro do repositório. Permite
trabalhar em novas funcionalidades ou correções sem afetar o código da branch
principal (geralmente `main`) até que as mudanças estejam prontas.

## Merge
A operação que combina o histórico de commits de uma branch em outra,
unificando as alterações feitas em paralelo.

## Clone
A cópia completa de um repositório remoto (incluindo todo o histórico e
branches) para uma máquina local, feita com o comando `git clone`.

## Pull Request
Uma solicitação para que as mudanças feitas em uma branch sejam revisadas e
integradas (merged) na branch principal de um repositório. É o mecanismo
usado para revisão de código colaborativa em plataformas como o GitHub.
