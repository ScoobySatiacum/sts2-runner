# Milestone 2: Schema contract and data mapping design

## Objective

Define the relational schema contract that will preserve the full contents of each .run file in SQLite in a normalized and queryable form. This milestone establishes the table layout and the relationship model that the rest of the application will depend on.

## Scope

- Define the top-level table families for a run.
- Map nested JSON sections to relational tables.
- Define the run_id and child-table identifiers.
- Decide how nested arrays and dictionaries are flattened into child records.
- Document the relationships between parent and child tables.

## Design constraints

- The schema must represent the source data faithfully.
- The design must not be driven by a single report or dashboard.
- No essential data should be dropped during normalization.
- The schema must support both reporting and analytics without requiring loss-prone flattening later.

## Proposed schema structure

```text
runs
players
player_relics
player_cards
player_potions
player_badges
map_points
map_rooms
player_stats
run_modifiers
card_choices
relic_choices
choice_props
cards_removed
cards_transformed
```

Additional tables may be created as needed, but all should follow the same principles: explicit identity fields, clear parent ownership, and a definition rooted in the raw JSON structure.

## How to read this milestone

The schema contract is the agreement between the source JSON, the normalizer, and the SQLite repository. It is more precise than a list of table names: it must explain what creates a row, how that row is identified, which parent owns it, how ordering is preserved, and what happens when a value is missing or unknown.

The examples below are teaching examples for the target contract. They are not a replacement for the existing generated schema in `sts2_run_db_schema.sql`, and they do not mean that the target table names or columns are approved until the checklist and unresolved questions are reviewed.

## Example 1: one run and one player

A representative player in `tests/samples/win.run` contains scalar values and nested collections:

```json
{
    "id": 0,
    "character": "CHARACTER.DEFECT",
    "max_potion_slot_count": 3,
    "deck": [
        {
            "id": "CARD.STRIKE_DEFECT",
            "floor_added_to_deck": 1,
            "enchantment": {
                "id": "ENCHANTMENT.SHARP",
                "amount": 2
            }
        }
    ],
    "relics": [],
    "potions": [],
    "badges": []
}
```

The run and player portions can become rows like these:

| Source value | Destination | Why |
| --- | --- | --- |
| The file stem, such as `win` | `runs.run_id` | Stable identity for one imported file. |
| `players[0].id` | `players.player_id` | Identity within the run. |
| `players[0].character` | `players.character` | Scalar player attribute. |
| `players[0].deck[0]` | One row in `player_cards` | One array element becomes one child row. |
| `deck[0].enchantment` | Columns on `player_cards` or a child property table | The contract must choose a lossless representation. |
| An empty `relics` array | Zero `player_relics` rows | Empty is different from an unknown field. |

The parent keys make the ownership explicit:

```text
runs.run_id
    |
    +-- players.(run_id, player_id)
                    |
                    +-- player_cards.(run_id, player_id, card_ordinal)
                    +-- player_relics.(run_id, player_id, relic_ordinal)
                    +-- player_potions.(run_id, player_id, potion_ordinal)
```

The `card_ordinal`, `relic_ordinal`, and `potion_ordinal` values are examples of source-order columns. They prevent a later query from having to guess the original order.

## Example 2: illustrative SQL for the parent and child rows

This is a small example of the constraints the contract should make explicit. It is intentionally narrower than the complete schema:

```sql
PRAGMA foreign_keys = ON;

CREATE TABLE runs (
        run_id TEXT PRIMARY KEY,
        schema_version INTEGER NOT NULL,
        win INTEGER,
        start_time INTEGER
);

CREATE TABLE players (
        run_id TEXT NOT NULL,
        player_id INTEGER NOT NULL,
        character TEXT,
        max_potion_slot_count INTEGER,
        PRIMARY KEY (run_id, player_id),
        FOREIGN KEY (run_id) REFERENCES runs(run_id) ON DELETE CASCADE
);

CREATE TABLE player_cards (
        run_id TEXT NOT NULL,
        player_id INTEGER NOT NULL,
        card_ordinal INTEGER NOT NULL,
        card_id TEXT,
        floor_added_to_deck INTEGER,
        enchantment_id TEXT,
        enchantment_amount INTEGER,
        PRIMARY KEY (run_id, player_id, card_ordinal),
        FOREIGN KEY (run_id, player_id)
                REFERENCES players(run_id, player_id) ON DELETE CASCADE
);
```

