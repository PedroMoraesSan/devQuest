# ⚔ DevQuest

> **Gamify your developer journey.**

## O que é o DevQuest?

O DevQuest não é um wrapper para Git.

O DevQuest é um RPG de terminal onde o ato de programar é o próprio gameplay.

Cada ação realizada pelo desenvolvedor representa uma missão, batalha ou conquista.

A ideia é transformar atividades repetitivas do desenvolvimento de software em uma experiência divertida, recompensadora e visualmente interessante.

O projeto deve ser útil, mas principalmente prazeroso de usar.

---

# Filosofia

O projeto deve seguir alguns princípios fundamentais.

## 1. Simplicidade acima de tudo

Evitar overengineering.

Não criar abstrações antes da necessidade.

Adicionar novas camadas apenas quando a complexidade realmente justificar.

Funções simples são preferíveis a dezenas de classes.

---

## 2. UX em primeiro lugar

Cada comando precisa ser agradável de utilizar.

O terminal deve parecer um jogo.

O usuário deve sentir satisfação ao executar tarefas simples como um commit ou um push.

---

## 3. Programação é o gameplay

O desenvolvedor não joga um jogo separado.

Programar É o jogo.

Git é uma espada.

Deploy é uma batalha.

Bug é um inimigo.

Merge Conflict é um boss.

---

## 4. Cada sprint deve adicionar uma mecânica completa

Evitar criar vários sistemas incompletos.

Exemplo:

Sprint:

* Sistema completo de XP

Sprint seguinte:

* Sistema completo de Achievements

Depois:

* Sistema completo de Quests

---

# Objetivo

Criar a CLI mais divertida possível para desenvolvedores.

Misturar ferramentas como:

* Git
* Lazygit
* Pokémon
* Stardew Valley
* RPGs clássicos
* Ferramentas UNIX

---

# Stack

Python

Typer

Rich

SQLite

Git

No futuro:

Textual

PyPI

Plugins

---

# Arquitetura Atual

O projeto atualmente segue uma arquitetura simples.

```
commands/

database.py

models.py

profile.py

animations.py

ui.py

main.py
```

Ainda NÃO existe:

* Services
* Events
* Plugins
* Game Engine

Esses módulos só serão criados quando realmente necessários.

---

# Fluxo atual

```
hero init

↓

hero commit

↓

hero push

↓

hero status
```

---

# Gameplay

Toda ação do desenvolvedor representa uma mecânica do RPG.

## Commit

Representa uma batalha.

Fluxo:

```
Commit Message

↓

Prepare Battle

↓

Enemy Appears

↓

Battle

↓

Git Commit

↓

Victory

↓

XP

↓

Gold
```

---

## Push

Representa conquistar uma fortaleza.

Fluxo:

```
Prepare Siege

↓

Fortress

↓

Upload

↓

Victory

↓

XP

↓

Gold
```

---

# Inimigos

Os inimigos representam problemas reais de desenvolvimento.

Exemplos:

* Merge Conflict
* Legacy Code
* Syntax Goblin
* Production Bug
* Memory Leak
* Null Pointer
* Race Condition
* Deadlock
* Infinite Loop
* Dependency Hell
* Circular Import
* Missing Environment Variable
* Segmentation Fault
* Kernel Panic
* Zombie Process
* Flaky Test
* CI Failure
* Hotfix Demon

Cada inimigo possui:

* Nome
* XP
* Gold
* HP (futuro)

---

# Progressão

O personagem evolui conforme programa.

O jogador nunca ganha XP por ações falsas.

Toda progressão precisa estar ligada a uma atividade real do desenvolvimento.

Exemplos:

Commit

↓

XP

Push

↓

XP

Deploy

↓

XP

Merge

↓

XP

Review

↓

XP

---

# Recursos atuais

✔ Hero

✔ SQLite

✔ Git Commit

✔ Git Push

✔ XP

✔ Gold

✔ Random Enemies

✔ Terminal UI

---

# Roadmap

## v0.1

* Hero
* Commit
* Push
* SQLite
* XP
* Gold

---

## v0.2

Sistema de Progressão

* Levels
* XP Bar
* Level Up Animation
* Titles

Exemplos:

Code Apprentice

Bug Hunter

Senior Warrior

Legendary Engineer

---

## v0.3

Sistema de Combate

* Enemy HP
* Attack Animation
* Critical Hit
* Miss
* Bosses

Cada batalha deve durar poucos segundos, mas parecer um pequeno RPG.

---

## v0.4

Achievements

Exemplos:

First Commit

10 Commits

100 Commits

1000 Commits

First Push

Night Owl

Weekend Warrior

Merge Master

Bug Slayer

Legendary Hero

---

## v0.5

Daily Quests

Exemplos:

* Fazer 3 commits

* Fazer um push

* Criar uma branch

* Revisar uma PR

* Resolver um Merge Conflict

Cada missão concede recompensas.

---

## v0.6

Inventory

Itens cosméticos.

Exemplos:

Bronze Keyboard

Mechanical Keyboard

RGB Keyboard

Coffee Mug

Legendary MacBook

Rubber Duck

Golden Monitor

Cyber Sword

Nenhum item deve fornecer vantagem competitiva.

Tudo deve ser cosmético.

---

## v0.7

Shop

Comprar itens usando Gold.

Ouro é obtido apenas realizando atividades reais.

---

## v0.8

Dashboard

Interface completa utilizando Textual.

Menu principal.

Player.

Quests.

Achievements.

Inventory.

Statistics.

---

## v0.9

Developer Analytics

Mostrar estatísticas reais.

Exemplo:

Tempo programando.

Número de commits.

Linguagens mais utilizadas.

Projetos ativos.

Commits por dia.

Heatmap.

Maior streak.

Maior sequência sem falhas.

---

## v1.0

Plugin System

Git

Docker

GitHub

AWS

Terraform

Kubernetes

Jira

Linear

Cursor

Claude Code

VS Code

Cada plugin adiciona novas formas de ganhar XP.

---

# Futuro

No futuro o comando principal poderá ser apenas:

```
hero
```

Abrindo um menu interativo.

```
DevQuest

▶ Commit

  Push

  Status

  Quests

  Inventory

  Achievements

  Shop

  Exit
```

O usuário poderá navegar utilizando apenas as setas do teclado.

---

# Ideias futuras

## Hero Watch

```
hero watch
```

O DevQuest observa o repositório.

Mesmo usando comandos Git normalmente, o sistema detecta commits e pushes automaticamente.

O usuário não precisa mudar seu fluxo de trabalho.

---

## Temas

Cyberpunk

Matrix

Retro

Nord

Dracula

Catppuccin

Windows 95

---

## Sons

Opcional.

Level Up.

Critical Hit.

Achievement.

Quest Complete.

---

## Configuração

Arquivo:

```
~/.devquest/config.toml
```

Exemplo:

```
theme = "cyberpunk"

animations = true

sounds = false

default_branch = "main"
```

---

# Regras do projeto

Nunca sacrificar simplicidade por arquitetura.

Sempre priorizar UX.

Cada comando deve gerar satisfação ao ser executado.

Toda mecânica deve representar uma atividade real do desenvolvimento.

Programar deve parecer uma aventura.

O terminal deve ser o mundo do jogo.

O objetivo final é criar uma ferramenta que faça o desenvolvedor sorrir sempre que abrir o terminal.
