# FAQ - Git e GitHub

## O que é Git?

Git é um sistema de controle de versão distribuído que permite acompanhar alterações em arquivos ao longo do tempo. Ele facilita o desenvolvimento de software, permitindo que várias pessoas trabalhem no mesmo projeto de forma organizada e segura.

**Uma comparação:** Imagine um videogame com vários *save points*, que são pontos em que você salva o progresso e pode voltar para um ponto anterior caso algo dê errado. O Git faz isso com o seu código!

---

## O que é GitHub?

GitHub é uma plataforma que hospeda repositórios Git na nuvem. Além de armazenar o código, oferece recursos para colaboração, como Pull Requests, Issues, revisão de código e gerenciamento de projetos.

**Uma comparação:** Pense no Git como um caderno onde você escreve suas anotações. O GitHub é como um Google Drive desse caderno: ele guarda uma cópia online e permite que outras pessoas leiam, comentem e contribuam. É como se fosse um grande serviço de cloud para seus projetos!

---

## O que é um commit?

Um commit é um registro das alterações realizadas em um projeto. Cada commit funciona como um "checkpoint", permitindo consultar o histórico, reverter mudanças quando necessário e acompanhar a evolução do código. É importante completar seu commit com uma boa mensagem explicando o que foi feito nas suas alterações. Os commits ficam salvos no seu repositório local e só são enviados ao repositório remoto quando você utiliza o comando git push.

**Metáfora:** É como tirar uma foto da sua construção de LEGO. Se depois você desmontar uma peça por engano, basta olhar a foto para saber exatamente como estava antes, mesmo que você tenha tropeçado e destruído tudo.

---

## O que é um branch?

Um branch é uma ramificação do projeto que permite desenvolver novas funcionalidades ou corrigir problemas sem alterar diretamente a versão principal do código. Depois que o trabalho é concluído, o branch pode ser integrado ao projeto principal por meio de um merge.

**Metáfora:** Imagine uma árvore. O tronco representa a versão principal do projeto, enquanto cada galho é um lugar onde você pode testar novas ideias sem colocar o tronco em risco. Quando o trabalho em um galho está pronto, ele pode ser unido novamente ao tronco por meio de um merge.

---

## O que é um Pull Request?

Um Pull Request (PR) é uma solicitação para que as alterações feitas em um branch sejam revisadas e incorporadas a outro branch. Esse processo facilita a revisão de código, a discussão entre os desenvolvedores e ajuda a manter a qualidade do projeto, e ajuda a evitar que alterações com erros sejam incorporadas à versão principal do projeto.

**Metáfora:** É como entregar uma redação para um professor antes da versão final. Ele revisa, faz sugestões e, quando tudo estiver certo, aprova para que ela faça parte do trabalho oficial.

---

## Qual a diferença entre `git fetch` e `git pull`?

Estes comandos são importantes para sincronizar o seu repositório local com o repositório remoto:

* `git fetch` baixa as alterações do repositório remoto, mas não modifica o branch atual.
* `git pull` baixa as alterações e tenta integrá-las automaticamente ao branch em que você está trabalhando.

**Metáfora:** Imagine que seus amigos atualizaram um documento compartilhado. O `git fetch` é como baixar a versão mais recente para ler depois. O `git pull` é como baixar essa versão e já substituir automaticamente a que você estava usando.

## O que é o Merge?
O Merge (em português, mescla ou fusão) é a ação técnica de costurar duas linhas do tempo separadas no Git. Ele pega todos os commits e os une matematicamente com a ramificação de destino.
## Para que serve o Merge?
Em um ecossistema focado em automação e infraestrutura, o Merge serve para oficializar o código. Ele pega o que era apenas um rascunho ou uma proposta de melhoria e injeta na base de código da equipe. No momento em que o Merge ocorre, a sua modificação deixa de ser uma ilha isolada e passa a integrar a versão mais recente do projeto, ficando disponível para todos os outros participantes assim que eles executarem o comando git pull.