The important lessons in this example are:

- `run_id` is present on every run-owned table.
- `player_id` is only unique within a run, so the parent key is `(run_id, player_id)`.
- `card_ordinal` distinguishes repeated cards and preserves array order.
- A child row cannot refer to a player that does not exist when foreign keys are enabled.
- `schema_version` belongs to the database contract, not to a report-specific query.

The target contract will prefer clear domain names such as `player_cards` and `map_rooms` rather than preserving ambiguous legacy names such as `deck` and `rooms`. Stable structures should use typed columns first. A generic property table should preserve fields whose names or shapes vary between game versions.

## Example 3: nested arrays and dictionaries

The source contains both arrays and dictionaries. They need different mapping rules.

### Arrays

For this source value:

```json
"relics": [
    {"id": "RELIC.A", "floor_added_to_deck": 1},
    {"id": "RELIC.B", "floor_added_to_deck": 8}
]
```

The normalized rows should retain both values and their order:

| run_id | player_id | relic_ordinal | relic_id | floor_added_to_deck |
| --- | ---: | ---: | --- | ---: |
| `win` | 0 | 0 | `RELIC.A` | 1 |
| `win` | 0 | 1 | `RELIC.B` | 8 |

Do not store only a comma-separated string when the elements may need to be queried individually. A display-oriented string can be produced later by the report layer.

### Dictionaries

For a value such as:

```json
"title": {"key": "SMALL_CAPSULE.title", "table": "relics"}
```

There are two reasonable contract choices:

```text
Choice A: columns on the owning row
    title_key = "SMALL_CAPSULE.title"
    title_table = "relics"

Choice B: a property row
    parent_type = "ancient_choice"
    property_name = "title"
    value_key = "SMALL_CAPSULE.title"
    value_table = "relics"
```

Choice A is easier to query when the dictionary shape is stable. Choice B is safer when keys vary between game versions. The target contract uses typed columns for stable fields and generic property rows for variable fields. Flattening a dictionary into a single display string would lose structure.

## Example 4: acts, map points, and player statistics

The sample `map_point_history` is nested more deeply than a single flat list. Conceptually, it can be expanded in stages:

```text
map_point_history[act_ordinal]
    -> map point[point_ordinal]
             -> rooms[room_ordinal]
             -> player_stats[player_stat_ordinal]
                        -> card_choices[]
                        -> relic_choices[]
                        -> event_choices[]
```

A target contract should therefore identify the owning context for each row, for example:

```text
run_id
act_ordinal
map_point_ordinal
player_id
room_ordinal or stat_ordinal
choice_ordinal
```

### Recommended map-point identity

Yes, each map point can be treated as one floor or level within an act. However, `run_id + floor_num` is only safe if `floor_num` is a run-wide number. The current parser generates `Floor 1`, `Floor 2`, and so on separately inside each act, so the same floor number occurs more than once in a run.

The recommended target identity is therefore:

```text
map_point_id = (run_id, act_ordinal, floor_num)
```

For the representative `win.run` sample, the generated parent rows would look like this:

| run_id | act_ordinal | floor_num | act |
| --- | ---: | ---: | --- |
| `win` | 0 | 1 | `UNDERDOCKS` |
| `win` | 0 | 2 | `UNDERDOCKS` |
| `win` | ... | ... | ... |
| `win` | 1 | 1 | `HIVE` |
| `win` | 1 | 2 | `HIVE` |
| `win` | 2 | 1 | `GLORY` |

The primary key can be declared as:

```sql
PRIMARY KEY (run_id, act_ordinal, floor_num)
```

This is a composite primary key: the combination must be unique, while each individual value may repeat. A run-wide generated floor number is also possible, but it would duplicate information already represented by `act_ordinal` and make comparisons with the source act structure less direct. If the game later exposes a canonical floor number, that source value should be stored separately from the importer-generated ordinal.

### Recommended player-stat identity

For player statistics, use the map point as the parent context and add the player identity:

```text
player_stat_id = (run_id, act_ordinal, floor_num, player_id)
```

