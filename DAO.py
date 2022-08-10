"""
# Coinbase Institute
# DAOs
# Author: Cesare Fracassi
# Twitter: @CesareFracassi
# Email: cesare.fracassi@coinbase.com
"""

# import libraries
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.io as pio

pio.renderers.default = "svg"


#%cd '/Volumes/GoogleDrive/Shared drives/POLICY/Vertical - Thought Leadership & Engagement/Coinbase Institute/Papers Drafts/DAOs/DAO Primer Paper /Data Analysis'

#%% IMPORT DATA AND CLEANUP

df = pd.read_csv("data/DAO Organizations.csv")

# Converting all strings to floats


# TOKEN HOLDERS
df["tmp_value"] = (
    df["governance token holders"]
    .str.replace("$", "")
    .str.replace("k", "")
    .str.replace("M", "")
    .str.replace("B", "")
)
df["tmp_value"] = df["tmp_value"].astype(float)
df["n_token_holders"] = df["tmp_value"]
df.loc[df["governance token holders"].str.strip().str[-1] == "B", "n_token_holders"] = (
    df["tmp_value"] * 1000000000
)
df.loc[df["governance token holders"].str.strip().str[-1] == "M", "n_token_holders"] = (
    df["tmp_value"] * 1000000
)
df.loc[df["governance token holders"].str.strip().str[-1] == "k", "n_token_holders"] = (
    df["tmp_value"] * 1000
)


# active members
df["tmp_value"] = (
    df["active members"]
    .str.replace("$", "")
    .str.replace("k", "")
    .str.replace("M", "")
    .str.replace("B", "")
)
df["tmp_value"] = df["tmp_value"].astype(float)
df["n_active_members"] = df["tmp_value"]
df.loc[df["active members"].str.strip().str[-1] == "B", "n_active_members"] = (
    df["tmp_value"] * 1000000000
)
df.loc[df["active members"].str.strip().str[-1] == "M", "n_active_members"] = (
    df["tmp_value"] * 1000000
)
df.loc[df["active members"].str.strip().str[-1] == "k", "n_active_members"] = (
    df["tmp_value"] * 1000
)


# Proposals
df["tmp_value"] = (
    df["proposals"]
    .str.replace("$", "")
    .str.replace("k", "")
    .str.replace("M", "")
    .str.replace("B", "")
)
df["tmp_value"] = df["tmp_value"].astype(float)
df["n_proposals"] = df["tmp_value"]
df.loc[df["proposals"].str.strip().str[-1] == "B", "n_proposals"] = (
    df["tmp_value"] * 1000000000
)
df.loc[df["proposals"].str.strip().str[-1] == "M", "n_proposals"] = (
    df["tmp_value"] * 1000000
)
df.loc[df["proposals"].str.strip().str[-1] == "k", "n_proposals"] = (
    df["tmp_value"] * 1000
)

# Votes
df["tmp_value"] = (
    df["votes"]
    .str.replace("$", "")
    .str.replace("k", "")
    .str.replace("M", "")
    .str.replace("B", "")
)
df["tmp_value"] = df["tmp_value"].astype(float)
df["n_votes"] = df["tmp_value"]
df.loc[df["votes"].str.strip().str[-1] == "B", "n_votes"] = df["tmp_value"] * 1000000000
df.loc[df["votes"].str.strip().str[-1] == "M", "n_votes"] = df["tmp_value"] * 1000000
df.loc[df["votes"].str.strip().str[-1] == "k", "n_votes"] = df["tmp_value"] * 1000


# treasury
df["tmp_value"] = (
    df["treasury"]
    .str.replace("$", "")
    .str.replace("k", "")
    .str.replace("M", "")
    .str.replace("B", "")
)
df["tmp_value"] = df["tmp_value"].astype(float)
df["treasury_amt"] = df["tmp_value"]
df.loc[df["treasury"].str.strip().str[-1] == "B", "treasury_amt"] = (
    df["tmp_value"] * 1000000000
)
df.loc[df["treasury"].str.strip().str[-1] == "M", "treasury_amt"] = (
    df["tmp_value"] * 1000000
)
df.loc[df["treasury"].str.strip().str[-1] == "k", "treasury_amt"] = (
    df["tmp_value"] * 1000
)


