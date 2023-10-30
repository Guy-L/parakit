

# ParaKit - Touhou Data Analysis

ParaKit is a customizable Python toolset capable of extracting nearly all gameplay relevant data from Touhou games for the purpose of helping players gain insight. Extracting game states can either be done frame-by-frame or over a span of time by specifying a duration. Once extraction is complete, the results of the specified analysis will be displayed. 

Many analyses come pre-built to help you get started, such as "graph bullet count over time", "plot all game entities" or "find the biggest bullet cluster of a given size" (see below screenshots). All the Touhou data you could need is given to you, and it's your turn to find the best ways to use it!

If you have feature requests or need help making your own custom analysis, feel free to ask Guy for support. ParaKit is meant to be useful even for those with little to no Python experience.

### [Settings Documentation](./settings.md)
### Supported games:
* DDC
* LoLK
* UM
* UDoALG

### Goals:
* Unix compatibility (for wearr)
* Polish mallet analyzer: add lasers, account for spread, more useful timing info
* Porting interface to C++
* TD support 
* MoF support 
* State saving/reloading
* Fix "Error: Operation completed successfully" Windows error
* Player bullet/bomb data?


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

A template analyzer called `AnalysisTemplate` can be found in `analysis.py`. To make your own analyzer, copy this template, give it a unique class name, and implement the `__init__()`, `step()` and `done()` methods. It'll then instantly be added to the analyzers you can select in `settings.py`.

Initialize in `__init__()` any variables you need to track during the extraction (a common property, for instance, is the "best frame" seen so far). Every time a game state is extracted (i.e. only once for single-state extraction), the `step()` method is called and passed a `GameState` object. `done()` then runs once extraction is complete. 

The full specification of the `GameState` object is found in `game_entities.py`. 

Getting the information you need should be intuitive even for novice programmers. If you're not sure how to get something done programatically, you can try to give `game_entities.py` and `AnalysisTemplate` to a language model like ChatGPT.

If the result of your analysis includes a plot of the game world, you'll want to extend `AnalysisPlot` instead of `Analysis` and implement `plot()`. There's many examples of plotting analyzers for each type of game entity. You can add any of these to your plot by calling their `plot()` method inside of your own (see `AnalysisPlotAll`). The latest recorded frame is stored in `lastframe` (though you can store any frame you want to have plotted there instead).

If you'd like to forcefully terminate sequence extraction when a certain condition is met, you can call `terminate()` in your `step()` method. `done()` will still be ran when this occurs.

State extraction over time can be a computationally heavy process, and the `exact` setting (which is on by default) will slow the game down as needed to ensure that no frame may be skipped as a result. Depending on your needs, you can speed up this process by disabling the extraction of various entities (bullets, enemies, items or lasers) in `settings.py`. States can also include screenshots if you need a visual of a particularly interesting frame (see `AnalysisMostBulletsFrame` as an example), but this behavior is off by default as it slows down extraction significantly.

You shouldn't need to edit any file other than `settings.py` and `analysis.py`.<br>If you do, feel free to send a feature request to the developers.

## Examples

### Single State Extraction

<img alt="single state extraction" src="https://cdn.discordapp.com/attachments/522639011295002626/1140864996348280952/image.png" width="600px">

<img alt="single state extraction 2" src="https://cdn.discordapp.com/attachments/522639011295002626/1140866361665531974/image.png" width="600px">


### Sequence Extraction over 50 frames:

<img alt="analysis over 50 frames" src="https://i.imgur.com/voSiS0I.png" width="300px">

### Prebuilt Analyzers

| Name / Description | Screenshot(s) |
|--|--|
| `AnalysisTemplate`<br>See [Custom Analyzers](#custom-analyzers).<br>*Requires nothing.*  | <img alt="template" src="https://cdn.discordapp.com/attachments/522639011295002626/1140885985337552946/image.png" width="5000px"> |
| `AnalysisMostBulletsFrame` <br>Finds the recorded frame which had the most bullets; saves the frame as `most_bullets.png` if screenshots are on. <br>*Only requires bullets, optionally screenshots.* | <img alt="most bullets" src="https://cdn.discordapp.com/attachments/522639011295002626/1140889040514711633/image.png" width="500px"> |
| `AnalysisBulletsOverTime` <br>Tracks the amount of bullets across time and plots that as a graph. <br>*Only requires bullets.* | <img alt="9head bullet count over time" src="https://i.imgur.com/nLY7TPQ.png"> |
| `AnalysisCloseBulletsOverTime` <br>Tracks the amount of bullets in a radius around the player across time and plots that as a graph. <br>*Only requires bullets.* | <img alt="FMH close bullets over time" src="https://i.imgur.com/o11hOLC.png">
| `AnalysisPlot` <br> Abstract base class to factorize common plotting code.<br>See [Custom Analyzers](#custom-analyzers). |  |
| `AnalysisPlotBullets` <br>Plots the bullet positions of the last frame. <br>*Only requires bullets.* | <img alt="Kudoku Gourmet" src="https://cdn.discordapp.com/attachments/522639011295002626/1140912067193352274/image.png"> |
| `AnalysisPlotEnemies` <br>Plots the enemy positions of the last frame. <br>*Only requires enemies.* |  <img alt="DDC St5 PostMid" src="https://cdn.discordapp.com/attachments/522639011295002626/1140921709713702932/image.png"> |
| `AnalysisPlotItems` <br>Plots the item positions of the last frame. <br>*Only requires items.* | <img alt="UM st2 woozy yy" src="https://cdn.discordapp.com/attachments/522639011295002626/1140893844947357736/image.png"> |
| `AnalysisPlotLineLasers` <br>Plots the line laser positions of the last frame. <br>*Only requires lasers.* | <img alt="Shimmy non 4" src="https://cdn.discordapp.com/attachments/522639011295002626/1140922776262295623/image.png"> |
| `AnalysisPlotInfiniteLasers` <br>Plots the telegraphed laser positions of the last frame. <br>*Only requires lasers.* | <img alt="Megu Final" src="https://cdn.discordapp.com/attachments/522639011295002626/1140896990440456212/image.png"> |
| `AnalysisPlotCurveLasers` <br>Plots the curvy laser positions of the last frame. <br>*Only requires lasers.* | <img alt="Sky Pendra" src="https://cdn.discordapp.com/attachments/522639011295002626/1140906836246138920/image.png"> |
| `AnalysisPlotAll` <br>Runs all the above plotting analyzers. | <img alt="DDC St4 Final" src="https://cdn.discordapp.com/attachments/522639011295002626/1140923987631808563/image.png"> |
| `AnalysisPlotBulletHeatmap` <br>Creates and plots a heatmap of bullet positions across time. <br>*Only requires bullets.* | <img alt="UM st5 fireballs enemies" src="https://cdn.discordapp.com/attachments/522639011295002626/1140902507720224788/image.png"> |
| `AnalysisPrintBulletsASCII` <br>Renders the bullet positions as ASCII art in the terminal. <br>*Only requires bullets.* | <img alt="Seki Ascii" src="https://cdn.discordapp.com/attachments/522639011295002626/1140925231171633152/image.png"> |
| `AnalysisMostBulletsCircleFrame` <br>Finds the best timing and position to convert bullets to items via the Miracle Mallet in UM, then plots the Mallet circle and prints relevant data.<br>*Only requires bullets.* | <img alt="S4 Casino" src="https://cdn.discordapp.com/attachments/522639011295002626/1140914669658325012/image.png"> |

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