# git pull

## O que faz
Atualiza a branch local com as mudanças que estão no repositório remoto. Na prática, é um `git fetch` (busca o que mudou no remoto) seguido de um `git merge` (junta essas mudanças na sua branch local) — feito automaticamente em um único comando.

## Quando utilizar
Sempre antes de começar a trabalhar em uma branch compartilhada (como `developer`), para garantir que você está partindo do código mais atualizado e evitar conflitos desnecessários com o que outras pessoas já enviaram.

## Exemplo de uso
```bash
git checkout developer
git pull origin developer
```

Isso baixa e aplica localmente tudo o que foi mergeado na `developer` desde a última vez que você atualizou — por exemplo, os perfis de outros alunos e os arquivos de documentação que já foram adicionados por colegas.