#%% DEFINE VOTING PARTICIPATION AND PLOT

# Voting Participation = Votes / (Governance token holders * Proposals)
df["Voting Participation"] = df["n_votes"] / (df["n_token_holders"] * df["n_proposals"])
df["Voting Participation"].replace([np.inf, -np.inf], np.nan, inplace=True)
df["Voting Participation"].describe()
df["treasury_amt"].replace(0, np.nan, inplace=True)
df["n_token_holders"].replace(0, np.nan, inplace=True)


figure = px.histogram(
    df.dropna(),
    x="Voting Participation",
    nbins=50,
    range_x=(-0.02, 0.50),
    color_discrete_sequence=["#1652f0"],
)
figure.update_layout(title_text="DAO Voting Turnout", title_x=0.5)
figure.update_layout(bargap=0)
figure.update_layout(
    plot_bgcolor="#FFFFFF", font_family="sans-serif", font_size=14, font_color="#000000"
)
figure.update_xaxes(
    showgrid=True,
    gridwidth=1,
    gridcolor="DarkGrey",
    showline=True,
    linewidth=1,
    linecolor="DarkGrey",
    showticklabels=True,
)
figure.update_yaxes(
    showgrid=True, gridwidth=1, gridcolor="DarkGrey", zerolinecolor="black"
)
figure.layout.yaxis.title.text = "N. DAOs"
figure.layout.xaxis.title.text = "DAOs Average Voting Turnout"
figure.show()
figure.write_image("results/dao_hist.png")

# Plot relationship between voting turnout and DAO size treasury

figure = px.scatter(
    df.dropna(),
    x="treasury_amt",
    y="Voting Participation",
    trendline="ols",
    trendline_options=dict(log_x=True),
    log_x=True,
    trendline_color_override="red",
)
figure.update_layout(title_text="DAO Voting Turnout - DAO Size (Treasury)", title_x=0.5)
figure.update_layout(bargap=0)
figure.update_layout(
    plot_bgcolor="#FFFFFF", font_family="sans-serif", font_size=14, font_color="black"
)
figure.update_traces(marker=dict(size=6, color="#1652f0"))
figure.update_xaxes(
    showgrid=True,
    gridwidth=1,
    gridcolor="DarkGrey",
    showline=True,
    linewidth=1,
    linecolor="DarkGrey",
    showticklabels=True,
    zerolinecolor="DarkGrey",
)
figure.update_yaxes(
    showgrid=True, gridwidth=1, gridcolor="DarkGrey", zerolinecolor="black"
)
figure.layout.yaxis.title.text = "DAOs Average Voting Turnout"
figure.layout.xaxis.title.text = "DAO Size (Treasury $ Amount - Log)"
figure.show()
figure.write_image("results/dao_scatter_treasury.png")

# Plot relationship between voting turnout and DAO size members

figure = px.scatter(
    df.dropna(),
    x="n_token_holders",
    y="Voting Participation",
    trendline="ols",
    log_x=True,
    trendline_options=dict(log_x=True),
    trendline_color_override="red",
)
figure.update_layout(
    title_text="DAO Voting Turnout - DAO Size (N. Holders)", title_x=0.5
)
figure.update_layout(bargap=0)
figure.update_layout(
    plot_bgcolor="#FFFFFF", font_family="sans-serif", font_size=14, font_color="black"
)
figure.update_traces(marker=dict(size=6, color="#1652f0"))
figure.update_xaxes(
    showgrid=True,
    gridwidth=1,
    gridcolor="DarkGrey",
    showline=True,
    linewidth=1,
    linecolor="DarkGrey",
    showticklabels=True,
    zerolinecolor="DarkGrey",
)
figure.update_yaxes(
    showgrid=True, gridwidth=1, gridcolor="DarkGrey", zerolinecolor="black"
)
figure.layout.yaxis.title.text = "DAOs Average Voting Turnout"
figure.layout.xaxis.title.text = "DAO Size (N. Token Holders - Log)"
figure.show()
figure.write_image("results/dao_scatter_holders.png")

