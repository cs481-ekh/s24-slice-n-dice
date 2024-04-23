---
layout: default
---

# GoVizzy - 2D and 3D Molecule Vizualization

## Abstract

Computational chemistry, as the name suggests, relies heavily on software. Displaying sets
of molecules rendered in 3D and as 2D slices is a common method used by scientists to interpret
and comprehend their data. Molecular visualization programs available today are outdated, have
limited feature sets, and are not extensible due to their designs and the languages used.
GoVizzy is a modern, user and developer friendly application for molecular visualization,
built atop JupyterLab using standard Python libraries. GoVizzy is easily installed, used,
tweaked, and expanded by chemists, many of whom already use and are familiar with
Python and Jupyter. GoVizzy takes in data as standard .cube files, used by existing
applications today. The data is displayed in a manipulatable 3D graph; it can be moved,
zoomed, colored, and have elements made selectively visible. 2D slices of the visualizations
can be made as well. GoVizzy’s modern design and user interface (UI), combined with a powerful
featureset, make it an indispensable tool for computational chemistry research.

## Project Description

GoVizzy is a Python module wrapped in a Jupyter Notebook UI that allows users to view multiple
types of 3D renderings and 2D slices of molecules and atoms.

Data is entered into GoVizzy in the standard .cube file format. The user is first presented with
the slicing screen. This screen shows the 3D render of their .cube data, which can be interacted
with in real time.

image

The user can then create and view 2D slices of the data. A slice plane exists for each axis, and
each plane's visibility and location can be toggled individually. A set of three plots show the
selected slice on each axis.

image

GoVizzy also supports mesh renderings of .cube files. In mesh mode, each individual atom can have
its visibility and color set; chemical bonds are also configurable in the same way.

image

## Manual

The user manual for GoVizzy can be found [here](manual/index.md).

## GoVizzy Development

GoVizzy was developed in the spring of 2024 as a Senior Design Project by four Boise State
University Computer Science students. The project was sponsored by Dr. Oliviero Andreussi of
the Boise State University Chemistry Department.

### The Team
 - Digno Teogalbo
 - Brayden Thompson
 - Rylie Walsh
 - Matthew Oberg
