debug_TagStruct = {}
debug_TagStruct_Type = {}
debug_DataBlock = {}
debug_DataReference = {}
debug_TagDependency = {}
debug_dict = {}
debug_dict_1 = {}
debug_hash = {}

debug_data_ref_zoneInfo = {}

bitmap_id_usage = {}

normal_artifact_files = {}

vertx_data_arrays = {}

artifact_on_all_comp = [
    '__chore\\pc__\\materials\\generic\\base\\banished\\grime\\oil_caked_a\\ban_base_grime_oil_caked_a_normal{pc}.bitmap',
    '__chore\\pc__\\materials\\generic\\base\\banished\\grime\\oil_heavy_a\\oil_heavy_a_normal{pc}.bitmap',
    '__chore\\pc__\\materials\\generic\\base\\banished\\grime\\oil_wet_a\\ban_base_grime_oil_wet_a_normal{pc}.bitmap',
    '__chore\\pc__\\materials\\generic\\base\\banished\\leather\\smooth_b\\smooth_b_normal{pc}.bitmap',
    '__chore\\pc__\\materials\\generic\\base\\banished\\leather\\techsuit_a\\techsuit_a_normal{pc}.bitmap',
    '__chore\\pc__\\materials\\generic\\base\\banished\\leather\\worn_a\\ban_base_leather_worn_a_normal{pc}.bitmap',
    '__chore\\pc__\\materials\\generic\\base\\banished\\leather\\worn_b\\worn_b_normal{pc}.bitmap',
    '__chore\\pc__\\materials\\generic\\base\\banished\\leather\\worn_c\\worn_b_normal{pc}.bitmap',
    '__chore\\pc__\\materials\\generic\\base\\banished\\metal\\dark_coated_a\\ban_base_metal_dark_coated_a_normal{pc}.bitmap',
    '__chore\\pc__\\materials\\generic\\base\\banished\\paint\\oil_heavy_a\\ban_base_grime_oil_heavy_a_normal{pc}.bitmap',
    '__chore\\pc__\\materials\\generic\\base\\banished\\paint\\oil_wet_a\\ban_base_grime_oil_wet_a_normal{pc}.bitmap',
    '__chore\\pc__\\materials\\generic\\base\\banished\\paint\\skin_cracked_a\\skin_cracked_a_normal{pc}.bitmap',
    '__chore\\pc__\\materials\\generic\\base\\banished\\paint\\wet_dry_a\\wet_dry_a_normal{pc}.bitmap',
    '__chore\\pc__\\materials\\generic\\base\\damage\\char_coarse_mask\\dmg_base_char_coarse_mask_normal{pc}.bitmap',
    '__chore\\pc__\\materials\\generic\\base\\human\\fabric\\canvas\\hum_base_fabric_canvas_normal{pc}.bitmap',
    '__chore\\pc__\\materials\\generic\\base\\human\\fabric\\cordura\\hum_base_fabric_cordura_normal{pc}.bitmap',
    '__chore\\pc__\\materials\\generic\\base\\human\\fabric\\cotton\\hum_base_fabric_cotton_normal{pc}.bitmap',
    '__chore\\pc__\\materials\\generic\\base\\human\\fabric\\felt\\hum_base_fabric_felt_normal{pc}.bitmap',
    '__chore\\pc__\\materials\\generic\\base\\human\\fabric\\gauze\\hum_base_fabric_gauze_normal{pc}.bitmap',
    '__chore\\pc__\\materials\\generic\\base\\human\\fabric\\nomex\\hum_base_fabric_nomex_normal{pc}.bitmap',
    '__chore\\pc__\\materials\\generic\\base\\human\\fabric\\nomex_thread_new\\hum_base_fabric_nomex_thread_new_normal{pc}.bitmap',
    '__chore\\pc__\\materials\\generic\\base\\human\\fabric\\oriental_pattern_01\\hum_base_fabric_oriental_pattern_01_normal{pc}.bitmap',
    '__chore\\pc__\\materials\\generic\\base\\human\\fabric\\oriental_pattern_04\\hum_base_fabric_oriental_pattern_04_normal{pc}.bitmap',
    '__chore\\pc__\\materials\\generic\\base\\human\\fabric\\oriental_pattern_09\\hum_base_fabric_oriental_pattern_09_normal{pc}.bitmap',
    '__chore\\pc__\\materials\\generic\\base\\human\\fabric\\plush\\hum_base_fabric_plush_normal{pc}.bitmap',
    '__chore\\pc__\\materials\\generic\\base\\human\\fabric\\polyester_ripstop\\hum_base_fabric_polyester_ripstop_normal{pc}.bitmap',
    '__chore\\pc__\\materials\\generic\\base\\human\\fabric\\suede\\hum_base_fabric_suede_normal{pc}.bitmap',
    '__chore\\pc__\\materials\\generic\\base\\human\\fabric\\velcro\\hum_base_fabric_velcro_normal{pc}.bitmap',
    '__chore\\pc__\\materials\\generic\\base\\human\\grime\\rust\\hum_base_rust_normal{pc}.bitmap',
    '__chore\\pc__\\materials\\generic\\base\\human\\leather\\leather\\hum_base_leather_basic_normal{pc}.bitmap',
    '__chore\\pc__\\materials\\generic\\base\\human\\leather\\leather_worn\\hum_base_leather_worn_normal{pc}.bitmap',
    '__chore\\pc__\\materials\\generic\\base\\human\\metal\\charred\\hum_base_metal_charred_normal{pc}.bitmap',
    '__chore\\pc__\\materials\\generic\\base\\human\\metal\\steel_battered\\hum_base_metal_steel_battered_normal{pc}.bitmap',
    '__chore\\pc__\\materials\\generic\\base\\human\\paint\\pattern_scales\\hum_base_paint_pattern_scales_small_normal{pc}.bitmap',
    '__chore\\pc__\\materials\\generic\\base\\human\\paint\\pattern_scales_b\\hum_base_paint_pattern_scales_small_b_normal{pc}.bitmap',
    '__chore\\pc__\\materials\\generic\\base\\human\\paint\\pattern_scales_c\\hum_base_paint_pattern_scales_small_c_normal{pc}.bitmap',
    '__chore\\pc__\\materials\\generic\\base\\human\\plastic\\plastic_gun_bumpy\\hum_base_plastic_gun_bumpy_normal{pc}.bitmap',
    '__chore\\pc__\\materials\\generic\\base\\human\\plastic\\plastic_high_grip\\hum_base_plastic_high_grip_normal{pc}.bitmap',
    '__chore\\pc__\\materials\\generic\\base\\human\\plastic\\plastic_textured\\hum_base_plastic_textured_normal{pc}.bitmap',
    '__chore\\pc__\\materials\\generic\\base\\human\\rubber\\textured\\hum_base_rubber_textured_normal{pc}.bitmap',
    '__chore\\pc__\\materials\\generic\\base\\human\\rubber\\textured\\hum_base_rubber_textured_scratched_normal{pc}.bitmap',
    '__chore\\pc__\\materials\\generic\\base\\human\\rubber\\worn\\hum_base_rubber_worn_normal{pc}.bitmap',
    '__chore\\pc__\\materials\\generic\\base\\human\\wood\\wood_worn_01\\hum_base_wood_worn_01_normal{pc}.bitmap',
    '__chore\\pc__\\materials\\generic\\base\\organic\\dirt\\org_base_dirt_dusting_normal{pc}.bitmap',
    '__chore\\pc__\\materials\\generic\\base\\organic\\frost\\org_base_frost_01_normal{pc}.bitmap',
    '__chore\\pc__\\materials\\generic\\base\\organic\\frost_shard\\hum_base_organic_frost_shard_normal{pc}.bitmap',
    '__chore\\pc__\\materials\\generic\\base\\organic\\skin\\creature\\bumpy_a\\skin_creature_bumpy_a_normal{pc}.bitmap',
    '__chore\\pc__\\materials\\generic\\base\\organic\\skin\\creature\\test\\skin_creature_test_normal{pc}.bitmap']


def fillDebugDict(main_key, name_key, p_debug_dict):
    if p_debug_dict.keys().__contains__(main_key):
        if p_debug_dict[main_key].keys().__contains__(name_key):
            p_debug_dict[main_key][name_key] += 1
        else:
            p_debug_dict[main_key][name_key] = 1
    else:
        p_debug_dict[main_key] = {name_key: 1}


def intersection_meth1(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3


def intersection_meth2(lst1, lst2):
    return list(set(lst1) & set(lst2))


def Intersection_meth3(lst1, lst2):
    return set(lst1).intersection(lst2)


def Difference_meth3(lst1, lst2):
    return set(lst1).difference(lst2)


def intersection_meth4(lst1, lst2):
    # Use of hybrid method
    temp = set(lst2)
    lst3 = [value for value in lst1 if value in temp]
    return lst3


def intersection_meth5(lst1, lst2):
    lst3 = [list(filter(lambda x: x in lst1, sublist)) for sublist in lst2]
    return lst3
