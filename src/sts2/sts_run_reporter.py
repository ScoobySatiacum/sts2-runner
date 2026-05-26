import sqlite3

from pathlib import Path

import pandas as pd

import streamlit as st
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)
from PIL import Image

# breakdown of most killed by monster, per character
# which monster do we lose the most health to as a whole and per character
# Pie chart of wins per character

def create_sql_schema():
    db_path = Path('sts2_run.db')
    create_db_schmea = []
    if db_path.exists():
        with sqlite3.connect(str(db_path)) as connection:
            df = pd.read_sql('SELECT tbl_name FROM sqlite_master', connection)
            for table in df['tbl_name'].values.tolist():
                table_df = pd.read_sql(f'SELECT * FROM "{table}" LIMIT 1;', connection)
                create_db_schmea.append(pd.io.sql.get_schema(table_df, table))

    db_create_schema = Path('sts2_run_db_schmea.sql')
    db_create_schema.write_text('\n'.join(create_db_schmea))

import plotly.express as px

color_discrete_map={
                "CHARACTER.IRONCLAD": "rgb(120,29,26)",
                "CHARACTER.SILENT": "rgb(78,128,40)",
                "CHARACTER.DEFECT": "rgb(40,84,124)",
                "CHARACTER.REGENT": "rgb(232,115,55)",
                "CHARACTER.NECROBINDER": "rgb(204,110,155)"}

win_loss_query = "SELECT  p.character, r.win FROM runs r JOIN players p on r.start_time = p.run_id WHERE r.was_abandoned = 0;"
with sqlite3.connect('/Users/scoob/dev/python/sts2-runner/instance/sts2_runs.db') as connection:
    df = pd.read_sql(win_loss_query, connection)
    fig = px.pie(df, names='character', values='win', color='character', color_discrete_map=color_discrete_map)
    fig.show()