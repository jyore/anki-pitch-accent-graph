anki-pitch-accent-graph
=======================


# Manual Install

- Ensure Python 2.7 and Pip are installed
- Browse to the Anki addons folder
- Install PIL library to the addons folder: `pip install Pillow -t .`
- Clone this repository and copy the capture.py file to the addons folder.
- Restart Anki


# Run POC

- Update line 82 with an expression to generate a graph for
- Restart Anki
- In Anki, click `Tools->Test Pitch Accent Image`
- When it finishes, a popup will notify you of the file name of the image
- Browse to your collection.media directory in Anki and view your file


# TODO

Items currently under development

- Generate an image for a card from New/Edit Card 
- Bulk Add images for a selection of cards 
- UI's and context menus
