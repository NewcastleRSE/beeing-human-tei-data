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
    1. If you are continuing your work or returning to the main development branch, [Pull new changes to the branch](#)
1. Make any changes to the files
1. Add a note about your changes to the [`revisionDesc`](https://htmlpreview.github.io/?https://raw.githubusercontent.com/NewcastleRSE/beeing-human-tei-data/dev/documentation/tei_beeing_human.html#encMetaChange) portion of the TEI file.
1. [Stage and commit your changes](#)
1. [Push your changes](#) to the GitHub repository.

## Finishing a set of changes
Once you have finished a set of changes, follow these steps:

1. Make sure you have [committed the latest changes to the file](#)
1. [Create a pull request](#)
1. Once the pull request has been approved, [merge your branch to the `dev` branch](#)
1. [Move to the `dev` branch](#) and [Pull the new changes](#)
1. The new changes should now be live and visible on the development view of the [Beeing Human website](https://newcastlerse.github.io/beeing-human-web/content/literature) (you might need to refresh it if you can't see the new changes).
1. If everything worked fine, you can now [delete your local branch](#) to avoid confusion.