The corresponding primary key is:

```sql
PRIMARY KEY (run_id, act_ordinal, floor_num, player_id)
```

For the current single-player sample, one row might be:

| run_id | act_ordinal | floor_num | player_id | current_hp |
| --- | ---: | ---: | ---: | ---: |
| `win` | 0 | 1 | 1 | 60 |

For a multiplayer run, the same map point can contain one row per player:

| run_id | act_ordinal | floor_num | player_id | current_hp |
| --- | ---: | ---: | ---: | ---: |
| `multiplayer_win` | 0 | 1 | 1 | 60 |
| `multiplayer_win` | 0 | 1 | 2 | 55 |

If source inspection discovers multiple statistics snapshots for the same player at one map point, add a generated `stat_ordinal`:

```text
player_stat_id = (run_id, act_ordinal, floor_num, player_id, stat_ordinal)
```

Do not add that extra key preemptively if the source guarantees one snapshot. The contract should reserve the option and test the assumption against single-player and multiplayer samples.

### Why not use only generated integer IDs?

A surrogate integer such as `map_point_id = 42` can be useful for joins, but it does not explain which run, act, or floor the row belongs to. If one is added later, retain the composite natural key as a `UNIQUE` constraint:

```sql
map_point_id INTEGER PRIMARY KEY,
run_id TEXT NOT NULL,
act_ordinal INTEGER NOT NULL,
floor_num INTEGER NOT NULL,
UNIQUE (run_id, act_ordinal, floor_num)
```

For M02, the composite key is easier to understand and sufficient for the observed data. A surrogate key should be introduced only if later repository or query code demonstrates a concrete benefit.

The key lesson is that a `room` or `card_choice` row should not be attached only to `run_id` if the source distinguishes acts, map points, players, or repeated choices. Child tables should reference the complete map-point context, either directly through the composite columns or through a map-point surrogate with the same natural-key constraint.

## Value and absence rules

The contract should use consistent meanings for these cases:

| Source state | Recommended relational meaning |
| --- | --- |
| A present scalar with a value | Store it in its typed column. |
| A present scalar with JSON `null` | Store SQL `NULL` unless the domain requires a separate sentinel. |
| An absent optional field | Store SQL `NULL` or record its absence in a documented preservation structure; do not silently convert it to an empty string. |
| An empty array | Create zero child rows and retain the parent row. |
| An empty dictionary | Retain the parent row; create zero property rows if using a property table. |
| An unknown field or enum value | Preserve it in a generic property row and record the interpretation gap. |
| A boolean | Use an explicit SQLite convention, such as `0` and `1`, and test it. |

The existing parser currently calls `fillna("")` in several places and serializes some nested lists into strings. That is useful legacy behavior to inventory, but it is not automatically the M02 contract because it can blur the difference between missing, empty, and present-empty values.

## Example 5: schema versioning and migrations

The first migration should be identifiable and repeatable. A minimal migration marker could look like this:

```sql
CREATE TABLE schema_migrations (
        version INTEGER PRIMARY KEY,
        applied_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
        description TEXT NOT NULL
);

INSERT INTO schema_migrations (version, description)
VALUES (1, 'Initial normalized run schema');
```

The repository should apply migrations in ascending order and refuse or clearly report an unsupported future version. The exact migration runner belongs to M04, but M02 must define the versioning promise that M04 will implement.

## Example contract tests

The tests should verify the contract rather than only whether a SQL file parses:

```python
def test_player_cards_preserve_source_order(schema):
        table = schema.table("player_cards")

        assert table.primary_key == ("run_id", "player_id", "card_ordinal")
        assert table.column("card_ordinal").not_null is True


def test_player_cards_require_existing_player(connection):
        connection.execute("PRAGMA foreign_keys = ON")

        with pytest.raises(sqlite3.IntegrityError):
                connection.execute(
                        "INSERT INTO player_cards "
                        "(run_id, player_id, card_ordinal, card_id) "
                        "VALUES ('missing', 0, 0, 'CARD.STRIKE_DEFECT')"
                )
```

Before implementation, these examples should be adapted to the repository's actual schema-contract API. The test names demonstrate the behavior to specify: ordering, ownership, foreign-key enforcement, and typed constraints.

