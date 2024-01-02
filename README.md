The purpose of this application is to allow developers to add decent text based diagrams to their
source code.  For example (warning.. looks like ass on github.  But looks good in vim or other
actual editor that supports a legit font):

⦃ My_diagram
╭────────────────────────╮
│                        │
│                        │
│                        │
│    Some text           │
│      here!        ╭────╯
│                   │  ∧
│                   │  │
│                   │  │
│                   │  │
╰───────────────────╯  │
                       │
                       │
                       │
                       └─────────┐
                                 │
                                 │
    ╭──────────────╮             │
    │   More text  │             │
    │    there.    │◁────────────┘
    │              │
    ╰──────────────╯
⦄

This is still a work in progress, has a few bugs, and is not ready for prime time.  To use, one
would add a tag to their source like:

// ${diagram:My_Diagram}

and then execute:

$ edit.sh MyFile.cpp:My_Diagram

A curses based editor will appear that allows one to create a diagram consisting of shapes
paths, arrows, text, etc.  When the diagram is saved, the tag within the source will be replaced
with the diagram.  The diagram can be subsquently edited and saved by invoking the edit command
again over and over.  This is possible by the creation of a supplemental MyFile.cpp.json file
containing meta-data about the diagrams that isn't contained in the diagram itself.
