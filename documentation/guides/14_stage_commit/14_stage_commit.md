# How to: stage and commit your changes to the repository

## Introduction
[Staging](/documentation/guides/10_GitHub_Concepts/10_github_concepts.md#stage) and [commiting](/documentation/guides/10_GitHub_Concepts/10_github_concepts.md#commit) changes are the essential steps in the Git and GitHub workflow. This is when you explicitly create a recoverable point in the history of the repository. Staging and committing changes is fairly easy to do in Oxygen.

## Example
Let's say I want to make a change to our TEI file. Specifically, I want to add a `@target` to one of our `<ref>` elements.
1. First, [we ensure we are working in the correct branch](/documentation/guides/12_ensure_correct_branch/12_ensure_correct_branch.md) (in this case the branch is `add-target-ref-example`)
1. We're going to change the following `<ref>`:

> 