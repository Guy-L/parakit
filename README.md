# ParaKit - Touhou Data Analysis

ParaKit is a customizable Python tool and scripting framework capable of extracting nearly all gameplay relevant data from Touhou games for the purpose of helping players gain insight. Extracting game states can either be done frame-by-frame or over a span of time by specifying a duration. Once extraction is complete, the results of the specified analyzer will be displayed.

Many analyzers come pre-built to help you get started, such as "graph bullet count over time", "plot all game entities" or "find the biggest bullet cluster of a given size" (see below screenshots). All the Touhou data you could need is given to you, and it's your turn to find the best ways to use it!

If you have feature requests or need help making your own custom analyzer, feel free to ask Guy for support. ParaKit is meant to be useful even for those with little to no Python experience.

### [Settings Documentation](./settings.md)
### Supported games:
||||||
|-|-|-|-|-|
|❌ EoSD |❌ *StB* |❌ *DS*    |❌ *ISC*     |✅ **WBaWC**  |
|❌ PCB  |❌ MoF   |❌ *GFW*   |✅ **LoLK**  |✅ **UM**     |
|❌ IN   |❌ SA    |✅ **TD**  |✅ **HSiFS** |❌ *HBM*      |
|❌ PoFV |❌ UFO   |✅ **DDC** |❌ *VD*      |✅ **UDoALG** |

### Goals:
* Faster inter-process reads
* Built-in analyzers for dynamic entity plotting
* All-game support
* Bomb data (more)
* Damage sources
* Cancel sources
* API collision check methods
* Better UX

## Installation & Setup
**Requirements:**
* **Terminal Essentials** (for Windows users):
  * Opening the terminal in a folder: https://johnwargo.com/posts/2024/launch-windows-terminal/
  * Changing the terminal's directory: https://www.geeksforgeeks.org/change-directories-in-command-prompt/
* **Python**: https://www.python.org/downloads
    * The oldest supported version is `3.7.4`. We recommend downloading the latest.
* **Git**: https://www.git-scm.com/downloads

You can check that these are correctly installed on your machine by running in the terminal:
```bash
> python --version    #any version above 3.7.4 is fine
> git --version       #any version is fine
```

Since ParaKit is not currently able to update itself but is constantly improving, **we highly recommend installing it through Git**. Instead of manually swapping out old files with new ones, you'll be able to update by simply running a command (`git pull`) when prompted to.

To install, open the terminal in the folder you'd like ParaKit to be installed in and run either:
* **via HTTPS (no setup needed)**: `git clone https://github.com/Guy-L/parakit.git`
* **via SSH (requires [setup](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account))**: `git clone git@github.com:Guy-L/parakit.git`

The rest of the setup process will be handled for you when running ParaKit for the first time. Please report to the developers if any issue comes up during this process.


## Running ParaKit
**You can simply run ParaKit by opening `parakit.py`.**

Doing so by double-clicking the script file will work. However, if you'd like to keep working in the same window, you should instead run it by opening the terminal in the ParaKit folder and running:

```bash
> python parakit.py
```

This comes with the added benefit of being able to specify three important parameters for the extraction as **command-line arguments**. If arguments are supplied, they will override the associated settings in `settings.py`. Conversely, this also means you should set those settings in `settings.py` if you intend to keep working with the same parameters.

| Setting Name | Defaults to | Details |
|-|-|-|
| `analyzer` | `AnalysisTemplate` | The **name of the analyzer** you'd like to run (case-sensitive).<br>For a list of built-in analyzers you can use out of the box, see [below section](#built-in-analyzers). |
| `ingame_duration` | single-frame extraction | The in-game duration for sequence extraction. Can be: <br>• **Frames (integer+`f`):** `100f`, `5000f`, etc.<br>• **Seconds (decimal+`s`):** `25s`, `9.5s`, etc.<br>• **Infinite**: `infinite`, `inf`, `endless`, `forever`<br>Sequence extraction can be terminted manually by pressing the termination key (which defaults to `F6`) or automatically by the running analyzer. A duration of `1` or `0` frames causes single-frame extraction, and a negative duration causes infinite sequence extraction. |
| `exact` | `False` | Whether ParaKit is allowed to **slow down the game** to ensure extraction of state data for *every single unique frame* in sequence extraction. When given as a command-line argument, can be set by specifying `exact` or unset by specifying `inexact`. |

