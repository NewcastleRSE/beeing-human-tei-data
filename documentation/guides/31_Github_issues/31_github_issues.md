# How to: use GitHub issues to track fixes and changes

## Introduction
GitHub [issues](/documentation/guides/10_GitHub_Concepts/10_github_concepts.md#issues) are the best way to keep track of a project's development, needs, and bugs. You can think of Github issues as a very detailed to-do list for the project, that also allow you to link an issue to a specific [branch](/documentation/guides/10_GitHub_Concepts/10_github_concepts.md#branches), attribute responsibility, engage in discussion about the solution, etc, etc. You don't *have* to use Issues, but it is very much encouraged and best practice. Consistent use of issues also gives you a human-readable history of the project's developement.

## Create a new issue
To create a new issue, simply go to the project page [https://github.com/NewcastleRSE/beeing-human-tei-data](https://github.com/NewcastleRSE/beeing-human-tei-data) and:

1. Click on the issues tab
2. Click on the green `New issue` button
3. Select from one of the available presets. These are all pretty self-explanatory, but your most used ones will likely be:
  - **Bug report**: use this if you are creating an issue about an *correcting* something
  - **Task issue template**: use this if you are *creating* something that will *add* to the project in some way
  - The other two are 'Feature request' (normally used by people who are not part of the project development team to ask for a specific feature) and 'User story template' (which are descriptions of fictitious people who we might want to think about while developing something -- in our case it would be something like a scholarly reader, an adult with interests in bee culture, a child doing a school report, etc...)
4. All templates will come pre-populated with headings and information for you to fill. Use this as much as possible.
5. For our example, we are going to create a new task, so we select the `Task Issue Template`
6. A few things to note: issues (as well as pull requests, and generally any similar field in Github) uses Markdown for formatting text. So anything that appears between \<!-- and --> is a comment and will not be shown in the issue. You can ignore those in the pre-populated text. Other significant Markdown characters are:
  - \# for headings (the more \#\# the lower level of heading)
  - \* and \_ for text in *italic*
  - \- for bullet points
  - \[\] for tick boxes (\[x\] if they are ticked)

There's also a more [detailed markdown guide available here](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax)

7. Give the issue an intelligeble title (something like 'Add targets to cross-reference <ref>')
8. Fill in as much detail as possible, but at the very least ensure you have something in the 'Summary' section: this should be detailed and clear. You can edit later to add more information if needs be, or leave a comment to ask for clarification, initiate a discussion, etc.
9. If the task can be broken up into smaller tasks, do that in the 'What needs to be done' section -- one bullet point and checkbox for each task. In this case, it could be something like:
  - Add the xml:id of the target for all <ref>
  - Make sure they all link correctly

and you can tick the boxes as you address the issue, to keep track of progress.

10. You can ignore the 'Which user story does this task relate to?' section.
11. Delete any sections you have not used
12. Finally, you can assign someone to work on the issue, on the right-hand column, under assignees. You can assign yourself, or other members of the team.

## What to do with issues throughout development

Throughout development, you can use the issue to ask any questions, make any notes, or say anything related to the specific issue (i.e., it allows you to concentrate information about the issue, which means it can be easy to find it again if needed.)

You can also edit the 'Updates' section to give more detail throughout development.

Once you created a branch to deal with the issue, you can also link it in the 'Development' section on the right-hand side.

## What to do once development is complete?

Once you have finished working on whatever the issue is, you can close the issue -- this will make it disappear from normal view, but they remain accessible and as a record of what we worked on. There are two ways of going about it:

1. You can reference the issue on your pull request using the `Fixes #` line, and adding the issue number. Once you merge the branch, the issue will automatically close;
2. You can use the 'Close issue' button on the issue itself. If you close it this way, please reference the specific commit that closes the issue, so that it is trackable.