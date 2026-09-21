# Ticket 02: Define the normalized SQLite schema and 1:1 run-file representation

## Goal

Design the database schema so that every field from the raw .run JSON is represented in SQLite without loss, while still remaining queryable and maintainable.

## Scope

- Define the canonical schema for run metadata
- Define normalized tables for players, relics, map data, modifiers, choices, and all nested collections
- Decide the relationship model for one-to-one, one-to-many, and many-to-many data
- Keep the database schema stable enough for future analysis and reporting

## Fundamental requirement

The project must not discard data from the raw .run file in order to fit a simplified reporting model. The database must be a faithful representation of the run data.

## Schema principles

1. The schema is normalized, not denormalized for convenience.
2. Each table should have a clear responsibility.
3. Tables are connected by run_id and related identifiers such as player_id, act_id, room_id, and choice_id where appropriate.
4. Nested arrays and dictionaries are exploded into child tables rather than stored as opaque JSON strings by default.
5. A small number of intentionally flattened or concatenated columns may remain where this is materially useful, but the default is to preserve the full structure in related tables.

## Proposed structure

- runs
  - one row per run
- players
  - one row per player in a run
- player_relics
  - one row per relic owned by a player
- player_cards
  - one row per card in a deck or hand state
- player_potions
  - one row per potion in a player state
- player_badges
  - one row per badge
- map_points
  - one row per floor or map point entry
- map_rooms
  - one row per room record
- player_stats
  - one row per player stat snapshot per map period
- run_modifiers
  - one row per modifier attached to the run
- card_choices
  - one row per card choice record
- relic_choices
  - one row per relic choice record
- choice_props
  - flattened property data belonging to choice records
- cards_removed
  - one row per removed card
- cards_transformed
  - one row per transformed card
- etc.

The exact table list should be generated from a schema contract, not from ad hoc DataFrame keys.

## Important design decision

The schema should not be driven by convenience for a single report. It should be driven by the actual structure of the Slay the Spire 2 run file. This is the root architectural requirement for the refactor.

## Acceptance criteria

- Each top-level section of the JSON run file has a corresponding table family in SQLite.
- Run-level metadata is stored in a dedicated run table with run_id as the identity key.
- Player-level data is mapped to player tables tied by run_id and player_id.
- Choice and map data are stored in distinct normalized tables rather than as embedded JSON.
- The schema can be regenerated or migrated without hand-editing the parser logic.

## Test-first approach

- Write a failing test that loads a sample .run file and asserts that a known field exists in the schema contract.
- Add a failing test for a nested collection, such as player relics or map room records, to ensure it is represented in a child table.
- Add a failing test that asserts no essential nested field is dropped during normalization.

## Definition of done

- The schema contract is approved and documented.
- The storage layer implements the planned table mapping.
- The rest of the implementation can reference the schema contract as the source of truth.
