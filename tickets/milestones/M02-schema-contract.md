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