**Example command:**
```bash
> python parakit.py AnalysisMostBulletsFrame 100f exact
```
**Note**: If the same parameter is specified multiple times, the last value will be used.

ParaKit will wait while in menus, endings, and stage transitions.<br>You can start ParaKit while in the main menu, and it will start extracting as soon as the game screen loads.

You can disable extraction of various game entities (i.e., bullets, enemies, items, lasers, player shots & the other side of the screen in PvP games) in `settings.py` to improve ParaKit's performance if the analysis you're doing doesn't require some of them. You may also enable adding game screenshots to the extracted states, though this has a significant performance and memory impact.

**<u>Documentation explaining every available setting in `settings.py` can be found [here](./settings.md).</u>**

## Custom Analyzers

**Temporary note:**
<br>**We higly recommend that you get started by looking at the GameState object specification in `game_entities.py` and simple analyzers in `analysis_examples.py`. This section will be expanded and improved for clarity at a later point. Feel free to ask if you have any questions.**

A template analyzer called `AnalysisTemplate` can be found in `analysis.py`. To make your own analyzer, copy this template, give it a unique class name, and implement the `__init__()`, `step()` and `done()` methods. It'll then instantly be added to the analyzers you can select in `settings.py`.

Initialize in `__init__()` any variables you need to track during the extraction (a common property, for instance, is the "best frame" seen so far). Every time a game state is extracted (i.e. only once for single-state extraction), the `step()` method is called and passed a `GameState` object. `done()` then runs once extraction is complete. 

The full specification of the `GameState` object is found in `game_entities.py`. 

Getting the information you need should be intuitive even for novice programmers. If you're not sure how to get something done programatically, you can try to give `game_entities.py` and `AnalysisTemplate` to a language model like ChatGPT.

If the result of your analyzer includes a plot of the game world, you'll want to extend `AnalysisPlot` instead of `Analysis` and implement `plot()`. There's many examples of plotting analyzers for each type of game entity. You can add any of these to your plot by calling their `plot()` method inside of your own (see `AnalysisPlotAll`). The latest recorded frame is stored in `lastframe` (though you can store any frame you want to have plotted there instead).

If you'd like to forcefully terminate sequence extraction when a certain condition is met, you can call `terminate()` in your `step()` method. `done()` will still be ran when this occurs.

You shouldn't need to edit any file other than `settings.py` and `analysis.py`.<br>If you do, feel free to send a feature request to the developers.

## Sample Outputs

<b>Single State Extraction</b>
A single frame's state is extracted and supplied to the selected analyzer to draw results from. The terminal output will display some information from the extracted game state, including basic state data, game-specific data, and data about the active entities in the game world. Note that the information presented in this mode is but an arbitrary sample, and that extracted states contain much more data not displayed here (see `game_entities.py`).<br>
<img alt="single state extraction in wbawc" src="https://github.com/Guy-L/parakit/assets/55163797/7e0beb25-50c8-4671-85bd-d6f07047e56a" width="600px">

<b>Sequence Extraction</b>
The analyzer will be supplied the game state extracted from each frame and will present its results once the extraction process is complete. The terminal output simply displays the extraction's progress. Note that extraction is paused while the game is paused, and that its duration can be infinite (in this case, the user should terminate it by pressing the termination key which defaults to `F6`; some analyzers may also terminate it automatically).<br>
<img alt="100f & inf sequence extraction" src="https://github.com/Guy-L/parakit/assets/55163797/984bbf31-fb5a-4612-b827-d468003b8300" width="600px">

## Built-In Analyzers

