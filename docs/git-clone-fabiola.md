# Documentação de Comandos Git: `git clone`

## Questões Fundamentais sobre o Git

* **Quem criou o Git?**
  Foi criado por Linus Torvalds (o mesmo criador do núcleo do sistema operativo Linux).
* **Em que ano foi lançado?**
  No ano de 2005.
* **O que significa SHA?**
  Significa *Secure Hash Algorithm*. No Git, é um código alfanumérico único (uma impressão digital criptográfica) gerado para identificar de forma exclusiva cada modificação e garantir a integridade dos dados.
* **O que é um Commit?**
  É um registo oficial (um *snapshot* ou fotografia) do estado dos seus ficheiros num determinado momento da linha do tempo. Ele sela as alterações num pacote seguro que pode ser recuperado no futuro.

---

## O Comando: `git clone`

* **O que faz:**
  Faz o descarregamento completo de um repositório que está num servidor remoto (como o GitHub) para a máquina local. Ele copia todos os ficheiros, todas as ramificações (*branches*) e todo o histórico de *commits* de uma só vez, preparando automaticamente o ambiente de rastreio.

* **Quando utilizar:**
  Deve ser utilizado sempre que precisar de trabalhar num projeto existente pela primeira vez na sua máquina local. Na arquitetura em nuvem, é o pilar do método "Nuvem Primeiro", garantindo que a infraestrutura nasça corretamente alinhada com o servidor remoto, evitando divergências de históricos.

* **Um exemplo de uso:**
  ```bash
  git clone [https://github.com/usuario/nome-do-repositorio.git](https://github.com/usuario/nome-do-repositorio.git)