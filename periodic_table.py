import pandas as pd
from bokeh.plotting import figure, output_file, save
from bokeh.transform import dodge, factor_cmap
from bokeh.io import export_png


periods = ["I", "II", "III", "IV", "V", "VI", "VII"]
groups = [str(x) for x in range(1, 19)]
df = pd.read_csv('Element_information.csv', dtype={'abundance(mg/kg)':object, 'price(USD/kg)':object})
df["group"] = df["group"].astype(str)
df["period"] = [periods[x-1] for x in df.period]
df = df[df.group != "-"]
df = df[df.symbol != "Lr"]
df = df[df.symbol != "Lu"]

cmap = {
    "alkali metal"         : "#a6cee3",
    "alkaline earth metal" : "#1f78b4",
    "metal"                : "#d93b43",
    "halogen"              : "#999d9a",
    "metalloid"            : "#e08d49",
    "noble gas"            : "#eaeaea",
    "nonmetal"             : "#f1d4Af",
    "transition metal"     : "#599d7A",
}

TOOLTIPS = [
    ("Price (USD/kg)", "@{price(USD/kg)}"),
    ("Abundance (mg/kg)", "@{abundance(mg/kg)}"),
    ("Availability", "@availability")
]

p = figure(title="Availability Periodic Table (omitting LA and AC Series)", width=1520, height=675,
           x_range=groups, y_range=list(reversed(periods)),
           tools="hover", toolbar_location=None, tooltips=TOOLTIPS)

r = p.rect("group", "period", 0.95, 0.95, source=df, fill_alpha=0.6, legend_field="metal",
           color=factor_cmap('metal', palette=list(cmap.values()), factors=list(cmap.keys())))

text_props = dict(source=df, text_align="left", text_baseline="middle")

x = dodge("group", -0.4, range=p.x_range)

p.text(x=x, y=dodge("period", 0.05, range=p.y_range), text="symbol", text_font_style="bold", text_font_size="18px", **text_props)

p.text(x=x, y=dodge("period", 0.3, range=p.y_range), text="atomic number",
       text_font_size="12px", **text_props)

p.text(x=x, y=dodge("period", -0.19, range=p.y_range), text="price(USD/kg)",
       text_font_size="11px", **text_props)

p.text(x=x, y=dodge("period", -0.35, range=p.y_range), text="name",
       text_font_size="10px", **text_props)

p.text(x=["3", "3"], y=["VI", "VII"], text=["LA", "AC"], text_align="center", text_baseline="middle")

p.toolbar_location = None
p.outline_line_color = None
p.grid.grid_line_color = None
p.axis.axis_line_color = None
p.axis.major_tick_line_color = None
p.axis.major_label_standoff = 0
p.legend.orientation = "horizontal"
p.legend.location ="top_center"
p.legend.margin = 18
p.legend.label_text_font_size = "15px"
p.legend.label_standoff = 3
p.legend.spacing = 6
p.legend.glyph_height = 22
p.legend.glyph_width = 22
p.hover.renderers = [r] # only hover element boxes

# set output to static HTML file
output_file(filename="Availability_periodic_table.html", title="Availability Periodic Table")
save(p)

# save the results to a file
export_png(p, filename="Availability_periodic_table.png")