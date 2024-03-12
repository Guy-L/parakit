# ParaKit - Touhou Data Analysis

ParaKit is a customizable Python tool and scripting framework capable of extracting nearly all gameplay relevant data from Touhou games for the purpose of helping players gain insight. Extracting game states can either be done frame-by-frame or over a span of time by specifying a duration. Once extraction is complete, the results of the specified analyzer will be displayed.

Many analyzers come pre-built to help you get started, such as "graph bullet count over time", "plot all game entities" or "find the biggest bullet cluster of a given size" (see below screenshots). All the Touhou data you could need is given to you, and it's your turn to find the best ways to use it!

If you have feature requests or need help making your own custom analyzer, feel free to ask Guy for support. ParaKit is meant to be useful even for those with little to no Python experience.

### [Settings Documentation](./settings.md)
### Supported games:
* TD
* DDC
* LoLK
* HSiFS
* WBaWC
* UM
* UDoALG

### Goals:
* Faster inter-process reads
* Built-in analyzers for dynamic entity plotting
* All-game support
* Player options data
* Player projectile data
* Bomb data (more)
* Cross-run and cross-stage extraction
* Better UX

## Setup
**Note for those not used to Git**: You can download this project as a ZIP by clicking on the green "Code" button at the top of the page or by downloading a release if a recent one is available. However, **I heavily recommend that you get a bit of experience with Git** to save you the trouble of re-downloading the project without erasing your changes each time a new version comes out. All you'll need to know is how to `clone` (download) and `pull` (update) a project.

Once you have the project (and Python) on your machine, **simply open `parakit.py` and the entire setup will be handled for you** before launching the program. Be patient, installing libraries can take a while. Please report to the developer if any issue comes up during this process.

**For experienced users:** If you'd like to run `state_reader.py` directly, you'll either need to source the virtual environment when you start a terminal or to install the required libraries on your machine directly.

To source the virtual environment:
```bash
venv\Scripts\activate #Windows only
source venv_name/bin/activate #Unix only
```
To install the libraries on your machine:
```bash
pip install -r requirements.txt
```


## Running

Edit `settings.py` to select the target game and analyzer. <br>**Documentation explaining every available setting can be found [here](./settings.md).**

**You can simply run the program by opening `parakit.py`.**<br>If you're going to use the program a lot, open a terminal window in the project's folder and run:

```bash
py parakit.py
```

The `parakit.py` script includes an automatic new-version checker and a confirmation prompt to exit the program (in case it is run in its own bash window, e.g. by double clicking the script). If this bothers you, it's possible to run `state_reader.py` directly (see the Setup section for more information). This comes with the benefit of being able to specify the extraction duration setting as a command line argument - open the below section for examples.

<details>
  <summary><b>state_reader.py CLI Examples</b></summary>

<br>When running `state_reader.py` directly, you can specify the extraction duration and `exact` settings as command line arguments. If these are specified, they'll take precedence over your settings in `settings.py`. For single-state extraction if duration isn't set in `settings.py`:
```bash
py state_reader.py
```

For single-state extraction if a different duration is set in `settings.py`:
```bash
py state_reader.py 1f
```

For sequence extraction over 500 in-game frames (value must be an integer):
```bash
py state_reader.py 500f
```

For sequence extraction over 10.5 in-game seconds (value can be decimal) without frame skips:
```bash
py state_reader.py 10.5s exact
```

For sequence extraction that continues indefinitely if not terminated some other way:
```bash
py state_reader.py infinite
```
</details>

## Custom Analyzers

**Temporary note:**
<br>**We higly recommend that you get started by looking at the GameState object specification in `game_entities.py` and simple analyzers in `analysis_examples.py`. This section will be expanded and improved for clarity at a later point. Feel free to ask if you have any questions.**

A template analyzer called `AnalysisTemplate` can be found in `analysis.py`. To make your own analyzer, copy this template, give it a unique class name, and implement the `__init__()`, `step()` and `done()` methods. It'll then instantly be added to the analyzers you can select in `settings.py`.

