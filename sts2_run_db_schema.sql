CREATE TABLE "ancient_choice" (
"TextKey" TEXT,
  "was_chosen" INTEGER,
  "title_key" TEXT,
  "title_table" TEXT,
  "run_id" TEXT
);

CREATE TABLE "badges" (
"id" TEXT,
  "rarity" TEXT,
  "player_id" INTEGER,
  "run_id" TEXT
);

CREATE TABLE "card_choices" (
"was_picked" INTEGER,
  "card_floor_added_to_deck" TEXT,
  "card_id" TEXT,
  "card_current_upgrade_level" TEXT,
  "run_id" TEXT,
  "card_enchantment_amount" TEXT,
  "card_enchantment_id" TEXT
);

CREATE TABLE "card_props" (
"name" TEXT,
  "value" INTEGER,
  "run_id" TEXT
);

CREATE TABLE "cards_enchanted" (
"enchantment" TEXT,
  "card_enchantment_amount" INTEGER,
  "card_enchantment_id" TEXT,
  "card_floor_added_to_deck" INTEGER,
  "card_id" TEXT,
  "run_id" TEXT
);

CREATE TABLE "cards_removed" (
"floor_added_to_deck" INTEGER,
  "id" TEXT,
  "run_id" TEXT,
  "current_upgrade_level" TEXT
);

CREATE TABLE "deck" (
"floor_added_to_deck" INTEGER,
  "id" TEXT,
  "enchantment_amount" TEXT,
  "enchantment_id" TEXT,
  "current_upgrade_level" TEXT,
  "player_id" INTEGER,
  "run_id" TEXT
);