#%% HISTOGRAM OF % OF ACTIVE MEMBERS

df["perc_active_members"] = df["n_active_members"] / df["n_token_holders"]
df["perc_active_members"].describe()

#%% PIE CHARTS OF DAO TYPE

fig = px.pie(
    df,
    values="treasury_amt",
    names="Categorization",
    color="Categorization",
    color_discrete_map={
        "Protocol ": "1554f0",
        "Investment and Grant": "99b0f3",
        "Service and Social": "07297c",
        "Media": "7c7c84",
    },
    hole=0.3,
)
fig.update_layout(
    title_text="DAO Classification - By Treasury Market Cap ($)", title_x=0.5
)

fig.show()
fig.write_image("results/dao_pie_treasury.png")


df["one"] = 1

fig = px.pie(
    df,
    values="one",
    names="Categorization",
    color="Categorization",
    color_discrete_map={
        "Protocol ": "1554f0",
        "Investment and Grant": "99b0f3",
        "Service and Social": "07297c",
        "Media": "7c7c84",
    },
    hole=0.3,
)
fig.update_layout(title_text="DAO Classification - By Count", title_x=0.5)

fig.show()
fig.write_image("results/dao_pie_count.png")


treasury_df = pd.DataFrame(columns=["Category", "Treasury"])

for value in df["Categorization"].unique():
    array = []
    array.append(value)
    array.append(df.loc[df["Categorization"] == value, "treasury"].sum())
    treasury_df.loc[len(treasury_df)] = array

fig = px.pie(
    treasury_df,
    values="Treasury",
    names="Category",
    title="DAO Classification - By Treasury Market Cap ($)",
    color="Category",
    color_discrete_map={
        "Protocol ": "1554f0",
        "Investment and Grant": "99b0f3",
        "Service and Social": "07297c",
        "Media": "7c7c84",
    },
)

fig.update_traces(textposition="inside", textinfo="value+label")
fig.show()

# Create df with only organization names and launch dates
launch_df = df[["organization", "launch date"]]
# Type cast launch date to datetime
launch_df["launch date"] = pd.to_datetime(launch_df["launch date"])

# sort by launch date
launch_df = launch_df.sort_values(by="launch date")

# drop all rows with no launch date
launch_df = launch_df[launch_df["launch date"].notnull()]

# create a new column named count, set default value to 0
launch_df["count"] = 0

count = 0

# iterate through each row in df
for index, row in launch_df.iterrows():
    count += 1
    # set the value of count
    launch_df.at[index, "count"] = count

# plot without legend
figure = px.line(launch_df, x="launch date", y="count")
figure.update_traces(line=dict(color="#1652f0", width=4))
figure.update_layout(
    plot_bgcolor="#FFFFFF", font_family="sans-serif", font_size=14, font_color="#000000"
)
figure.update_xaxes(
    showgrid=True,
    gridwidth=1,
    gridcolor="DarkGrey",
    showline=True,
    linewidth=1,
    linecolor="DarkGrey",
    showticklabels=True,
)
figure.update_yaxes(showgrid=True, gridwidth=1, gridcolor="DarkGrey")
figure.update_layout(title_text="DAOs Launched Over Time", title_x=0.5)
figure.layout.yaxis.title.text = "Number of DAOs Launched"
figure.layout.xaxis.title.text = "Date"

figure.show()
figure.write_image("results/dao_line_count.png")