Initialize in `__init__()` any variables you need to track during the extraction (a common property, for instance, is the "best frame" seen so far). Every time a game state is extracted (i.e. only once for single-state extraction), the `step()` method is called and passed a `GameState` object. `done()` then runs once extraction is complete. 

The full specification of the `GameState` object is found in `game_entities.py`. 

Getting the information you need should be intuitive even for novice programmers. If you're not sure how to get something done programatically, you can try to give `game_entities.py` and `AnalysisTemplate` to a language model like ChatGPT.

If the result of your analyzer includes a plot of the game world, you'll want to extend `AnalysisPlot` instead of `Analysis` and implement `plot()`. There's many examples of plotting analyzers for each type of game entity. You can add any of these to your plot by calling their `plot()` method inside of your own (see `AnalysisPlotAll`). The latest recorded frame is stored in `lastframe` (though you can store any frame you want to have plotted there instead).

If you'd like to forcefully terminate sequence extraction when a certain condition is met, you can call `terminate()` in your `step()` method. `done()` will still be ran when this occurs.

State extraction over time can be a computationally heavy process, and the `exact` setting (which is on by default) will slow the game down as needed to ensure that no frame may be skipped as a result. Depending on your needs, you can speed up this process by disabling the extraction of various entities (bullets, enemies, items or lasers) in `settings.py`. States can also include screenshots if you need a visual of a particularly interesting frame (see `AnalysisMostBulletsFrame` as an example), but this behavior is off by default as it slows down extraction significantly.

You shouldn't need to edit any file other than `settings.py` and `analysis.py`.<br>If you do, feel free to send a feature request to the developers.

## Examples

### Single State Extraction

<img alt="single state extraction" src="https://cdn.discordapp.com/attachments/522639011295002626/1140864996348280952/image.png" width="600px">

### Sequence Extraction over 50 frames:

<img alt="analysis over 50 frames" src="https://i.imgur.com/voSiS0I.png" width="300px">

### Prebuilt Analyzers

