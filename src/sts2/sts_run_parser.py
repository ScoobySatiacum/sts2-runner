import json
from pathlib import Path
import sqlite3
import pandas as pd

from tqdm import tqdm

import traceback

class StsRunParser:

    def __init__(self, input_path: Path, db_path: Path):

        self.input_path = input_path
        self.db_path = db_path
        self.schema_path = Path('/Users/scoob/dev/python/sts2-runner/sts2_run_db_schmea.sql')
        self.run_id = self.input_path.stem

        self.data = json.load(self.input_path.open(encoding='utf-8'))

        self.dfs: dict[str, pd.DataFrame] = {}

    def create_df_from_field(self, player: dict, field_name: str):
        df = pd.json_normalize(player, record_path=[field_name]).fillna('')
        df['player_id'] = player['id']
        df['run_id'] = self.run_id
        self.dfs[field_name] = pd.concat([self.dfs[field_name], df]).fillna('') if field_name in self.dfs else df

    def parse_players(self):
        dfs = {}
        for player in self.data['players']:

            player_df = pd.json_normalize(player).fillna('')
            # strings, badges
            #player_df['potions'] = ['; '.join(i) for i in player_df['potions'].values.tolist()]

            fields_to_df = ['deck', 'badges', 'potions']
            for field in fields_to_df:
                if field in player_df.columns:
                    self.create_df_from_field(player, field)
                    player_df.drop(field, axis=1, inplace=True)
            player_df['run_id'] = self.run_id

            props = ['props.ints']
            if props[0] in self.dfs['deck'].columns:
                props_dfs = {}
                props_dfs[props[0]] = [pd.json_normalize(i) for i in self.dfs['deck'][props[0]] if i]
                self.dfs['deck'].drop(props[0], axis=1, inplace=True)

            # parse player relics
            relics = pd.json_normalize(player, record_path=['relics']).fillna('')
            fields_to_df = ['props.cards', 'props.ints', 'props.bools', 'props.model_ids', 'props.strings', 'props.card_arrays']
            for field in fields_to_df:
                if field in relics:
                    if field not in dfs:
                        dfs[field] = []
                    if field == 'props.card_arrays':
                        field_df = pd.concat([pd.json_normalize(i, record_path=['value']) for i in relics[field].values.tolist() if i]).fillna('')
                    else:
                        field_df = pd.concat([pd.json_normalize(i) for i in relics[field].values.tolist() if i]).fillna('')
                    field_df['run_id'] = self.run_id
                    field_df['player_id'] = player['id']
                    dfs[field].append(field_df)
            relics['player_id'] = player['id']
            relics['run_id'] = self.run_id
            for field in fields_to_df:
                if field in relics.columns:
                    relics.drop(field, axis=1, inplace=True)
            
            player_df.drop('relics', axis=1, inplace=True)

            self.dfs['player_relics'] = pd.concat([self.dfs['player_relics'], relics]) if 'player_relics' in self.dfs else relics

            self.dfs['players'] = pd.concat([self.dfs['players'], player_df]) if 'players' in self.dfs else player_df

        for k, v in dfs.items():
            self.dfs[k] = pd.concat(v).fillna('')
            self.dfs[k]['run_id'] = self.run_id

    def parse_map_point_history(self):
        acts = [i.replace('ACT.', '').capitalize() for i in self.data['acts']]

        fields_to_df = ['ancient_choice', 'event_choices', 'card_choices', 'relic_choices', 'potion_choices', 'cards_removed', 'cards_transformed', 'cards_enchanted']

        dfs: dict[str, list[pd.DataFrame]] = {}

        map_point_dfs = []
        player_stats_dfs = []
        rooms_dfs = []

        for i in range(len(self.data['map_point_history'])):
            act = acts[i]
            df = pd.json_normalize(self.data['map_point_history'][i]).fillna('') # this will be a table named map_points
            df['run_id'] = self.run_id
            df['act'] = act
            df['floors'] = [f'Floor {i + 1}' for i in range(len(df))]
            df.drop(['rooms', 'player_stats'], axis=1, inplace=True)
            map_point_dfs.append(df)
            
            rooms = pd.json_normalize(self.data['map_point_history'][i], record_path=['rooms']).fillna('')
            if 'monster_ids' in rooms.columns:
                monsters = rooms['monster_ids'].values.tolist()
                new_monsters = []
                for monster in monsters:
                    if monster:
                        new_monsters.append('; '.join([m.replace('MONSTER.', '').replace('_', ' ') for m in monster]))
                    else:
                        new_monsters.append('')
                rooms['monster_ids'] = new_monsters
                rooms['run_id'] = self.run_id

            rooms_dfs.append(rooms)
            
            player_stats = pd.json_normalize(self.data['map_point_history'][i], record_path=['player_stats']).fillna('')
            player_stats['run_id'] = self.run_id

            for field in fields_to_df:
                if field in player_stats:
                    if field not in dfs:
                        dfs[field] = []
                    field_df = pd.concat([pd.json_normalize(i) for i in player_stats[field].values.tolist() if i]).fillna('')
                    field_df['run_id'] = self.run_id
                    dfs[field].append(field_df)

            fields_to_str = ['relics_removed', 'rest_site_choices', 'potion_used', 'upgraded_cards', 'bought_relics', 'completed_quests', 'bought_colorless', 'bought_potions', 'downgraded_cards', 'potion_discarded']

            for field in fields_to_str:
                if field in player_stats.columns:
                    player_stats[field] = ['; '.join(i) for i in player_stats[field].values.tolist()]

            if 'cards_gained' in player_stats.columns:
                cards_gained = player_stats['cards_gained'].values.tolist()
                new_cards = []
                for cards in cards_gained:
                    if cards:
                        new_cards.append('; '.join([i['id'].replace('CARD.', '') for i in cards]))
                    else:
                        new_cards.append('')
                player_stats['cards_gained'] = new_cards

            for field in fields_to_df:
                if field in player_stats.columns:
                    player_stats.drop(field, axis=1, inplace=True)
            player_stats_dfs.append(player_stats)

        self.dfs['map_point'] = pd.concat(map_point_dfs)
        self.dfs['rooms'] = pd.concat(rooms_dfs)
        self.dfs['player_stats'] = pd.concat(player_stats_dfs)

        for k, v in dfs.items():
            self.dfs[k] = pd.concat(v).fillna('')
            self.dfs[k]['run_id'] = self.run_id

        if 'card_choices' in self.dfs:
            card_props_df = pd.DataFrame()
            if 'card.props.ints' in self.dfs['card_choices'].columns:
                card_props_df = pd.concat([pd.json_normalize(i) for i in self.dfs['card_choices']['card.props.ints'].values.tolist() if i])
                card_props_df['run_id'] = self.run_id
                self.dfs['card_choices'].drop('card.props.ints', axis=1, inplace=True)
            self.dfs['card_props'] = card_props_df

        if 'relic_choices' in self.dfs:
            relics_props_df = pd.DataFrame()
            if 'props.ints' in self.dfs['relic_choices'].columns:
                relics_props_df = pd.concat([pd.json_normalize(i) for i in self.dfs['relic_choices']['props.ints'].values.tolist() if i])
                relics_props_df['run_id'] = self.run_id
                self.dfs['relic_choices'].drop('props.ints', axis=1, inplace=True)
            self.dfs['relics_props'] = relics_props_df

            relics_models_df = pd.DataFrame()
            if 'props.model_ids' in self.dfs['relic_choices'].columns:
                relics_models_df = pd.concat([pd.json_normalize(i) for i in self.dfs['relic_choices']['props.model_ids'].values.tolist() if i])
                relics_models_df['run_id'] = self.run_id
                self.dfs['relic_choices'].drop('props.model_ids', axis=1, inplace=True)
            self.dfs['relics_models'] = relics_models_df

        if 'cards_removed' in self.dfs:
            card_removed_props_df = pd.DataFrame()
            if 'props.ints' in self.dfs['cards_removed'].columns:
                card_removed_props_df = pd.concat([pd.json_normalize(i) for i in self.dfs['cards_removed']['props.ints'].values.tolist() if i])
                card_removed_props_df['run_id'] = self.run_id
                self.dfs['cards_removed'].drop('props.ints', axis=1, inplace=True)          
            self.dfs['card_removed_props'] = card_removed_props_df

        if 'cards_transformed' in self.dfs:
            card_transformed_df = pd.DataFrame()
            if 'final_card.props.ints' in self.dfs['cards_transformed'].columns:
                card_transformed_df = pd.concat([pd.json_normalize(i) for i in self.dfs['cards_transformed']['final_card.props.ints'].values.tolist() if i])
                card_transformed_df['run_id'] = self.run_id
                self.dfs['cards_transformed'].drop('final_card.props.ints', axis=1, inplace=True)          
            self.dfs['cards_transformed'] = card_transformed_df

    def parse_run_metadata(self):
        run_data = {}
        fields_to_ignore = ['map_point_history', 'acts', 'players', 'modifiers']
        for k, v in self.data.items():
            if k not in fields_to_ignore:
                run_data[k] = v
            if k == 'modifiers':
                if self.data['modifiers']:
                    self.dfs['run_modifiers'] = pd.json_normalize(self.data, record_path=['modifiers']).fillna('')
                    if 'props.model_ids' in self.dfs['run_modifiers']:
                        self.dfs['run_modifiers_model_ids'] = pd.concat([pd.json_normalize(i) for i in self.dfs['run_modifiers']['props.model_ids'].values.tolist() if i])
                        self.dfs['run_modifiers_model_ids']['run_id'] = self.run_id
                        self.dfs['run_modifiers'].drop('props.model_ids', axis=1, inplace=True)
                    self.dfs['run_modifiers']['run_id'] = self.run_id

        self.dfs['runs'] = pd.DataFrame([run_data])

    def create_db(self):
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.db_path) as connection:
            connection.cursor().executescript(self.schema_path.read_text())

    def load_to_db(self):
        if not self.db_path.exists():
            self.create_db()
        with sqlite3.connect(self.db_path) as connection:
            for k, v in self.dfs.items():
                if not v.empty:
                    try:
                        current_table = pd.read_sql(f"select * from sqlite_master WHERE tbl_name = '{k}'", connection)
                        
                        field_renames: dict[str, str] = {}
                        for field in list(v.columns):
                            if '.' in field:
                                if field not in field_renames:
                                    field_renames[field] = field.replace('.', '_')
                        if field_renames:
                            v.rename(columns=field_renames)
                        if current_table.empty:
                            v.to_sql(k, connection, index=False)
                        else:
                            current_table = pd.read_sql(f'SELECT * FROM "{k}"', connection)
                            new_df = pd.concat([current_table, v])
                            try:
                                new_df.to_sql(k, connection, if_exists='replace', index=False)
                            except Exception as e:
                                print(list(current_table.columns))
                                print(list(self.dfs[k].columns))
                                print(e)
                                print(traceback.format_exc())
                                raise
                        #v.to_sql(f'{self.run_id}_{k}', connection, if_exists='append')
                    except pd.errors.DatabaseError as e:
                        print(e)
                        print(traceback.format_exc())
                        raise

def get_run_ids(db_path: Path) -> list[str]:
    output: list[str] = []
    if db_path.exists():
        with sqlite3.connect(db_path) as connection:
            df = pd.read_sql('SELECT start_time FROM runs', connection)
            output = [str(i) for i in df['start_time'].values.tolist()]

    return output

if __name__ == '__main__':

    runs_location = Path('/Users/scoob/Library/Application Support/SlayTheSpire2/steam/76561197989393831/profile2/saves/history') # Path to your saves
    db_path = Path('instance/sts2_runs.db') # creates an instance next to the location the script is running instance/sts2_runs.db. Change as needed.
    run_files = [i for i in runs_location.glob('*')]

    run_ids = get_run_ids(db_path)
    runs_to_parse = []
    if run_ids:
        run_file_ids = {str(i.stem) : i  for i in run_files}
        for run_id in run_file_ids:
            if run_id not in run_ids:
                runs_to_parse.append(run_file_ids[run_id])
    for run_file in tqdm(runs_to_parse):
        sts = StsRunParser(run_file, db_path)
        sts.parse_run_metadata()
        sts.parse_map_point_history()
        sts.parse_players()

        sts.load_to_db()