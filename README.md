# TUMcalendar
This tool removes duplicate events and unifies event titles, description and location from your TUM calendar.

## What it actually does

### Title
The title of each event will formatted like this:

```{title of the lecture} ({type of the lecture})```

whereas `{type of lecture}` is one of the following:

* Vorlesung
* Übung
* Vorlesung/Übung
* Seminar
* Workshop
* Fachprüfung
* Modulprüfung

Examples:
* Nichtlineare Finite-Element-Methoden *(Vorlesung)* ~~(MW0620) VO, Standardgruppe~~
* Moderne Methoden der Regelungstechnik 3 *(Vorlesung)* ~~- Vorlesung - (MW0868) VO, Standardgruppe~~

~~xxx~~ denotes deleted parts and *xxx* added parts.

### Location
The location of each event will be formatted like this:

```{room number} ({room name})```

The locations of duplicate events will each be added in a new line with the same scheme.

Example:
* MW 1801 *(Ernst-Schmidt-Hörsaal)* ~~, Ernst-Schmidt-Hörsaal (5508.01.801)~~

### Description
All lecture specific stuff in the description will be kept (like chapters). Only the unnecessary parts in the following list will be removed:
* fix
* geplant
* Abhaltung
* Import

Different parts of the description will be separated with a new line.

In a new line, the description will be extended with the name of the module if is provided in the title.

Examle:
* ~~fix; Abhaltung;~~ Orbitales Rendezvous

### Duplicate events
If duplicate events i.e. events with the same title, start- and endtime are detected the unnecessary events will be ignored and the different locations will be added to the original event in a new line.

## How to use
The `master`-branch of this repository is hosted on heroku (in europe) and can be reached with [https://tumcalendar.herokuapp.com/](https://tumcalendar.herokuapp.com/). A small instruction page can be found at the [index](https://tumcalendar.herokuapp.com/).

## How to configure
The core of the app with all modifications can be found [here](TUMCalendarTools/tumtools/tools.py). Modify it as you want and send me a pull request.

## How to host and deploy
This app can be simply hosted on HEROKU as an app without modifications. Just create a new app on heroku and deploy it. The environment variable `SECRET_KEY` must be set with an arbitrary random secret key.
