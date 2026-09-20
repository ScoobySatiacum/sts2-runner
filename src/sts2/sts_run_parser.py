import argparse
import json
import sqlite3
from pathlib import Path

import pandas as pd
from tqdm import tqdm


class StsRunParser:

    def __init__(self, input_path: Path, db_path: Path):
        self.input_path = input_path
        self.db_path = db_path
        self.schema_path = self._default_schema_path()
        self.run_id = self.input_path.stem

        self.data = json.load(self.input_path.open(encoding="utf-8"))

        self.dfs: dict[str, pd.DataFrame] = {}

    @staticmethod
    def _default_schema_path() -> Path:
        return Path(__file__).resolve().parent.parent.parent / "sts2_run_db_schema.sql"

    # ------------------------------------------------------------------
    # generic dataframe helpers
    # ------------------------------------------------------------------

    def _append_df(self, key: str, df: pd.DataFrame) -> None:
        """Concatenate ``df`` into ``self.dfs[key]``, filling NaN with empty strings."""
        if df.empty:
            return
        if key in self.dfs and not self.dfs[key].empty:
            df = pd.concat([self.dfs[key], df])
        self.dfs[key] = df.fillna("")

    @staticmethod
    def _flatten_props(values) -> pd.DataFrame:
        """Flatten a column containing a list of dicts into a single dataframe."""
        frames = [pd.json_normalize(v) for v in values if v]
        if not frames:
            return pd.DataFrame()
        return pd.concat(frames)

    def _read_sql_master(self, connection, table_name: str) -> pd.DataFrame:
        return pd.read_sql(
            "SELECT * FROM sqlite_master WHERE tbl_name = ?",
            connection,
            params=(table_name,),
        )

    # ------------------------------------------------------------------
    # parsing
    # ------------------------------------------------------------------

    def create_df_from_field(self, player: dict, field_name: str):
        df = pd.json_normalize(player, record_path=[field_name]).fillna("")
        df["player_id"] = player["id"]
        df["run_id"] = self.run_id
        self.dfs[field_name] = (
            pd.concat([self.dfs[field_name], df]) if field_name in self.dfs else df
        )

    def parse_players(self):
        props_fields = [
            "props.cards",
            "props.ints",
            "props.bools",
            "props.model_ids",
            "props.strings",
            "props.card_arrays",
        ]
        props_buckets: dict[str, list[pd.DataFrame]] = {}

        for player in self.data["players"]:
            player_df = pd.json_normalize(player).fillna("")

            # expand list-of-dict sub-fields off the player row into their own dfs
            for field in ("deck", "badges", "potions"):
                if field in player_df.columns:
                    self.create_df_from_field(player, field)
                    player_df.drop(field, axis=1, inplace=True)
            player_df["run_id"] = self.run_id

            # parse player relics
            relics = pd.json_normalize(player, record_path=["relics"]).fillna("")
            for field in props_fields:
                if field in relics.columns:
                    field_df = self._flatten_props(relics[field].values.tolist())
                    if not field_df.empty:
                        field_df["run_id"] = self.run_id
                        field_df["player_id"] = player["id"]
                        props_buckets.setdefault(field, []).append(field_df)
                if field in relics.columns:
                    relics.drop(field, axis=1, inplace=True)
            relics["player_id"] = player["id"]
            relics["run_id"] = self.run_id
            player_df.drop("relics", axis=1, inplace=True)

            self._append_df("player_relics", relics)
            self._append_df("players", player_df)

        for field, frames in props_buckets.items():
            field_df = pd.concat(frames).fillna("")
            field_df["run_id"] = self.run_id
            self.dfs[field] = field_df

    def parse_map_point_history(self):
        acts = [a.replace("ACT.", "").capitalize() for a in self.data["acts"]]

        fields_to_df = [
            "ancient_choice",
            "event_choices",
            "card_choices",
            "relic_choices",
            "potion_choices",
            "cards_removed",
            "cards_transformed",
            "cards_enchanted",
        ]
        choices_buckets: dict[str, list[pd.DataFrame]] = {}

        map_point_recurrence = {}
        for act_idx, act_data in enumerate(self.data["map_point_history"]):
            act = acts[act_idx]
            map_point = pd.json_normalize(act_data).fillna("")
            map_point["run_id"] = self.run_id
            map_point["act"] = act
            map_point["floors"] = [f"Floor {i + 1}" for i in range(len(map_point))]
            map_point.drop(["rooms", "player_stats"], axis=1, inplace=True)
            map_point_recurrence.setdefault("map_point", []).append(map_point)

            rooms = pd.json_normalize(act_data, record_path=["rooms"]).fillna("")
            if "monster_ids" in rooms.columns:
                rooms["monster_ids"] = [
                    "; ".join(m.replace("MONSTER.", "").replace("_", " ") for m in monsters)
                    if monsters
                    else ""
                    for monsters in rooms["monster_ids"].values.tolist()
                ]
                rooms["run_id"] = self.run_id
            map_point_recurrence.setdefault("rooms", []).append(rooms)

            player_stats = pd.json_normalize(act_data, record_path=["player_stats"]).fillna("")
            player_stats["run_id"] = self.run_id

            for field in fields_to_df:
                if field in player_stats.columns:
                    field_df = self._flatten_props(player_stats[field].values.tolist())
                    if not field_df.empty:
                        field_df["run_id"] = self.run_id
                        choices_buckets.setdefault(field, []).append(field_df)

            for field in fields_to_df:
                if field in player_stats.columns:
                    player_stats.drop(field, axis=1, inplace=True)

            fields_to_str = [
                "relics_removed",
                "rest_site_choices",
                "potion_used",
                "upgraded_cards",
                "bought_relics",
                "completed_quests",
                "bought_colorless",
                "bought_potions",
                "downgraded_cards",
                "potion_discarded",
            ]
            for field in fields_to_str:
                if field in player_stats.columns:
                    player_stats[field] = ["; ".join(v) for v in player_stats[field].values.tolist()]

            if "cards_gained" in player_stats.columns:
                player_stats["cards_gained"] = [
                    "; ".join(card["id"].replace("CARD.", "") for card in cards)
                    if cards
                    else ""
                    for cards in player_stats["cards_gained"].values.tolist()
                ]

            map_point_recurrence.setdefault("player_stats", []).append(player_stats)

        for key, frames in map_point_recurrence.items():
            self.dfs[key] = pd.concat(frames).fillna("")

        for field, frames in choices_buckets.items():
            self.dfs[field] = pd.concat(frames).fillna("")
            self.dfs[field]["run_id"] = self.run_id

        if "card_choices" in self.dfs:
            self._split_props_column("card_choices", "card.props.ints", "card_props")

        if "relic_choices" in self.dfs:
            self._split_props_column("relic_choices", "props.ints", "relics_props")
            self._split_props_column("relic_choices", "props.model_ids", "relics_models")

        if "cards_removed" in self.dfs:
            self._split_props_column("cards_removed", "props.ints", "card_removed_props")

        if "cards_transformed" in self.dfs:
            self._split_props_column(
                "cards_transformed", "final_card.props.ints", "cards_transformed"
            )

    def _split_props_column(self, source: str, column: str, target: str):
        """Extract a nested ``props`` column into its own dataframe and drop it in place."""
        df = pd.DataFrame()
        if column in self.dfs[source].columns:
            df = self._flatten_props(self.dfs[source][column].values.tolist())
            if not df.empty:
                df["run_id"] = self.run_id
            self.dfs[source].drop(column, axis=1, inplace=True)
        self.dfs[target] = df

    def parse_run_metadata(self):
        fields_to_ignore = {"map_point_history", "acts", "players", "modifiers"}

        run_data = {"run_id": self.run_id}
        for k, v in self.data.items():
            if k in fields_to_ignore:
                continue
            run_data[k] = v

        if self.data.get("modifiers"):
            self.dfs["run_modifiers"] = pd.json_normalize(self.data, record_path=["modifiers"]).fillna("")
            if "props.model_ids" in self.dfs["run_modifiers"].columns:
                self._split_props_column(
                    "run_modifiers", "props.model_ids", "run_modifiers_model_ids"
                )
            self.dfs["run_modifiers"]["run_id"] = self.run_id

        self.dfs["runs"] = pd.DataFrame([run_data])

    # ------------------------------------------------------------------
    # database
    # ------------------------------------------------------------------

    def create_db(self):
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.db_path) as connection:
            connection.cursor().executescript(self.schema_path.read_text())

    @staticmethod
    def _rename_dotted_columns(df: pd.DataFrame) -> pd.DataFrame:
        renames = {col: col.replace(".", "_") for col in df.columns if "." in col}
        return df.rename(columns=renames)

    def load_to_db(self):
        if not self.db_path.exists():
            self.create_db()
        with sqlite3.connect(self.db_path) as connection:
            for key, v in self.dfs.items():
                if v.empty:
                    continue
                v = self._rename_dotted_columns(v)
                table_exists = not self._read_sql_master(connection, key).empty
                if not table_exists:
                    v.to_sql(key, connection, index=False)
                else:
                    new_df = pd.concat(
                        [pd.read_sql(f'SELECT * FROM "{key}"', connection), v]
                    )
                    new_df.to_sql(key, connection, if_exists="replace", index=False)


def get_run_ids(db_path: Path) -> list[str]:
    output: list[str] = []
    if db_path.exists():
        with sqlite3.connect(db_path) as connection:
            df = pd.read_sql("SELECT run_id FROM runs", connection)
            output = [str(i) for i in df["run_id"].values.tolist()]
    return output


def main():
    parser = argparse.ArgumentParser(
        description="Parse Slay the Spire 2 run history into a sqlite database."
    )
    parser.add_argument("runs_location", type=Path, help="Directory holding .run save files")
    parser.add_argument(
        "--db",
        type=Path,
        default=Path("instance/sts2_runs.db"),
        help="Output sqlite database path",
    )
    args = parser.parse_args()

    db_path = args.db
    run_files = [p for p in args.runs_location.glob("*.run") if p.is_file()]

    existing_ids = set(get_run_ids(db_path))
    runs_to_parse = [
        p for p in run_files if p.stem not in existing_ids
    ]

    for run_file in tqdm(runs_to_parse):
        sts = StsRunParser(run_file, db_path)
        sts.parse_run_metadata()
        sts.parse_map_point_history()
        sts.parse_players()
        sts.load_to_db()


if __name__ == "__main__":
    main()
