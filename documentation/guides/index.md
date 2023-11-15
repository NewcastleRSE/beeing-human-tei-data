# Making changes to the TEI documents

## Setup
You will only need to do these steps once (or once for each computer you use in the cases of 2, 3, and 4):

1. [Register a GitHub account](./01_register_github/01_register_github.md)
1. [Install Git](./02_Install_Git/02_install_git.md)
1. [Link Oxygen to the Github repository](./03_Link_Oxygen_Github/03_Link_Oxygen_Github.md)
1. [Make sure the file is associated with the custom Schema of the project](./04_Associate_Schema/04_Associate_Schema.md)

## Making changes
These steps should be followed for **every** work session (i.e., any time you plan on making any changes to the files), or at any time you plan to make a significant change.
1. [Create a new branch](./11_Create_branch/11_create_branch.md) if you are starting a new set of changes or [Ensure you are in the correct branch](./12_ensure_correct_branch/12_ensure_correct_branch.md) if you are continuing your work from another time
    1. If you are continuing your work or returning to the main development branch, [Pull new changes to the branch](./13_Pull_new_changes/13_pull_new_changes.md)
1. Make any changes to the files
1. Add a note about your changes to the [`revisionDesc`](https://htmlpreview.github.io/?https://raw.githubusercontent.com/NewcastleRSE/beeing-human-tei-data/dev/documentation/tei_beeing_human.html#encMetaChange) portion of the TEI file.
1. [Stage and commit your changes](./14_stage_commit/14_stage_commit.md)
1. [Push your changes](./15_Pushing_Changes/15_push_changes.md) to the GitHub repository.

## Finishing a set of changes
Once you have finished a set of changes, follow these steps:

1. Make sure you have [committed the latest changes to the file](./14_stage_commit/14_stage_commit.md) and [pushed them to the remote repository](./15_Pushing_Changes/15_push_changes.md)
2. [Create a pull request](./21_create_pull_request/21_create_pull_request.md)
3. Once the pull request has been approved, [merge your branch to the `dev` branch](./22_Merge_changes/22_merge_changes.md)
4. [Move to the `dev` branch](./12_ensure_correct_branch/12_ensure_correct_branch.md) and [Pull the new changes](./13_Pull_new_changes/13_pull_new_changes.md)
5. The new changes should now be live and visible on the development view of the [Beeing Human website](https://newcastlerse.github.io/beeing-human-web/content/literature) (you might need to refresh it if you can't see the new changes).
6. If everything worked fine, you can now [delete your local branch](./23_delete_local_branch/23_delete_local_branch.md) to avoid confusion.

## Other useful stuff
1. [Using GitHub Issues to keep track of tasks and fixes](./31_Github_issues/31_github_issues.md)
1. [Navigate the TEI document using `XPath`](./32_XPath_guide/32_xpath_guide.md)
1. [Preview changes as they will be displayed](./33_preview_changes/33_preview_changes.md)

