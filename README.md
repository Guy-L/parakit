
# ParaKit - Touhou Data Analysis

ParaKit is a customizable Python toolset capable of extracting nearly all gameplay relevant data from Touhou games for the purpose of helping players gain insight. Extracting game states can either be done frame-by-frame or over a span of time by specifying a duration. Once extraction is complete, the results of the specified analysis will be displayed. 

Many analyses come pre-built to help you get started, such as "graph bullet count over time", "plot all game entities" or "find the biggest bullet cluster of a given size" (see below screenshots). All the Touhou data you could need is given to you, and it's your turn to find the best ways to use it!

If you have feature requests or need help making your own custom analysis, feel free to ask Guy for support. ParaKit is meant to be useful even for those with little to no Python experience.

### [Settings Documentation](./settings.md)
### Supported games:
* DDC
* UM

### Goals:
* Unix compatibility
* Finish UM support: active cooldowns, lasers in mallet calculation, better mallet calculations
* Porting interface to C++
* LoLK support
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
</details>

## Custom Analyzers

A template analyzer called `AnalysisTemplate` can be found in `analysis.py`. To make your own analyzer, copy this template, give it a unique class name, and implement the `__init__()`, `step()` and `done()` methods. It'll then instantly be added to the analyzers you can select in `settings.py`.

Initialize in `__init__()` any variables you need to track during the extraction (a common property, for instance, is the "best frame" seen so far). Every time a game state is extracted (i.e. only once for single-state extraction), the `step()` method is called and passed a `GameState` object. `done()` then runs once extraction is complete. 

The full specification of the `GameState` object is found in `game_entities.py`. 

Getting the information you need should be intuitive even for novice programmers. If you're not sure how to get something done programatically, you can try to give `game_entities.py` and `AnalysisTemplate` to a language model like ChatGPT.

If the result of your analysis includes a plot of the game world, you'll want to extend `AnalysisPlot` instead of `Analysis` and implement `plot()`. There's many examples of plotting analyzers for each type of game entity. You can add any of these to your plot by calling their `plot()` method inside of your own (see `AnalysisPlotAll`). 

State extraction over time can be a computationally heavy process, and the `exact` setting (which is on by default) will slow the game down as needed to ensure that no frame may be skipped as a result. Depending on your needs, you can speed up this process by disabling the extraction of various entities (bullets, enemies, items or lasers) in `settings.py`. States can also include screenshots if you need a visual of a particularly interesting frame (see `AnalysisMostBulletsFrame` as an example), but this behavior is off by default as it slows down extraction significantly.

You shouldn't need to edit any file other than `settings.py` and `analysis.py`.<br>If you do, feel free to send a feature request to the developers.

## Examples

**Note**: This section needs updating to show off new features.

Single state extraction:

<img alt="single state extraction" src="https://i.imgur.com/mKAfFJ0.png" width="600px">

Analysis over 50 frames (`exact`):

<img alt="analysis over 50 frames" src="https://i.imgur.com/voSiS0I.png" width="300px">

Various analyses:

![9head bullet count over time](https://i.imgur.com/nLY7TPQ.png)
![FMH close bullets over time](https://i.imgur.com/o11hOLC.png)
![SUR bullet scatter plot](https://i.imgur.com/zXazVcT.png)
![Shimmy laser plot](https://cdn.discordapp.com/attachments/913211531158749227/1105889947241693396/image.png)
![Benben laser plot](https://cdn.discordapp.com/attachments/913211531158749227/1105993194233139351/image.png)
![Modded laser plot](https://cdn.discordapp.com/attachments/205514395566997514/1106354957281665034/image.png)