| Name / Description | Screenshot(s) |
|--|--|
| `AnalysisTemplate`<br>See [Custom Analyzers](#custom-analyzers). | <img alt="template" src="https://github.com/Guy-L/parakit/assets/55163797/a73fb8a2-b4ac-4d96-9d07-3c30f4c2449d" width="500px"> |
| `AnalysisBulletsOverTime` <br>Tracks the amount of bullets across time and plots that as a graph. Simple example of how to make an analyzer. <br>*Uses bullets.* | <img alt="9head bullet count over time" src="https://github.com/Guy-L/parakit/assets/55163797/419df0ff-a449-41c4-9607-d83c949a6154"> |
| `AnalysisCloseBulletsOverTime` <br>Tracks the amount of bullets in a radius around the player across time and plots that as a graph. <br>*Uses bullets.* | <img alt="FMH close bullets over time" src="https://github.com/Guy-L/parakit/assets/55163797/ae30aae2-488b-4bc4-8f76-7946f5d58dc9">
| `AnalysisMostBulletsFrame` <br>Finds the recorded frame which had the most bullets; saves the frame as `most_bullets.png` if screenshots are on. <br>*Uses bullets & optionally screenshots.* | <img alt="most bullets" src="https://github.com/Guy-L/parakit/assets/55163797/194e03ad-1de5-4b20-9455-bbfc42898d0e" width="500px"> |
| `AnalysisMostBulletsCircleFrame` <br>Finds the time and position of the circle covering the most bullets. <br>*Uses bullets.* | <img alt="TD Yahoo easy most bullets circle" src="https://github.com/Guy-L/parakit/assets/55163797/2e1c65dc-393e-43a8-9329-dee6ed323f6a"> |
| `AnalysisDynamic` <br>Abstract base class to factorize common code for real-time auto-updating graphs using PyQt5.<br> |  |
| `AnalysisBulletsOverTimeDynamic` <br>Tracks the amount of bullets across time and plots that as a dynamic graph. Simple example of how to make a dynamic analyzer. <br>*Uses bullets.* | <img alt="Bullets plot (UM Mike)" src="https://github.com/Guy-L/parakit/assets/55163797/f13d14b6-1b4b-459c-bd1f-3d75a99f70a2"> |
| `AnalysisItemCollectionDynamic` <br>Tracks item collection events, counts items auto-collected vs attracted manually and plots that as a dynamic graph.<br>*Uses items.* | <img alt="Item collection plot" src="https://github.com/Guy-L/parakit/assets/55163797/9620057f-810b-45c4-9497-6db5ac6425c0"> |
| `AnalysisPlot` <br> Abstract base class to factorize common plotting code.<br>See [Custom Analyzers](#custom-analyzers). |  |
| `AnalysisPlotBullets` <br>Plots the bullet positions of the last frame. <br>*Uses bullets.* | <img alt="Kudoku Gourmet" src="https://github.com/Guy-L/parakit/assets/55163797/3c955a52-819f-40b0-a82a-93356adadf29"> |
| `AnalysisPlotEnemies` <br>Plots the enemy positions of the last frame. <br>*Uses enemies.* |  <img alt="TD s5c1" src="https://github.com/Guy-L/parakit/assets/55163797/9ed6d4e2-1dac-48e2-a915-03aa112de5de"> |
| `AnalysisPlotItems` <br>Plots the item positions of the last frame. <br>*Uses items.* | <img alt="UM st2 woozy yy" src="https://github.com/Guy-L/parakit/assets/55163797/99aa15b2-84de-4220-bb96-2f0084186b6e"> |
| `AnalysisPlotLineLasers` <br>Plots the line laser positions of the last frame. <br>*Uses lasers.* | <img alt="Shimmy non 4" src="https://github.com/Guy-L/parakit/assets/55163797/71adbb99-4724-427b-a190-0e11b96d0adf"> |
| `AnalysisPlotInfiniteLasers` <br>Plots the telegraphed laser positions of the last frame. <br>*Uses lasers.* | <img alt="Megu Final" src="https://github.com/Guy-L/parakit/assets/55163797/f860e2bb-a00b-44ff-a759-aac3cb84968a"> |
| `AnalysisPlotCurveLasers` <br>Plots the curvy laser positions of the last frame. <br>*Uses lasers.* | <img alt="Score Desire Eater" src="https://github.com/Guy-L/parakit/assets/55163797/f46e37d7-28dc-425b-88b9-c09c05fe2ba7"> |
| `AnalysisPlotPlayerShots` <br>Plots the player shot positions of the last frame. <br>*Uses player shots.* | <img alt="Yatsuhashi midnon 1 w/ SakuyaA shots" src="https://github.com/Guy-L/parakit/assets/55163797/b4106047-3ed2-43af-adf7-bf80cf84c446"> |
| `AnalysisPlotAll` <br>Runs all the above plotting analyzers. | <img alt="UDoALG Sanae vs Hisami" src="https://github.com/Guy-L/parakit/assets/55163797/b9bb4a57-55b3-458d-8f4e-e9f1a667bf7d"> |
| `AnalysisPlotBulletHeatmap` <br>Creates and plots a heatmap of bullet positions across time. <br>*Uses bullets.* | <img alt="UM st5 fireballs enemies" src="https://github.com/Guy-L/parakit/assets/55163797/71c8e758-8c02-4278-9d12-9a42ae3f82e8"> |
| `AnalysisPrintBulletsASCII` <br>Renders the bullet positions as ASCII art in the terminal. <br>*Uses bullets.* | <img alt="Seki Ascii" src="https://github.com/Guy-L/parakit/assets/55163797/fae9f00a-36dd-4576-bac6-04bd9b438050"> |
| `AnalysisPatternTurbulence` <br>Calculates the ratio of codirectional to non-codirectional pattern projectiles and plots that as a dynamic graph. <br>*Uses bullets, lasers and enemies.* | <img alt="UM s1 Turbulence" src="https://github.com/Guy-L/parakit/assets/55163797/8d452dfa-b181-4dda-86a6-5d75c7d1b088" height=250px> |
| `AnalysisPlotGrazeableBullets` <br>Plots the bullet positions with ungrazeable bullets obscured. Also obscures unscopeable bullets in UDoALG, as the two are equivalent. <br>*Uses bullets.* | <img alt="Narumi spell 1" src="https://github.com/Guy-L/parakit/assets/55163797/ee571ca8-9d82-4afa-9512-39356d645f77"> |
| `AnalysisPlotTD` <br>Plots the spirit item positions and Kyouko echo bounds of the last frame. Included in `AnalysisPlotAll`. <br>*Uses items & enemies.* | <img alt="Kyouko non 2" src="https://github.com/Guy-L/parakit/assets/55163797/c79dfd28-f4b8-4c29-b08b-8363e0102dde"> |
| `AnalysisPlotEnemiesSpeedkillDrops` <br>Plots enemies with color intensity based on time-based item drops, shows the current amount of speedkill drops and the remaining time to get that amount. Works with blue spirits in TD and season items in HSiFS. <br>*Uses enemies.* | <img alt="TD s4 post midboss" src="https://github.com/Guy-L/parakit/assets/55163797/9f0e0824-2a15-48da-8ce9-1b0d6dee9bb8"> <img alt="HSiFS s1c2" src="https://github.com/Guy-L/parakit/assets/55163797/f6cef537-6bc0-449b-ba84-4508848548e0"> |
| `AnalysisHookChapterTransition` <br>Example showing how to programatically detect chapter transitions in LoLK. | <img alt="Log of chapter detected transitions" src="https://github.com/Guy-L/parakit/assets/55163797/37900ec6-0961-4f8e-9b96-121be65aa3b0"> |
| `AnalysisPlotBulletGraze` <br>Plots bullets with color intensity based on graze timer. <br>*Uses bullets.* | <img alt="EX Doremy final" src="https://github.com/Guy-L/parakit/assets/55163797/8727b316-9f84-4201-ade7-9d5e8bbb3f08"> |
| `AnalysisPlotWBaWC` <br>Plots the animal token and shield otter positions of the last frame. Included in `AnalysisPlotAll`. <br>*Uses items.* | <img alt="Keiki penult with otter hyper" src="https://github.com/Guy-L/parakit/assets/55163797/b63c14bb-b19b-4a87-8260-3df0fe8297a8"> |
| `AnalysisBestMallet` <br>Finds the best timing and position to convert bullets to items via the Miracle Mallet in UM, plots Mallet circle and prints relevant data.<br>*Uses bullets.* | <img alt="S4 Casino" src="https://github.com/Guy-L/parakit/assets/55163797/6b4b288c-6417-453c-acc7-f9f3ba0c231c"> |

## For Contributors

Add the following pre-commit hook (`pre-commit`, no extension) to `.git/hooks/` to avoid accidentally breaking the commit-based automatic version checker:

<details>
  <summary><b>pre-commit</b></summary>

```
#!/bin/sh

adjustedDate=$(date -u -d '+2 minutes' +"%Y, %-m, %-d, %-H, %-M, %-S")
sed -i "s/VERSION_DATE = datetime(.*)/VERSION_DATE = datetime($adjustedDate, tzinfo=timezone.utc)/" "version.py"
git add version.py
```
</details>