| Name / Description | Screenshot(s) |
|--|--|
| `AnalysisTemplate`<br>See [Custom Analyzers](#custom-analyzers). | <img alt="template" src="https://github.com/Guy-L/parakit/assets/55163797/a73fb8a2-b4ac-4d96-9d07-3c30f4c2449d" width="500px"> |
| `AnalysisBulletsOverTime` <br>Tracks the amount of bullets across time and plots that as a graph. Simple example of how to make an analyzer. <br>*Uses bullets.* | <img alt="9head bullet count over time" src="https://github.com/Guy-L/parakit/assets/55163797/419df0ff-a449-41c4-9607-d83c949a6154"> |
| `AnalysisCloseBulletsOverTime` <br>Tracks the amount of bullets in a radius around the player across time and plots that as a graph. <br>*Uses bullets.* | <img alt="FMH close bullets over time" src="https://github.com/Guy-L/parakit/assets/55163797/ae30aae2-488b-4bc4-8f76-7946f5d58dc9">
| `AnalysisMostBulletsFrame` <br>Finds the recorded frame which had the most bullets; saves the frame as `most_bullets.png` if screenshots are on. <br>*Uses bullets & optionally screenshots.* | <img alt="most bullets" src="https://github.com/Guy-L/parakit/assets/55163797/194e03ad-1de5-4b20-9455-bbfc42898d0e" width="500px"> |
| `AnalysisMostBulletsCircleFrame` <br>Finds the time and position of the circle covering the most bullets. <br>*Uses bullets.* | <img alt="TD Yahoo easy most bullets circle" src="https://github.com/Guy-L/parakit/assets/55163797/2e1c65dc-393e-43a8-9329-dee6ed323f6a"> |
| `AnalysisDynamic` <br>Abstract base class to factorize common code for real-time auto-updating graphs using PyQt5.<br> |  |
| `AnalysisBulletsOverTimeDynamic` <br>Tracks the amount of bullets across time and plots that as a dynamic graph. Simple example of how to make a dynamic analyzer. <br>*Uses bullets.* | <img alt="Bullets plot, TD Yuyuko penult" src="https://github.com/Guy-L/parakit/assets/55163797/cd978d83-d87f-4380-a6ed-7d355174870c"> |
| `AnalysisItemCollectionDynamic` <br>Tracks item collection events, counts items auto-collected vs attracted manually and plots that as a dynamic graph.<br>*Uses items.* | <img alt="Item collection plot" src="https://github.com/Guy-L/parakit/assets/55163797/836e2075-012a-4dd5-94f4-5470247a3c48"> |
| `AnalysisPlot` <br> Abstract base class to factorize common plotting code.<br>See [Custom Analyzers](#custom-analyzers). |  |
| `AnalysisPlotBullets` <br>Plots the bullet positions of the last frame. <br>*Uses bullets.* | <img alt="Kudoku Gourmet" src="https://github.com/Guy-L/parakit/assets/55163797/3c955a52-819f-40b0-a82a-93356adadf29"> |
| `AnalysisPlotEnemies` <br>Plots the enemy positions of the last frame. <br>*Uses enemies.* |  <img alt="TD s5c1" src="https://github.com/Guy-L/parakit/assets/55163797/9ed6d4e2-1dac-48e2-a915-03aa112de5de"> |
| `AnalysisPlotItems` <br>Plots the item positions of the last frame. <br>*Uses items.* | <img alt="UM st2 woozy yy" src="https://github.com/Guy-L/parakit/assets/55163797/99aa15b2-84de-4220-bb96-2f0084186b6e"> |
| `AnalysisPlotLineLasers` <br>Plots the line laser positions of the last frame. <br>*Uses lasers.* | <img alt="Shimmy non 4" src="https://github.com/Guy-L/parakit/assets/55163797/71adbb99-4724-427b-a190-0e11b96d0adf"> |
| `AnalysisPlotInfiniteLasers` <br>Plots the telegraphed laser positions of the last frame. <br>*Uses lasers.* | <img alt="Megu Final" src="https://github.com/Guy-L/parakit/assets/55163797/f860e2bb-a00b-44ff-a759-aac3cb84968a"> |
| `AnalysisPlotCurveLasers` <br>Plots the curvy laser positions of the last frame. <br>*Uses lasers.* | <img alt="Score Desire Eater" src="https://github.com/Guy-L/parakit/assets/55163797/f46e37d7-28dc-425b-88b9-c09c05fe2ba7"> |
| `AnalysisPlotAll` <br>Runs all the above plotting analyzers. | <img alt="DDC St4 Final" src="https://github.com/Guy-L/parakit/assets/55163797/f7076cab-4bbb-42d9-be50-48069e103914"> |
| `AnalysisPlotBulletHeatmap` <br>Creates and plots a heatmap of bullet positions across time. <br>*Uses bullets.* | <img alt="UM st5 fireballs enemies" src="https://github.com/Guy-L/parakit/assets/55163797/71c8e758-8c02-4278-9d12-9a42ae3f82e8"> |
| `AnalysisPrintBulletsASCII` <br>Renders the bullet positions as ASCII art in the terminal. <br>*Uses bullets.* | <img alt="Seki Ascii" src="https://github.com/Guy-L/parakit/assets/55163797/fae9f00a-36dd-4576-bac6-04bd9b438050"> |
| `AnalysisPlotTD` <br>Plots the spirit item positions and Kyouko echo bounds of the last frame. Included in `AnalysisPlotAll`. <br>*Uses items & enemies.* | <img alt="Kyouko non 2" src="https://github.com/Guy-L/parakit/assets/55163797/c79dfd28-f4b8-4c29-b08b-8363e0102dde"> |
| `AnalysisPlotEnemiesSpeedkillDrops` <br>Plots enemies with color intensity based on time-based item drops, shows the current amount of speedkill drops and the remaining time to get that amount. Works with blue spirits in TD and season items in HSiFS. <br>*Uses enemies.* | <img alt="TD s4 post midboss" src="https://github.com/Guy-L/parakit/assets/55163797/9f0e0824-2a15-48da-8ce9-1b0d6dee9bb8"> |
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
