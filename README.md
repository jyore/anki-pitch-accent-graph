anki-pitch-accent-graph 
=======================

Add Pitch Accent Graphs to your cards quickly and easily for reinforcing pitch accent patterns during your reps.


# Installation

## Release Install

- Go to the [Releases](https://github.com/jyore/anki-pitch-accent-graph/releases) page and download the zip file for the version you want to install
- Unzip the zip file
- Copy all contents of the expanded directory into your addons folder


## Manual Install

- Ensure Python 2.7 and Pip are installed
- Browse to the Anki addons folder
- Install PIL library to the addons folder: `pip install Pillow -t .`
- Install Selenium library to the addons folder: `pip install selenium -t .`
- Clone this repository and copy the `PitchAccentGraph.py` and `pitchaccentgraph` directories to the addons folder
- Restart Anki



# Use It

## Add to Single Card

This can be done from either the Add New Card or Edit Card forms.

- Highlight the text you wish to generate a pitch accent graph for
- Click on the editor icon (<img height="16" width="16" src="pitchaccentgraph/gui/icons/icon.png"/>) or use the right-click context menu
- Verify the Expression field is correct
- Select a target destination field to place the generated pitch accent graph into
- Select "Append" to add the graph into the destination field or "Replace" to completely replace the contents of the destination field
- Click Ok to generate the graph


## Bulk add to cards

This can only be done through selecting cards in the browser.

- Open the broswer and select the cards you wish to add graphs to
- Click the Pitch Accent Graphs option from the menu bar and then select the bulk add option
- Ensure the correct source and destination fields are selected
- Select "Append" to add the graph into the destination field or "Replace" to completely replace the contents of the destination field
- Click Ok to generate graphs for the notes


> **Note:** You can only select a source and destination field that are present on all of the selected cards. If there are card types that do not have common fields, then you must modify your note selection to meet this condition.



# Styling

The graph is inserted with the following html:

    <div class="pitch_accent_graph"><img src="image_name.png"/></div>


Therefore you can use the `.pitch_accent_graph` class as a good way to target the graph in css

Sample CSS:

    .pitch_accent_graph img { 
        max-width:     100%;
        min-height:    50px;
        margin-top:    30px;
        background:    white;
        border:        solid 1px black;
        border-radius: 3px;
        padding:       8px;
    }

The sample CSS above will:
- ensure the image scales correctly without getting cutoff or skewed
- create some whitespace around the image to give it space
- fill in the background with "white"
- create arounded  border around the image
