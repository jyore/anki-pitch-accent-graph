anki-pitch-accent-graph
=======================


# Manual Install

- Ensure Python 2.7 and Pip are installed
- Browse to the Anki addons folder
- Install PIL library to the addons folder: `pip install Pillow -t .`
- Install Selenium library to the addons folder: `pip install selenium -t .`
- Clone this repository and copy the `PitchAccentGraph.py` and `pitchaccentgraph` directories to the addons folder
- Restart Anki


# Run POC

- Update line 62 of `testit.py` with expressiosn to generate a graphs for
- Restart Anki
- In Anki, click `Tools->TEST STUFF
- Click 'Go'`
- When it finishes, a tooltip will notify you of the file names of the images created
- Browse to your collection.media directory in Anki and view your files


# TODO

Items currently under development

- Generate an image for a card from New/Edit Card 
- Bulk Add images for a selection of cards 
- UI's and context menus