## Current-schema comparison points

The committed `sts2_run_db_schema.sql` is useful evidence, but it also shows why M02 is needed:

- `runs` has a unique index for `run_id`, but most child tables do not declare foreign keys back to it.
- `players` uses `id`, while the proposed contract needs a clearly named run-scoped player identifier.
- `rooms.monster_ids` is currently stored as a delimited text value, which is convenient for display but not lossless for relational querying.
- Several nested property tables use dotted table names and generic `name`/`value` columns without a documented parent identifier beyond `run_id` and sometimes `player_id`.
- There is no visible migration table or ordered migration mechanism in the current SQL file.

These are comparison points, not a demand to rewrite the legacy schema during M02. M02 should decide the target contract; M03 and M04 should implement parsing and persistence against that approved contract.

## Decisions recorded for review

- Prefer clear target names such as `player_cards` and `map_rooms`; document legacy names as compatibility evidence rather than treating them as the target contract.
- Use typed columns for stable, well-understood structures.
- Use generic property rows for unknown or version-variable fields so their keys and values remain queryable.
- Do not rely on a raw JSON column as the primary preservation mechanism for fields that can be represented by generic property rows.

The remaining questions for approval are narrower:

- What is the authoritative identity for a map point and a player-stat snapshot when the source contains repeated records?
- What initial schema version and migration naming convention will M04 adopt?

## Acceptance criteria

- Each high-level object in the run file has a corresponding relational table family.
- Parent and child relationships are explicitly represented with run_id and related foreign keys.
- There is a stable contract for how nested arrays and objects are expanded into database rows.
- The schema is versioned and migration-aware.

## Execution checklist

### Preconditions

- [ ] Confirm Milestone 1 package contracts are available and tested.
- [ ] Inventory the actual top-level keys and nested collections in every representative sample `.run` file.
- [ ] Record unknown, optional, and version-dependent fields instead of assuming the sample files are complete.

### Schema design

- [ ] Define the `runs` table and its stable primary key.
- [ ] Define each child table and its parent key, including `run_id` on every run-owned table.
- [ ] Define identifiers for players, acts, rooms, choices, modifiers, and other repeated entities.
- [ ] Define how arrays become multiple rows while preserving their original order.
- [ ] Define how dictionaries become key/value or property rows without losing keys.
- [ ] Define how scalar values, nulls, empty arrays, and empty dictionaries are represented.
- [ ] Define SQLite column types and nullability for every table.
- [ ] Define uniqueness constraints and foreign-key constraints.
- [ ] Define a schema version mechanism and the first migration identifier.
- [ ] Map every source field to a destination column or explicitly documented preservation table.
- [ ] Record fields that cannot yet be interpreted without dropping their raw value.

### Tests and validation

- [ ] Write failing schema-contract tests for required tables and relationships.
- [ ] Test representative multiplayer and single-player samples where available.
- [ ] Test optional sections, empty collections, and repeated nested values.
- [ ] Test that source ordering is preserved for ordered arrays.
- [ ] Validate the schema with SQLite foreign-key enforcement enabled.
- [ ] Run the focused schema tests and the existing regression suite.

### Documentation and completion evidence

- [ ] Document the table catalog and relationship rules beside the schema contract.
- [ ] Record unresolved source-shape questions in the milestone ticket rather than silently choosing a lossy mapping.
- [ ] Update the technical specification if the approved schema differs from the proposal.
- [ ] Update `docs/DEVELOPMENT_STATUS.md` with the schema decision and validation evidence.
- [ ] Mark this milestone complete only when the repository can implement against the contract without inventing mappings.

## Example pytest cases

```python
# tests/test_schema_contract.py

def test_run_schema_has_required_core_tables():
    schema = build_schema_contract()

    assert "runs" in schema.tables
    assert "players" in schema.tables
    assert "player_relics" in schema.tables
    assert "map_points" in schema.tables


def test_table_foreign_keys_are_defined():
    schema = build_schema_contract()

    assert schema.table("players").foreign_key("run_id") == "runs.run_id"
    assert schema.table("player_relics").foreign_key("run_id") == "runs.run_id"
```

## Definition of done

The schema contract is complete when the table model is approved and the storage layer can begin implementation using it as the source of truth.
