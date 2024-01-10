
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def read_export_import_data(filename):
    """
    Read merchandise data from a CSV file and preprocess it.

    Parameters:
    filename (str): The path to the CSV file containing merchandise data.

    Returns:
    pd.DataFrame: Preprocessed merchandise data.
    """
    merchandise_data = pd.read_csv(filename).iloc[:-10]
    merchandise_data.drop(columns=['Country Code', 'Series Code'], 
                          inplace=True)
    merchandise_data.columns = [col.split(' ')[0] 
                                for col in merchandise_data.columns]
    return merchandise_data

background_color = 'plum'

sns.set(style="whitegrid", palette="pastel", context='talk')

plt.rcParams.update({
    'font.size': 20,
    'axes.titleweight': 'bold',
    'font.family': 'sans-serif',
    'axes.labelweight': 'bold',
    'figure.facecolor': background_color,
    'axes.facecolor': background_color,
    'savefig.facecolor': background_color
})

plt.figure(figsize=(45, 45))

fig, axs = plt.subplots(2, 2, figsize=(40, 20))
plt.subplots_adjust(left=0.05, bottom=0.1, right=0.6, top=0.9, wspace=0.3,
                    hspace=0.4)

def line_plot_creation(ax, data, countries, indicator, years):
    """
    Create line plots showing merchandise values for specific indicators 
    across different years for selected countries.

    Parameters:
    ax (matplotlib.axes.Axes): The Axes object for plotting.
    data (pd.DataFrame): Merchandise data.
    countries (list): List of countries for plotting.
    indicator (str): The merchandise indicator for visualization.
    years (list): List of years for which data will be plotted.
    """
    colors = ['red', 'dodgerblue', 'lawngreen', 'k']
    for i, year in enumerate(years):
        values = data.loc[(data['Series'] == indicator) 
                          & (data['Country'].isin(countries)),
                          year].values.tolist()
        values = pd.to_numeric(values, errors='coerce') / 1e1
        ax.plot(countries, values, marker='D', label=f'{year}',
                color=colors[i])

    ax.set_title(f'{indicator} (American Countries)', pad=15, fontsize=30)
    sns.set_style("dark")
    ax.set_xlabel('Country', fontsize=20)
    ax.set_ylabel('Value (in 10^10)', fontsize=20)
    ax.legend()
    ax.grid(True)

def horizontal_bar_plot_creation(ax, data, countries, indicator, years):
    """
    Create horizontal bar plots illustrating merchandise values for
    specific indicators across different years for selected countries.

    Parameters:
    ax (matplotlib.axes.Axes): The Axes object for plotting.
    data (pd.DataFrame): Merchandise data.
    countries (list): List of countries for plotting.
    indicator (str): The merchandise indicator for visualization.
    years (list): List of years for which data will be plotted.
    """
    bar_height = 0.20
    bar_positions = np.arange(len(countries))

    colormap = plt.cm.viridis

    for i, year in enumerate(years):
        values = data.loc[(data['Series'] == indicator) 
                          & (data['Country'].isin(countries)),
                          year].values.tolist()
        values = pd.to_numeric(values, errors='coerce')
        values_billions = [val / 1_000_000_000 for val in values]

        bars = ax.barh(bar_positions + i * (bar_height), values_billions, 
                       height=bar_height, label=f'{year}', 
                       color=colormap(i / len(years)), edgecolor='k')

        for bar, value in zip(bars, values_billions):
            formatted_value = f'{value:.1f}B' if value >= 1 else f'{value * 1000:.1f}M'
            ax.text(bar.get_width(), bar.get_y() + bar.get_height() / 2, 
                    formatted_value, ha='left', va='center', color='k',
                    fontsize=20)

    ax.set_title(f'{indicator} (Asian Countries)', pad=27, fontsize=30)
    sns.set_style("dark")
    ax.set_xlabel('Value (in Billions)', fontsize=20)
    ax.set_ylabel('Country', fontsize=20)
    ax.set_yticks(bar_positions + ((len(years) - 1) * (bar_height)) / 2)
    ax.set_yticklabels(countries)
    ax.legend()
    ax.grid()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

