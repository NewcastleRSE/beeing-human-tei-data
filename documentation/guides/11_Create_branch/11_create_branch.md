# How to: create a new branch on the GitHub repository

## Introduction
Every time you start a new task, you should create a new branch in the repository.

[Branches](/documentation/guides/10_GitHub_Concepts/10_github_concepts.md#branches) represent groups of related changes to the TEI file: for example, adding `@target` attributes to internal references marked with a `<ref>` element should all be made in the same branch. Isolating tasks means that any errors introduced during this process should be isolated from the main development branch (and therefore should not pass the [pull request](/documentation/guides/10_GitHub_Concepts/10_github_concepts.md#pull-request) review).

You can do this directly on Oxygen.

## Instructions
1. Make sure you can see the Git panel (if not, click `Tools>Git Client`)
1. In the Git Client panel, click the icon that looks like a curved line coming out of a straigth line (top right)
![branches icon]()