CREATE TABLE "event_choices" (
"title_key" TEXT,
  "title_table" TEXT,
  "variables_Enchantment1_type" TEXT,
  "variables_Enchantment1_decimal_value" TEXT,
  "variables_Enchantment1_bool_value" TEXT,
  "variables_Enchantment1_string_value" TEXT,
  "variables_Enchantment2_type" TEXT,
  "variables_Enchantment2_decimal_value" TEXT,
  "variables_Enchantment2_bool_value" TEXT,
  "variables_Enchantment2_string_value" TEXT,
  "variables_Enchantment3_type" TEXT,
  "variables_Enchantment3_decimal_value" TEXT,
  "variables_Enchantment3_bool_value" TEXT,
  "variables_Enchantment3_string_value" TEXT,
  "run_id" TEXT,
  "variables_RandomCard_type" TEXT,
  "variables_RandomCard_decimal_value" TEXT,
  "variables_RandomCard_bool_value" TEXT,
  "variables_RandomCard_string_value" TEXT,
  "variables_HpLoss_type" TEXT,
  "variables_HpLoss_decimal_value" TEXT,
  "variables_HpLoss_bool_value" TEXT,
  "variables_HpLoss_string_value" TEXT,
  "variables_TopRelicOwned_type" TEXT,
  "variables_TopRelicOwned_decimal_value" TEXT,
  "variables_TopRelicOwned_bool_value" TEXT,
  "variables_TopRelicOwned_string_value" TEXT,
  "variables_TopRelicNew_type" TEXT,
  "variables_TopRelicNew_decimal_value" TEXT,
  "variables_TopRelicNew_bool_value" TEXT,
  "variables_TopRelicNew_string_value" TEXT,
  "variables_MiddleRelicOwned_type" TEXT,
  "variables_MiddleRelicOwned_decimal_value" TEXT,
  "variables_MiddleRelicOwned_bool_value" TEXT,
  "variables_MiddleRelicOwned_string_value" TEXT,
  "variables_MiddleRelicNew_type" TEXT,
  "variables_MiddleRelicNew_decimal_value" TEXT,
  "variables_MiddleRelicNew_bool_value" TEXT,
  "variables_MiddleRelicNew_string_value" TEXT,
  "variables_BottomRelicOwned_type" TEXT,
  "variables_BottomRelicOwned_decimal_value" TEXT,
  "variables_BottomRelicOwned_bool_value" TEXT,
  "variables_BottomRelicOwned_string_value" TEXT,
  "variables_BottomRelicNew_type" TEXT,
  "variables_BottomRelicNew_decimal_value" TEXT,
  "variables_BottomRelicNew_bool_value" TEXT,
  "variables_BottomRelicNew_string_value" TEXT,
  "variables_Relic_type" TEXT,
  "variables_Relic_decimal_value" TEXT,
  "variables_Relic_bool_value" TEXT,
  "variables_Relic_string_value" TEXT,
  "variables_Curse_type" TEXT,
  "variables_Curse_decimal_value" TEXT,
  "variables_Curse_bool_value" TEXT,
  "variables_Curse_string_value" TEXT,
  "variables_BargainBinCost_type" TEXT,
  "variables_BargainBinCost_decimal_value" TEXT,
  "variables_BargainBinCost_bool_value" TEXT,
  "variables_BargainBinCost_string_value" TEXT,
  "variables_MysteryBoxCost_type" TEXT,
  "variables_MysteryBoxCost_decimal_value" TEXT,
  "variables_MysteryBoxCost_bool_value" TEXT,
  "variables_MysteryBoxCost_string_value" TEXT,
  "variables_FeaturedItemCost_type" TEXT,
  "variables_FeaturedItemCost_decimal_value" TEXT,
  "variables_FeaturedItemCost_bool_value" TEXT,
  "variables_FeaturedItemCost_string_value" TEXT,
  "variables_MysteryBoxRelicCount_type" TEXT,
  "variables_MysteryBoxRelicCount_decimal_value" TEXT,
  "variables_MysteryBoxRelicCount_bool_value" TEXT,
  "variables_MysteryBoxRelicCount_string_value" TEXT,
  "variables_MysteryBoxCombatCount_type" TEXT,
  "variables_MysteryBoxCombatCount_decimal_value" TEXT,
  "variables_MysteryBoxCombatCount_bool_value" TEXT,
  "variables_MysteryBoxCombatCount_string_value" TEXT,
  "variables_WongoPointAmount_type" TEXT,
  "variables_WongoPointAmount_decimal_value" TEXT,
  "variables_WongoPointAmount_bool_value" TEXT,
  "variables_WongoPointAmount_string_value" TEXT,
  "variables_RemainingWongoPointAmount_type" TEXT,
  "variables_RemainingWongoPointAmount_decimal_value" TEXT,
  "variables_RemainingWongoPointAmount_bool_value" TEXT,
  "variables_RemainingWongoPointAmount_string_value" TEXT,
  "variables_TotalWongoBadgeAmount_type" TEXT,
  "variables_TotalWongoBadgeAmount_decimal_value" TEXT,
  "variables_TotalWongoBadgeAmount_bool_value" TEXT,
  "variables_TotalWongoBadgeAmount_string_value" TEXT,
  "variables_RandomRelic_type" TEXT,
  "variables_RandomRelic_decimal_value" TEXT,
  "variables_RandomRelic_bool_value" TEXT,
  "variables_RandomRelic_string_value" TEXT,
  "variables_Enchantment_type" TEXT,
  "variables_Enchantment_decimal_value" TEXT,
  "variables_Enchantment_bool_value" TEXT,
  "variables_Enchantment_string_value" TEXT,
  "variables_BoneTeaCost_type" TEXT,
  "variables_BoneTeaCost_decimal_value" TEXT,
  "variables_BoneTeaCost_bool_value" TEXT,
  "variables_BoneTeaCost_string_value" TEXT,
  "variables_EmberTeaCost_type" TEXT,
  "variables_EmberTeaCost_decimal_value" TEXT,
  "variables_EmberTeaCost_bool_value" TEXT,
  "variables_EmberTeaCost_string_value" TEXT,
  "variables_BoneTeaDescription_type" TEXT,
  "variables_BoneTeaDescription_decimal_value" TEXT,
  "variables_BoneTeaDescription_bool_value" TEXT,
  "variables_BoneTeaDescription_string_value" TEXT,
  "variables_EmberTeaDescription_type" TEXT,
  "variables_EmberTeaDescription_decimal_value" TEXT,
  "variables_EmberTeaDescription_bool_value" TEXT,
  "variables_EmberTeaDescription_string_value" TEXT,
  "variables_TeaOfDiscourtesyDescription_type" TEXT,
  "variables_TeaOfDiscourtesyDescription_decimal_value" TEXT,
  "variables_TeaOfDiscourtesyDescription_bool_value" TEXT,
  "variables_TeaOfDiscourtesyDescription_string_value" TEXT,
  "variables_Card1_type" TEXT,
  "variables_Card1_decimal_value" TEXT,
  "variables_Card1_bool_value" TEXT,
  "variables_Card1_string_value" TEXT,
  "variables_Card2_type" TEXT,
  "variables_Card2_decimal_value" TEXT,
  "variables_Card2_bool_value" TEXT,
  "variables_Card2_string_value" TEXT,
  "variables_UncoverFutureCost_type" TEXT,
  "variables_UncoverFutureCost_decimal_value" TEXT,
  "variables_UncoverFutureCost_bool_value" TEXT,
  "variables_UncoverFutureCost_string_value" TEXT,
  "variables_UncoverFutureProphesizeCount_type" TEXT,
  "variables_UncoverFutureProphesizeCount_decimal_value" TEXT,
  "variables_UncoverFutureProphesizeCount_bool_value" TEXT,
  "variables_UncoverFutureProphesizeCount_string_value" TEXT,
  "variables_PaymentPlanCount_type" TEXT,
  "variables_PaymentPlanCount_decimal_value" TEXT,
  "variables_PaymentPlanCount_bool_value" TEXT,
  "variables_PaymentPlanCount_string_value" TEXT,
  "variables_CurseTitle_type" TEXT,
  "variables_CurseTitle_decimal_value" TEXT,
  "variables_CurseTitle_bool_value" TEXT,
  "variables_CurseTitle_string_value" TEXT
);

