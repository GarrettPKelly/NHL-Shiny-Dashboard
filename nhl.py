import pandas as pd
import datetime
from random import randint
import seaborn as sb
import seaborn.objects as so
from shiny import ui, render, App
from shiny.types import ImgData

df2 = pd.read_csv('scraped_data.csv')
df2.drop(df2[df2['Rk'] == 'Rk'].index, inplace=True)
df2 = df2.drop_duplicates('Rk', keep='first')
df2.set_index('Rk')
df2 = df2.convert_dtypes()
df2 = df2.astype({'GP':'int32', 'G':'int32','A':'int32','PTS':'int32','+/-':'int32','PIM':'int32','PS':'float','EV':'int32','PP':'int32','SH':'int32','GW':'int32','EV.1':'int32','PP.1':'int32','SH.1':'int32','S':'int32','S%':'float','TOI':'int32','BLK':'int32','HIT':'int32','FOW':'int32','FOL':'int32' })
histogram = sb.displot(df2, x='GP', binwidth=3, hue="Pos", multiple="stack")
histogram.set_axis_labels("Games Played", "Count")
dot = so.Plot(df2, x="S", y="G", color="Pos").add(so.Dots()).add(so.Line(color="0.2"), so.PolyFit(), color=None)
dot.label(x="Shots",y="Goals")
joint = sb.jointplot(df2, x="G", y="A", hue="Pos")
joint.set_axis_labels("Goals","Assists")


app_ui = ui.page_fluid(
    ui.panel_title(
        ui.h1("NHL Skater Dashboard"),
        ui.h2("Season 2022-2023"),
    ),
    ui.layout_sidebar(
        ui.panel_sidebar(
            ui.p("This dashboard uses data scraped from ", ui.a('Hockey References ', href="https://www.hockey-reference.com/leagues/NHL_2023_skaters.html"), "to investigate the difference skater positions for the last season."),
            ui.p("The first plot is looking at the distribution of games played for each position. As you can see, the Center position players consistently see more play throughout the season compared to other positions such as Right Winger that have a more uniform distribution."),
            ui.p("In the next visual, we can see the relationship between shots and goals for a player, and how it changes based on the player’s position. One obvious takeaway is that Defenders are usually less successful at landing their shots in the goal, which makes sense since they are already focused on making sure that the puck is not on their side of the rink."),
            ui.p("Finally, this joint plot shows the distribution of Goals and Assists for players along with a scatterplot of their relationship. Defenders are once again standing out from the rest due to how many assists they get per goal made, whereas Centers and Left Wingers have nearly identical relationships. Defenders are more likely to be passing a puck to another skater who makes the actual shot, so this result is expected.")
        ),
        ui.panel_main(
            ui.navset_tab_card(
                ui.nav("Games Played",ui.output_plot("plot1", width="50%")),
                ui.nav("Shots vs Goals",ui.output_image("plot2")),
                ui.nav("Assists vs Goals",ui.output_plot("plot3", width="50%")),
            ),
        ),
    ),
)

def server(input, output, session):
    @output
    @render.plot(alt="Histogram")
    def plot1():
        return histogram
    
    @output
    @render.image
    def plot2():
        from pathlib import Path

        dir = Path(__file__).resolve().parent
        img : ImgData = {"src": str(dir / "shots.png")}
        return img
    
    @output
    @render.plot(alt="Joint Plot")
    def plot3():
        return joint
    
app = App(app_ui, server)