def create_merchandise_pie_chart(ax, data, countries, indicator, year,
                                 chart_type):
    """
    Create pie charts displaying the distribution of 
    merchandise values for specific indicators in a 
    given year among selected countries.

    Parameters:
    ax (matplotlib.axes.Axes): The Axes object for plotting.
    data (pd.DataFrame): Merchandise data.
    countries (list): List of countries for plotting.
    indicator (str): The merchandise indicator for visualization.
    year (str): The year for which data will be visualized.
    chart_type (str): Type of merchandise chart ('exports' or 'imports').
    """
    values = data.loc[(data['Series'] == indicator)
                      & (data['Country'].isin(countries)), 
                      year].values.tolist()
    values = pd.to_numeric(values, errors='coerce')

    explode = [0.1] * len(countries)

    colormap = plt.cm.Set3 if chart_type == 'exports' else plt.cm.prism

    ax.pie(values, labels=countries, explode=explode, autopct='%1.1f%%',
           shadow=True, startangle=140,
           colors=colormap(np.linspace(0, 1, len(countries))))

    chart_title = 'Exports to economies in the Arab World' if chart_type == 'exports' else 'Imports from economies in the Arab World'

    ax.set_title(f'{chart_title} in {year}', pad=20, fontsize=30)
    centre_circle = plt.Circle((0, 0), 0.40, fc='white')
    ax.add_artist(centre_circle)
    ax.text(0, 0, f'{chart_type.capitalize()}', ha='center', va='center', 
            fontsize=25, color='black', weight='bold')
    ax.axis('equal')

filename = "MerchandiseData.csv"

merchandise_data = read_export_import_data(filename)

arab_countries = ['Saudi Arabia', 'Bahrain', 'Iraq',
                  'Qatar', 'Libya', 'Kuwait']
european_countries = ['France', 'Germany', 'Italy', 'Poland', 'Spain']
asian_countries = ['China', 'India', 'Japan', 'Malaysia', 'Singapore']
american_countries = ['Colombia', 'Brazil', 'Canada',
                      'Chile', 'Argentina', 'Mexico']

year_list = ['2010', '2011', '2012', '2013']
indicators_list = ['Merchandise exports (current US$)',
                   'Merchandise exports to economies in the Arab World (% of total merchandise exports)',
                   'Merchandise imports (current US$)',
                   'Merchandise imports from economies in the Arab World (% of total merchandise imports)']

line_plot_creation(axs[0, 0], merchandise_data, american_countries, 
                   'Merchandise exports (current US$)', year_list)
horizontal_bar_plot_creation(axs[0, 1], merchandise_data, asian_countries,
                             'Merchandise imports (current US$)', year_list)
create_merchandise_pie_chart(axs[1, 0], 
                             merchandise_data, arab_countries,
                             'Merchandise exports to economies in the Arab World (% of total merchandise exports)', '2015', 'exports')
create_merchandise_pie_chart(axs[1, 1], 
                             merchandise_data, arab_countries,
                             'Merchandise imports from economies in the Arab World (% of total merchandise imports)', '2015', 'imports')

plt.suptitle('Growth of Merchandise Trade in the Regions 2010-2015',
             fontsize=40, weight='bold')

details_params = {
    'facecolor': '#add8e6',
    'alpha': 0.7,
    'edgecolor': 'black',
    'boxstyle': 'round,pad=1'
}

description_text = """
Objective of the Plots:

The Merchandise value of goods exported by American nations grew gradually, rising from 70 billion in 2010 to 458 billion in 2013. Canada is a major exporter of goods, with 387 billion in 2010 and 458 billion in 2013.

Asian countries are gradually increasing their imports of goods across all regions, but China is the region's leading importer in 2010, the value of its imports was $1369 billion, but in 2013, it jumped to $1950 billion.

In 2015, the percentage of goods exported and imported by the Arab countries' economies had significant consequences.
Saudi Arabia exports 67.1% of its commodities, but only imports 33.4% of them. In terms of economics, Kuwait is the second-largest Arab exporter, accounting for 10.4% of global goods.

In the Arab world's economy in 2015, 50.7% of imports were sourced from Qatar, Libya, and Iraq.

Data Source: World Bank Data
"""

details = "Name : Susairaj Anthony\nStudent ID : 22071718"

font_props = {'fontsize': 40, 'weight': 'bold', 'family': 'sans-serif'}

plt.figtext(0.70, 0.1, details, ha='left', va='center', 
            fontdict=font_props, bbox=details_params)

description_font_props = {'fontsize': 35, 'family': 'sans-serif',
                          'weight': 'bold'}

plt.figtext(0.60, 0.3, description_text, ha='left', va='bottom',
            fontdict=description_font_props, wrap=True)

plt.tight_layout(pad=2, rect=[0, 0, 0.6, 1])
plt.subplots_adjust(top=0.90)

#plt.savefig("22071718.png", dpi=300, bbox_inches='tight')

plt.show()