CREATE TABLE "map_point" (
"map_point_type" TEXT,
  "run_id" TEXT,
  "act" TEXT,
  "floors" TEXT
);

CREATE TABLE "player_relics" (
"floor_added_to_deck" INTEGER,
  "id" TEXT,
  "player_id" INTEGER,
  "run_id" TEXT
);

CREATE TABLE "player_stats" (
"current_gold" INTEGER,
  "current_hp" INTEGER,
  "damage_taken" INTEGER,
  "gold_gained" INTEGER,
  "gold_lost" INTEGER,
  "gold_spent" INTEGER,
  "gold_stolen" INTEGER,
  "hp_healed" INTEGER,
  "max_hp" INTEGER,
  "max_hp_gained" INTEGER,
  "max_hp_lost" INTEGER,
  "player_id" INTEGER,
  "cards_gained" TEXT,
  "upgraded_cards" TEXT,
  "rest_site_choices" TEXT,
  "potion_used" TEXT,
  "run_id" TEXT,
  "relics_removed" TEXT,
  "bought_relics" TEXT,
  "completed_quests" TEXT
);

CREATE TABLE "players" (
"character" TEXT,
  "id" INTEGER,
  "max_potion_slot_count" INTEGER,
  "run_id" TEXT
);

CREATE TABLE "potion_choices" (
"choice" TEXT,
  "was_picked" INTEGER,
  "run_id" TEXT
);

CREATE TABLE "props.bools" (
"name" TEXT,
  "value" INTEGER,
  "run_id" TEXT,
  "player_id" INTEGER
);

CREATE TABLE "props.cards" (
"name" TEXT,
  "value_id" TEXT,
  "value_floor_added_to_deck" TEXT,
  "run_id" TEXT,
  "player_id" INTEGER,
  "value_current_upgrade_level" TEXT
);

CREATE TABLE "props.ints" (
"name" TEXT,
  "value" INTEGER,
  "run_id" TEXT,
  "player_id" INTEGER
);

CREATE TABLE "props.model_ids" (
"name" TEXT,
  "value" TEXT,
  "run_id" TEXT,
  "player_id" INTEGER
);

CREATE TABLE "relic_choices" (
"choice" TEXT,
  "was_picked" INTEGER,
  "run_id" TEXT
);

CREATE TABLE "rooms" (
"model_id" TEXT,
  "room_type" TEXT,
  "turns_taken" INTEGER,
  "monster_ids" TEXT,
  "run_id" TEXT
);

CREATE TABLE "runs" (
"run_id" TEXT,
  "ascension" INTEGER,
  "build_id" TEXT,
  "game_mode" TEXT,
  "killed_by_encounter" TEXT,
  "killed_by_event" TEXT,
  "platform_type" TEXT,
  "run_time" INTEGER,
  "schema_version" INTEGER,
  "seed" TEXT,
  "start_time" INTEGER,
  "was_abandoned" INTEGER,
  "win" INTEGER
);

CREATE UNIQUE INDEX IF NOT EXISTS run_idx ON "runs"("run_id");

CREATE TABLE "card_removed_props" (
"name" TEXT,
  "value" TEXT,
  "run_id" TEXT
);

CREATE TABLE "cards_transformed" (
"name" TEXT,
  "value" TEXT,
  "run_id" TEXT
);

CREATE TABLE "potions" (
"id" TEXT,
  "slot_index" TEXT,
  "player_id" TEXT,
  "run_id" TEXT
);

CREATE TABLE "props.strings" (
"name" TEXT,
  "value" TEXT,
  "run_id" TEXT,
  "player_id" TEXT
);

CREATE TABLE "run_modifiers" (
"id" TEXT,
  "run_id" TEXT
);

CREATE TABLE "run_modifiers_model_ids" (
"name" TEXT,
  "value" TEXT,
  "run_id" TEXT
);
