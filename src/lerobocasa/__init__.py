from robosuite.environments.base import make

# Manipulation environments
from lerobocasa.environments.kitchen.kitchen import Kitchen
from lerobocasa.environments.kitchen.composite.adding_ice_to_beverages.make_ice_lemonade import (
    MakeIceLemonade,
)
from lerobocasa.environments.kitchen.composite.adding_ice_to_beverages.place_equal_ice_cubes import (
    PlaceEqualIceCubes,
)
from lerobocasa.environments.kitchen.composite.adding_ice_to_beverages.place_ice_in_cup import (
    PlaceIceInCup,
)
from lerobocasa.environments.kitchen.composite.adding_ice_to_beverages.retrieve_ice_tray import (
    RetrieveIceTray,
)
from lerobocasa.environments.kitchen.composite.arranging_cabinets.reset_cabinet_doors import (
    ResetCabinetDoors,
)
from lerobocasa.environments.kitchen.composite.arranging_cabinets.gather_tableware import (
    GatherTableware,
)
from lerobocasa.environments.kitchen.composite.arranging_cabinets.stack_cans import (
    StackCans,
)
from lerobocasa.environments.kitchen.composite.arranging_condiments.categorize_condiments import (
    CategorizeCondiments,
)
from lerobocasa.environments.kitchen.composite.arranging_condiments.organize_condiments import (
    OrganizeCondiments,
)
from lerobocasa.environments.kitchen.composite.arranging_condiments.line_up_condiments import (
    LineUpCondiments,
)
from lerobocasa.environments.kitchen.composite.arranging_buffet.arrange_buffet_dessert import (
    ArrangeBuffetDessert,
)
from lerobocasa.environments.kitchen.composite.arranging_buffet.cut_buffet_pizza import (
    CutBuffetPizza,
)
from lerobocasa.environments.kitchen.composite.arranging_buffet.divide_buffet_trays import (
    DivideBuffetTrays,
)
from lerobocasa.environments.kitchen.composite.arranging_buffet.place_beverages_together import (
    PlaceBeveragesTogether,
)
from lerobocasa.environments.kitchen.composite.arranging_buffet.tong_buffet_setup import (
    TongBuffetSetup,
)
from lerobocasa.environments.kitchen.composite.baking.cookie_dough_prep import (
    CookieDoughPrep,
)
from lerobocasa.environments.kitchen.composite.baking.cool_baked_cake import (
    CoolBakedCake,
)
from lerobocasa.environments.kitchen.composite.baking.cool_baked_cookies import (
    CoolBakedCookies,
)
from lerobocasa.environments.kitchen.composite.baking.cupcake_cleanup import (
    CupcakeCleanup,
)
from lerobocasa.environments.kitchen.composite.baking.mix_cake_frosting import (
    MixCakeFrosting,
)
from lerobocasa.environments.kitchen.composite.baking.organize_baking_ingredients import (
    OrganizeBakingIngredients,
)
from lerobocasa.environments.kitchen.composite.baking.pastry_display import (
    PastryDisplay,
)
from lerobocasa.environments.kitchen.composite.boiling.boil_pot import BoilPot
from lerobocasa.environments.kitchen.composite.boiling.boil_corn import BoilCorn
from lerobocasa.environments.kitchen.composite.boiling.boil_eggs import BoilEggs
from lerobocasa.environments.kitchen.composite.boiling.cool_kettle import CoolKettle
from lerobocasa.environments.kitchen.composite.boiling.fill_kettle import FillKettle
from lerobocasa.environments.kitchen.composite.boiling.heat_multiple_water import (
    HeatMultipleWater,
)
from lerobocasa.environments.kitchen.composite.boiling.place_lid_to_boil import (
    PlaceLidToBoil,
)
from lerobocasa.environments.kitchen.composite.boiling.start_electric_kettle import (
    StartElectricKettle,
)
from lerobocasa.environments.kitchen.composite.brewing.arrange_tea import ArrangeTea
from lerobocasa.environments.kitchen.composite.brewing.deliver_brewed_coffee import (
    DeliverBrewedCoffee,
)
from lerobocasa.environments.kitchen.composite.brewing.kettle_boiling import (
    KettleBoiling,
)
from lerobocasa.environments.kitchen.composite.brewing.organize_coffee_condiments import (
    OrganizeCoffeeCondiments,
)
from lerobocasa.environments.kitchen.composite.brewing.prepare_coffee import (
    PrepareCoffee,
)
from lerobocasa.environments.kitchen.composite.brewing.sweeten_coffee import (
    SweetenCoffee,
)
from lerobocasa.environments.kitchen.composite.broiling_fish.oven_broil_fish import (
    OvenBroilFish,
)
from lerobocasa.environments.kitchen.composite.broiling_fish.prepare_broiling_station import (
    PrepareBroilingStation,
)
from lerobocasa.environments.kitchen.composite.broiling_fish.remove_broiled_fish import (
    RemoveBroiledFish,
)
from lerobocasa.environments.kitchen.composite.broiling_fish.toaster_oven_broil_fish import (
    ToasterOvenBroilFish,
)
from lerobocasa.environments.kitchen.composite.broiling_fish.wash_fish import (
    WashFish,
)
from lerobocasa.environments.kitchen.composite.chopping_food.arrange_cutting_fruits import (
    ArrangeCuttingFruits,
)
from lerobocasa.environments.kitchen.composite.chopping_food.arrange_vegetables import (
    ArrangeVegetables,
)
from lerobocasa.environments.kitchen.composite.chopping_food.bread_setup_slicing import (
    BreadSetupSlicing,
)
from lerobocasa.environments.kitchen.composite.chopping_food.clear_cutting_board import (
    ClearCuttingBoard,
)
from lerobocasa.environments.kitchen.composite.chopping_food.meat_transfer import (
    MeatTransfer,
)
from lerobocasa.environments.kitchen.composite.chopping_food.organize_vegetables import (
    OrganizeVegetables,
)
from lerobocasa.environments.kitchen.composite.chopping_vegetables.gather_cutting_tools import (
    GatherCuttingTools,
)
from lerobocasa.environments.kitchen.composite.chopping_vegetables.cutting_tool_selection import (
    CuttingToolSelection,
)
from lerobocasa.environments.kitchen.composite.cleaning_appliances.clean_blender_jug import (
    CleanBlenderJug,
)
from lerobocasa.environments.kitchen.composite.cleaning_appliances.prep_fridge_for_cleaning import (
    PrepFridgeForCleaning,
)
from lerobocasa.environments.kitchen.composite.cleaning_appliances.prep_sink_for_cleaning import (
    PrepSinkForCleaning,
)
from lerobocasa.environments.kitchen.composite.cleaning_sink.clear_food_waste import (
    ClearFoodWaste,
)
from lerobocasa.environments.kitchen.composite.cleaning_sink.clear_sink_area import (
    ClearSinkArea,
)
from lerobocasa.environments.kitchen.composite.cleaning_sink.rinse_sink_basin import (
    RinseSinkBasin,
)
from lerobocasa.environments.kitchen.composite.clearing_table.bowl_and_cup import (
    BowlAndCup,
)
from lerobocasa.environments.kitchen.composite.clearing_table.candle_cleanup import (
    CandleCleanup,
)
from lerobocasa.environments.kitchen.composite.clearing_table.clear_receptacles_for_cleaning import (
    ClearReceptaclesForCleaning,
)
from lerobocasa.environments.kitchen.composite.clearing_table.cluster_items_for_clearing import (
    ClusterItemsForClearing,
)
from lerobocasa.environments.kitchen.composite.clearing_table.condiment_collection import (
    CondimentCollection,
)
from lerobocasa.environments.kitchen.composite.clearing_table.dessert_assembly import (
    DessertAssembly,
)
from lerobocasa.environments.kitchen.composite.clearing_table.drinkware_consolidation import (
    DrinkwareConsolidation,
)
from lerobocasa.environments.kitchen.composite.clearing_table.food_cleanup import (
    FoodCleanup,
)
from lerobocasa.environments.kitchen.composite.defrosting_food.defrost_by_category import (
    DefrostByCategory,
)
from lerobocasa.environments.kitchen.composite.defrosting_food.microwave_thawing import (
    MicrowaveThawing,
)
from lerobocasa.environments.kitchen.composite.defrosting_food.microwave_thawing_fridge import (
    MicrowaveThawingFridge,
)
from lerobocasa.environments.kitchen.composite.defrosting_food.move_to_counter import (
    MoveToCounter,
)
from lerobocasa.environments.kitchen.composite.defrosting_food.quick_thaw import (
    QuickThaw,
)
from lerobocasa.environments.kitchen.composite.defrosting_food.thaw_in_sink import (
    ThawInSink,
)
from lerobocasa.environments.kitchen.composite.filling_serving_dishes.build_appetizer_plate import (
    BuildAppetizerPlate,
)
from lerobocasa.environments.kitchen.composite.filling_serving_dishes.display_meat_variety import (
    DisplayMeatVariety,
)
from lerobocasa.environments.kitchen.composite.filling_serving_dishes.meat_skewer_assembly import (
    MeatSkewerAssembly,
)
from lerobocasa.environments.kitchen.composite.filling_serving_dishes.mixed_fruit_platter import (
    MixedFruitPlatter,
)
from lerobocasa.environments.kitchen.composite.frying.assemble_cooking_array import (
    AssembleCookingArray,
)
from lerobocasa.environments.kitchen.composite.frying.distribute_steak_on_pans import (
    DistributeSteakOnPans,
)
from lerobocasa.environments.kitchen.composite.frying.frying_pan_adjustment import (
    FryingPanAdjustment,
)
from lerobocasa.environments.kitchen.composite.frying.meal_prep_staging import (
    MealPrepStaging,
)
from lerobocasa.environments.kitchen.composite.frying.press_chicken import (
    PressChicken,
)
from lerobocasa.environments.kitchen.composite.frying.rotate_pan import (
    RotatePan,
)
from lerobocasa.environments.kitchen.composite.frying.searing_meat import SearingMeat
from lerobocasa.environments.kitchen.composite.frying.setup_frying import SetupFrying
from lerobocasa.environments.kitchen.composite.garnishing_dishes.add_lemon_to_fish import (
    AddLemonToFish,
)
from lerobocasa.environments.kitchen.composite.garnishing_dishes.add_sugar_cubes import (
    AddSugarCubes,
)
from lerobocasa.environments.kitchen.composite.garnishing_dishes.garnish_cake import (
    GarnishCake,
)
from lerobocasa.environments.kitchen.composite.garnishing_dishes.garnish_cupcake import (
    GarnishCupcake,
)
from lerobocasa.environments.kitchen.composite.garnishing_dishes.garnish_pancake import (
    GarnishPancake,
)
from lerobocasa.environments.kitchen.composite.loading_dishwasher.load_dishwasher import (
    LoadDishwasher,
)
from lerobocasa.environments.kitchen.composite.loading_dishwasher.prepare_dishwasher import (
    PrepareDishwasher,
)
from lerobocasa.environments.kitchen.composite.loading_fridge.create_child_friendly_fridge import (
    CreateChildFriendlyFridge,
)
from lerobocasa.environments.kitchen.composite.loading_fridge.load_condiments_in_fridge import (
    LoadCondimentsInFridge,
)
from lerobocasa.environments.kitchen.composite.loading_fridge.load_fridge_by_type import (
    LoadFridgeByType,
)
from lerobocasa.environments.kitchen.composite.loading_fridge.load_fridge_fifo import (
    LoadFridgeFifo,
)
from lerobocasa.environments.kitchen.composite.loading_fridge.load_prepared_food import (
    LoadPreparedFood,
)
from lerobocasa.environments.kitchen.composite.loading_fridge.move_freezer_to_fridge import (
    MoveFreezerToFridge,
)
from lerobocasa.environments.kitchen.composite.loading_fridge.place_veggies_in_drawer import (
    PlaceVeggiesInDrawer,
)
from lerobocasa.environments.kitchen.composite.loading_fridge.rearrange_fridge_items import (
    RearrangeFridgeItems,
)
from lerobocasa.environments.kitchen.composite.making_juice.choose_ripe_fruit import (
    ChooseRipeFruit,
)
from lerobocasa.environments.kitchen.composite.making_juice.juice_fruit_reamer import (
    JuiceFruitReamer,
)
from lerobocasa.environments.kitchen.composite.making_juice.fill_blender_jug import (
    FillBlenderJug,
)
from lerobocasa.environments.kitchen.composite.making_salads.prepare_cheese_station import (
    PrepareCheeseStation,
)
from lerobocasa.environments.kitchen.composite.making_salads.wash_lettuce import (
    WashLettuce,
)
from lerobocasa.environments.kitchen.composite.making_smoothies.add_ice_cubes import (
    AddIceCubes,
)
from lerobocasa.environments.kitchen.composite.making_smoothies.add_sweetener import (
    AddSweetener,
)
from lerobocasa.environments.kitchen.composite.making_smoothies.blend_ingredients import (
    BlendIngredients,
)
from lerobocasa.environments.kitchen.composite.making_smoothies.place_straw import (
    PlaceStraw,
)
from lerobocasa.environments.kitchen.composite.making_smoothies.prepare_smoothie import (
    PrepareSmoothie,
)
from lerobocasa.environments.kitchen.composite.making_tea.arrange_tea_accompaniments import (
    ArrangeTeaAccompaniments,
)
from lerobocasa.environments.kitchen.composite.making_tea.serve_tea import (
    ServeTea,
)
from lerobocasa.environments.kitchen.composite.making_tea.strainer_setup import (
    StrainerSetup,
)
from lerobocasa.environments.kitchen.composite.making_toast.bread_selection import (
    BreadSelection,
)
from lerobocasa.environments.kitchen.composite.making_toast.prepare_toast import (
    PrepareToast,
)
from lerobocasa.environments.kitchen.composite.making_toast.sweet_savory_toast_setup import (
    SweetSavoryToastSetup,
)
from lerobocasa.environments.kitchen.composite.managing_freezer_space.clear_freezer import (
    ClearFreezer,
)
from lerobocasa.environments.kitchen.composite.managing_freezer_space.freeze_bottled_waters import (
    FreezeBottledWaters,
)
from lerobocasa.environments.kitchen.composite.managing_freezer_space.freeze_ice_tray import (
    FreezeIceTray,
)
from lerobocasa.environments.kitchen.composite.managing_freezer_space.maximize_freezer_space import (
    MaximizeFreezerSpace,
)
from lerobocasa.environments.kitchen.composite.managing_freezer_space.move_fridge_to_freezer import (
    MoveFridgeToFreezer,
)
from lerobocasa.environments.kitchen.composite.managing_freezer_space.move_to_freezer_drawer import (
    MoveToFreezerDrawer,
)
from lerobocasa.environments.kitchen.composite.managing_freezer_space.reorganize_frozen_vegetables import (
    ReorganizeFrozenVegetables,
)
from lerobocasa.environments.kitchen.composite.managing_freezer_space.separate_freezer_rack import (
    SeparateFreezerRack,
)
from lerobocasa.environments.kitchen.composite.measuring_ingredients.choose_measuring_cup import (
    ChooseMeasuringCup,
)
from lerobocasa.environments.kitchen.composite.measuring_ingredients.organize_measuring_cups import (
    OrganizeMeasuringCups,
)
from lerobocasa.environments.kitchen.composite.measuring_ingredients.weigh_ingredients import (
    WeighIngredients,
)
from lerobocasa.environments.kitchen.composite.meat_preparation.prep_for_tenderizing import (
    PrepForTenderizing,
)
from lerobocasa.environments.kitchen.composite.meat_preparation.prep_marinating_meat import (
    PrepMarinatingMeat,
)
from lerobocasa.environments.kitchen.composite.microwaving_food.filter_microwavable_item import (
    FilterMicrowavableItem,
)
from lerobocasa.environments.kitchen.composite.microwaving_food.microwave_correct_meal import (
    MicrowaveCorrectMeal,
)
from lerobocasa.environments.kitchen.composite.microwaving_food.microwave_defrost_meat import (
    MicrowaveDefrostMeat,
)
from lerobocasa.environments.kitchen.composite.microwaving_food.place_microwave_safe_item import (
    PlaceMicrowaveSafeItem,
)
from lerobocasa.environments.kitchen.composite.microwaving_food.reheat_meal import (
    ReheatMeal,
)
from lerobocasa.environments.kitchen.composite.microwaving_food.return_heated_food import (
    ReturnHeatedFood,
)
from lerobocasa.environments.kitchen.composite.preparing_marinade.blend_marinade import (
    BlendMarinade,
)
from lerobocasa.environments.kitchen.composite.preparing_marinade.gather_marinade_ingredients import (
    GatherMarinadeIngredients,
)
from lerobocasa.environments.kitchen.composite.preparing_marinade.place_meat_in_marinade import (
    PlaceMeatInMarinade,
)
from lerobocasa.environments.kitchen.composite.mixing_and_blending.colorful_salsa import (
    ColorfulSalsa,
)
from lerobocasa.environments.kitchen.composite.mixing_and_blending.make_banana_milkshake import (
    MakeBananaMilkshake,
)
from lerobocasa.environments.kitchen.composite.mixing_and_blending.spicy_marinade import (
    SpicyMarinade,
)
from lerobocasa.environments.kitchen.composite.mixing_ingredients.blend_salsa_mix import (
    BlendSalsaMix,
)
from lerobocasa.environments.kitchen.composite.mixing_ingredients.blend_vegetable_sauce import (
    BlendVegetableSauce,
)
from lerobocasa.environments.kitchen.composite.mixing_ingredients.cheese_mixing import (
    CheeseMixing,
)
from lerobocasa.environments.kitchen.composite.mixing_ingredients.make_cheesecake_filling import (
    MakeCheesecakeFilling,
)
from lerobocasa.environments.kitchen.composite.mixing_ingredients.make_chocolate_milk import (
    MakeChocolateMilk,
)
from lerobocasa.environments.kitchen.composite.mixing_ingredients.prepare_veggie_dip import (
    PrepareVeggieDip,
)
from lerobocasa.environments.kitchen.composite.plating_food.balanced_meal_prep import (
    BalancedMealPrep,
)
from lerobocasa.environments.kitchen.composite.plating_food.plate_steak_meal import (
    PlateSteakMeal,
)
from lerobocasa.environments.kitchen.composite.plating_food.plate_store_dinner import (
    PlateStoreDinner,
)
from lerobocasa.environments.kitchen.composite.portioning_meals.distribute_chicken import (
    DistributeChicken,
)
from lerobocasa.environments.kitchen.composite.portioning_meals.portion_fruit_bowl import (
    PortionFruitBowl,
)
from lerobocasa.environments.kitchen.composite.portioning_meals.portion_hot_dogs import (
    PortionHotDogs,
)
from lerobocasa.environments.kitchen.composite.portioning_meals.portion_in_tupperware import (
    PortionInTupperware,
)
from lerobocasa.environments.kitchen.composite.portioning_meals.portion_on_size import (
    PortionOnSize,
)
from lerobocasa.environments.kitchen.composite.portioning_meals.portion_yogurt import (
    PortionYogurt,
)
from lerobocasa.environments.kitchen.composite.portioning_meals.scale_portioning import (
    ScalePortioning,
)
from lerobocasa.environments.kitchen.composite.sorting_ingredients.separate_raw_ingredients import (
    SeparateRawIngredients,
)
from lerobocasa.environments.kitchen.composite.sorting_ingredients.sort_breakfast_ingredients import (
    SortBreakfastIngredients,
)
from lerobocasa.environments.kitchen.composite.organizing_dishes_and_containers.empty_dish_rack import (
    EmptyDishRack,
)
from lerobocasa.environments.kitchen.composite.organizing_dishes_and_containers.organize_mugs_by_handle import (
    OrganizeMugsByHandle,
)
from lerobocasa.environments.kitchen.composite.organizing_dishes_and_containers.stack_bowls_cabinet import (
    StackBowlsCabinet,
)
from lerobocasa.environments.kitchen.composite.organizing_recycling.recycle_bottles_by_size import (
    RecycleBottlesBySize,
)
from lerobocasa.environments.kitchen.composite.organizing_recycling.recycle_bottles_by_type import (
    RecycleBottlesByType,
)
from lerobocasa.environments.kitchen.composite.organizing_recycling.recycle_soda_cans import (
    RecycleSodaCans,
)
from lerobocasa.environments.kitchen.composite.organizing_recycling.recycle_stacked_yogurt import (
    RecycleStackedYogurt,
)
from lerobocasa.environments.kitchen.composite.organizing_utensils.arrange_utensils_by_type import (
    ArrangeUtensilsByType,
)
from lerobocasa.environments.kitchen.composite.organizing_utensils.cluster_utensils_in_drawer import (
    ClusterUtensilsInDrawer,
)
from lerobocasa.environments.kitchen.composite.organizing_utensils.organize_metalic_utensils import (
    OrganizeMetallicUtensils,
)
from lerobocasa.environments.kitchen.composite.packing_lunches.pack_food_by_temp import (
    PackFoodByTemp,
)
from lerobocasa.environments.kitchen.composite.packing_lunches.pack_fruit_container import (
    PackFruitContainer,
)
from lerobocasa.environments.kitchen.composite.packing_lunches.pack_identical_lunches import (
    PackIdenticalLunches,
)
from lerobocasa.environments.kitchen.composite.packing_lunches.pack_snack import (
    PackSnack,
)
from lerobocasa.environments.kitchen.composite.preparing_hot_chocolate.add_marshmallow import (
    AddMarshmallow,
)
from lerobocasa.environments.kitchen.composite.preparing_hot_chocolate.sweeten_hot_chocolate import (
    SweetenHotChocolate,
)
from lerobocasa.environments.kitchen.composite.preparing_sandwiches.gather_vegetables import (
    GatherVegetables,
)
from lerobocasa.environments.kitchen.composite.preparing_sandwiches.heat_kebab_sandwich import (
    HeatKebabSandwich,
)
from lerobocasa.environments.kitchen.composite.preparing_sandwiches.hot_dog_setup import (
    HotDogSetup,
)
from lerobocasa.environments.kitchen.composite.preparing_sandwiches.prepare_sandwich_station import (
    PrepareSandwichStation,
)
from lerobocasa.environments.kitchen.composite.preparing_sandwiches.prepare_sausage_cheese import (
    PrepareSausageCheese,
)
from lerobocasa.environments.kitchen.composite.preparing_sandwiches.toast_heatable_ingredients import (
    ToastHeatableIngredients,
)
from lerobocasa.environments.kitchen.composite.reheating_food.heat_mug import HeatMug
from lerobocasa.environments.kitchen.composite.reheating_food.make_loaded_potato import (
    MakeLoadedPotato,
)
from lerobocasa.environments.kitchen.composite.reheating_food.reheat_meat_on_stove import (
    ReheatMeatOnStove,
)
from lerobocasa.environments.kitchen.composite.reheating_food.simmering_sauce import (
    SimmeringSauce,
)
from lerobocasa.environments.kitchen.composite.reheating_food.waffle_reheat import (
    WaffleReheat,
)
from lerobocasa.environments.kitchen.composite.reheating_food.warm_croissant import (
    WarmCroissant,
)
from lerobocasa.environments.kitchen.composite.restocking_supplies.beverage_sorting import (
    BeverageSorting,
)
from lerobocasa.environments.kitchen.composite.restocking_supplies.fresh_produce_organization import (
    FreshProduceOrganization,
)
from lerobocasa.environments.kitchen.composite.restocking_supplies.refill_condiment_station import (
    RefillCondimentStation,
)
from lerobocasa.environments.kitchen.composite.restocking_supplies.restock_bowls import (
    RestockBowls,
)
from lerobocasa.environments.kitchen.composite.restocking_supplies.restock_canned_food import (
    RestockCannedFood,
)
from lerobocasa.environments.kitchen.composite.restocking_supplies.restock_pantry import (
    RestockPantry,
)
from lerobocasa.environments.kitchen.composite.restocking_supplies.restock_sink_supplies import (
    RestockSinkSupplies,
)
from lerobocasa.environments.kitchen.composite.restocking_supplies.stocking_breakfast_foods import (
    StockingBreakfastFoods,
)
from lerobocasa.environments.kitchen.composite.sanitizing_cutting_board.remove_cutting_board_items import (
    RemoveCuttingBoardItems,
)
from lerobocasa.environments.kitchen.composite.sanitizing_cutting_board.rinse_cutting_board import (
    RinseCuttingBoard,
)
from lerobocasa.environments.kitchen.composite.sanitizing_cutting_board.sanitize_prep_cutting_board import (
    SanitizePrepCuttingBoard,
)
from lerobocasa.environments.kitchen.composite.sanitizing_cutting_board.scrub_cutting_board import (
    ScrubCuttingBoard,
)
from lerobocasa.environments.kitchen.composite.sanitizing_surface.arrange_sink_sanitization import (
    ArrangeSinkSanitization,
)
from lerobocasa.environments.kitchen.composite.sanitizing_surface.clean_microwave import (
    CleanMicrowave,
)
from lerobocasa.environments.kitchen.composite.sanitizing_surface.countertop_cleanup import (
    CountertopCleanup,
)
from lerobocasa.environments.kitchen.composite.sanitizing_surface.prep_for_sanitizing import (
    PrepForSanitizing,
)
from lerobocasa.environments.kitchen.composite.sanitizing_surface.sanitize_sink import (
    SanitizeSink,
)
from lerobocasa.environments.kitchen.composite.sanitizing_surface.wipe_table import (
    WipeTable,
)
from lerobocasa.environments.kitchen.composite.sauteing_vegetables.adjust_heat import (
    AdjustHeat,
)
from lerobocasa.environments.kitchen.composite.sauteing_vegetables.butter_on_pan import (
    ButterOnPan,
)
from lerobocasa.environments.kitchen.composite.sauteing_vegetables.place_vegetables_evenly import (
    PlaceVegetablesEvenly,
)
from lerobocasa.environments.kitchen.composite.sauteing_vegetables.preheat_pot import (
    PreheatPot,
)
from lerobocasa.environments.kitchen.composite.sauteing_vegetables.shake_pan import (
    ShakePan,
)
from lerobocasa.environments.kitchen.composite.sauteing_vegetables.stir_vegetables import (
    StirVegetables,
)
from lerobocasa.environments.kitchen.composite.sauteing_vegetables.tilt_pan import (
    TiltPan,
)
from lerobocasa.environments.kitchen.composite.seasoning_food.lemon_seasoning_fish import (
    LemonSeasoningFish,
)
from lerobocasa.environments.kitchen.composite.seasoning_food.seasoning_steak import (
    SeasoningSteak,
)
from lerobocasa.environments.kitchen.composite.seasoning_food.setup_spice_station import (
    SetUpSpiceStation,
)
from lerobocasa.environments.kitchen.composite.serving_beverages.deliver_straw import (
    DeliverStraw,
)
from lerobocasa.environments.kitchen.composite.serving_beverages.match_cup_and_drink import (
    MatchCupAndDrink,
)
from lerobocasa.environments.kitchen.composite.serving_beverages.prepare_cocktail_station import (
    PrepareCocktailStation,
)
from lerobocasa.environments.kitchen.composite.serving_beverages.prepare_drink_station import (
    PrepareDrinkStation,
)
from lerobocasa.environments.kitchen.composite.serving_beverages.serve_meal_juice import (
    ServeMealJuice,
)
from lerobocasa.environments.kitchen.composite.serving_beverages.setup_soda_bowl import (
    SetupSodaBowl,
)
from lerobocasa.environments.kitchen.composite.serving_food.dessert_upgrade import (
    DessertUpgrade,
)
from lerobocasa.environments.kitchen.composite.serving_food.pan_transfer import (
    PanTransfer,
)
from lerobocasa.environments.kitchen.composite.serving_food.place_food_in_bowls import (
    PlaceFoodInBowls,
)
from lerobocasa.environments.kitchen.composite.serving_food.prepare_soup_serving import (
    PrepareSoupServing,
)
from lerobocasa.environments.kitchen.composite.serving_food.serve_steak import (
    ServeSteak,
)
from lerobocasa.environments.kitchen.composite.serving_food.alcohol_serving_prep import (
    AlcoholServingPrep,
)
from lerobocasa.environments.kitchen.composite.setting_the_table.align_silverware import (
    AlignSilverware,
)
from lerobocasa.environments.kitchen.composite.setting_the_table.arrange_bread_basket import (
    ArrangeBreadBasket,
)
from lerobocasa.environments.kitchen.composite.setting_the_table.arrange_bread_bowl import (
    ArrangeBreadBowl,
)
from lerobocasa.environments.kitchen.composite.setting_the_table.arrange_drinkware import (
    ArrangeDrinkware,
)
from lerobocasa.environments.kitchen.composite.setting_the_table.beverage_organization import (
    BeverageOrganization,
)
from lerobocasa.environments.kitchen.composite.setting_the_table.date_night import (
    DateNight,
)
from lerobocasa.environments.kitchen.composite.setting_the_table.setup_bowls import (
    SetupBowls,
)
from lerobocasa.environments.kitchen.composite.setting_the_table.setup_butter_plate import (
    SetupButterPlate,
)
from lerobocasa.environments.kitchen.composite.setting_the_table.setup_fruit_bowl import (
    SetupFruitBowl,
)
from lerobocasa.environments.kitchen.composite.setting_the_table.setup_wine_glasses import (
    SetupWineGlasses,
)
from lerobocasa.environments.kitchen.composite.setting_the_table.seasoning_spice_setup import (
    SeasoningSpiceSetup,
)
from lerobocasa.environments.kitchen.composite.setting_the_table.set_bowls_for_soup import (
    SetBowlsForSoup,
)
from lerobocasa.environments.kitchen.composite.setting_the_table.size_sorting import (
    SizeSorting,
)
from lerobocasa.environments.kitchen.composite.slicing_meat.retrieve_meat import (
    RetrieveMeat,
)
from lerobocasa.environments.kitchen.composite.slicing_meat.clean_board import (
    CleanBoard,
)
from lerobocasa.environments.kitchen.composite.slicing_meat.set_up_cutting_station import (
    SetUpCuttingStation,
)
from lerobocasa.environments.kitchen.composite.slow_cooking.add_to_soup_pot import (
    AddToSoupPot,
)
from lerobocasa.environments.kitchen.composite.slow_cooking.begin_slow_cooking import (
    BeginSlowCooking,
)
from lerobocasa.environments.kitchen.composite.slow_cooking.stop_slow_cooking import (
    StopSlowCooking,
)
from lerobocasa.environments.kitchen.composite.simmering_sauces.turn_off_simmered_sauce_heat import (
    TurnOffSimmeredSauceHeat,
)
from lerobocasa.environments.kitchen.composite.snack_preparation.bread_and_cheese import (
    BreadAndCheese,
)
from lerobocasa.environments.kitchen.composite.snack_preparation.cereal_and_bowl import (
    CerealAndBowl,
)
from lerobocasa.environments.kitchen.composite.snack_preparation.make_fruit_bowl import (
    MakeFruitBowl,
)
from lerobocasa.environments.kitchen.composite.snack_preparation.veggie_dip_prep import (
    VeggieDipPrep,
)
from lerobocasa.environments.kitchen.composite.snack_preparation.yogurt_delight_prep import (
    YogurtDelightPrep,
)
from lerobocasa.environments.kitchen.composite.steaming_food.multistep_steaming import (
    MultistepSteaming,
)
from lerobocasa.environments.kitchen.composite.steaming_food.steam_fish import (
    SteamFish,
)
from lerobocasa.environments.kitchen.composite.steaming_food.steam_in_microwave import (
    SteamInMicrowave,
)
from lerobocasa.environments.kitchen.composite.steaming_vegetables.prepare_veggies_for_steaming import (
    PrepareVeggiesForSteaming,
)
from lerobocasa.environments.kitchen.composite.steaming_vegetables.remove_steamed_vegetables import (
    RemoveSteamedVegetables,
)
from lerobocasa.environments.kitchen.composite.steaming_vegetables.steam_veggies_with_water import (
    SteamVeggiesWithWater,
)
from lerobocasa.environments.kitchen.composite.storing_leftovers.freeze_cooked_food import (
    FreezeCookedFood,
)
from lerobocasa.environments.kitchen.composite.storing_leftovers.prepare_storing_leftovers import (
    PrepareStoringLeftovers,
)
from lerobocasa.environments.kitchen.composite.storing_leftovers.store_dumplings import (
    StoreDumplings,
)
from lerobocasa.environments.kitchen.composite.storing_leftovers.store_leftovers_by_type import (
    StoreLeftoversByType,
)
from lerobocasa.environments.kitchen.composite.storing_leftovers.store_leftovers_in_bowl import (
    StoreLeftoversInBowl,
)
from lerobocasa.environments.kitchen.composite.tidying_cabinets_and_drawers.drawer_utensil_sort import (
    DrawerUtensilSort,
)
from lerobocasa.environments.kitchen.composite.tidying_cabinets_and_drawers.organize_cleaning_supplies import (
    OrganizeCleaningSupplies,
)
from lerobocasa.environments.kitchen.composite.tidying_cabinets_and_drawers.place_breakfast_items_away import (
    PlaceBreakfastItemsAway,
)
from lerobocasa.environments.kitchen.composite.tidying_cabinets_and_drawers.utensil_shuffle import (
    UtensilShuffle,
)
from lerobocasa.environments.kitchen.composite.tidying_cabinets_and_drawers.snack_sorting import (
    SnackSorting,
)
from lerobocasa.environments.kitchen.composite.toasting_bread.get_toasted_bread import (
    GetToastedBread,
)
from lerobocasa.environments.kitchen.composite.toasting_bread.pj_sandwich_prep import (
    PJSandwichPrep,
)
from lerobocasa.environments.kitchen.composite.toasting_bread.serve_warm_croissant import (
    ServeWarmCroissant,
)
from lerobocasa.environments.kitchen.composite.toasting_bread.toast_bagel import (
    ToastBagel,
)
from lerobocasa.environments.kitchen.composite.toasting_bread.toast_baguette import (
    ToastBaguette,
)
from lerobocasa.environments.kitchen.composite.toasting_bread.toast_on_correct_rack import (
    ToastOnCorrectRack,
)
from lerobocasa.environments.kitchen.composite.toasting_bread.toast_one_slot_pair import (
    ToastOneSlotPair,
)
from lerobocasa.environments.kitchen.composite.washing_dishes.clear_sink import (
    ClearSink,
)
from lerobocasa.environments.kitchen.composite.washing_dishes.collect_washing_supplies import (
    CollectWashingSupplies,
)
from lerobocasa.environments.kitchen.composite.washing_dishes.divide_basins import (
    DivideBasins,
)
from lerobocasa.environments.kitchen.composite.washing_dishes.dry_dishes import (
    DryDishes,
)
from lerobocasa.environments.kitchen.composite.washing_dishes.dry_drinkware import (
    DryDrinkware,
)
from lerobocasa.environments.kitchen.composite.washing_dishes.dump_leftovers import (
    DumpLeftovers,
)
from lerobocasa.environments.kitchen.composite.washing_dishes.place_dishes_by_sink import (
    PlaceDishesBySink,
)
from lerobocasa.environments.kitchen.composite.washing_dishes.place_on_dish_rack import (
    PlaceOnDishRack,
)
from lerobocasa.environments.kitchen.composite.washing_dishes.pre_rinse_station import (
    PreRinseStation,
)
from lerobocasa.environments.kitchen.composite.washing_dishes.pre_soak_pan import (
    PreSoakPan,
)
from lerobocasa.environments.kitchen.composite.washing_dishes.return_washing_supplies import (
    ReturnWashingSupplies,
)
from lerobocasa.environments.kitchen.composite.washing_dishes.rinse_bowls import (
    RinseBowls,
)
from lerobocasa.environments.kitchen.composite.washing_dishes.rinse_fragile_item import (
    RinseFragileItem,
)
from lerobocasa.environments.kitchen.composite.washing_dishes.scrub_bowl import (
    ScrubBowl,
)
from lerobocasa.environments.kitchen.composite.washing_dishes.soak_sponge import (
    SoakSponge,
)
from lerobocasa.environments.kitchen.composite.washing_dishes.sorting_cleanup import (
    SortingCleanup,
)
from lerobocasa.environments.kitchen.composite.washing_dishes.stack_bowls import (
    StackBowlsInSink,
)
from lerobocasa.environments.kitchen.composite.washing_dishes.transport_cookware import (
    TransportCookware,
)
from lerobocasa.environments.kitchen.composite.washing_fruits_and_vegetables.afterwash_sorting import (
    AfterwashSorting,
)
from lerobocasa.environments.kitchen.composite.washing_fruits_and_vegetables.airdry_fruit import (
    AirDryFruit,
)
from lerobocasa.environments.kitchen.composite.washing_fruits_and_vegetables.clear_clutter import (
    ClearClutter,
)
from lerobocasa.environments.kitchen.composite.washing_fruits_and_vegetables.drain_veggies import (
    DrainVeggies,
)
from lerobocasa.environments.kitchen.composite.washing_fruits_and_vegetables.clear_sink_space import (
    ClearSinkSpace,
)
from lerobocasa.environments.kitchen.composite.washing_fruits_and_vegetables.gather_produce_washing import (
    GatherProduceWashing,
)
from lerobocasa.environments.kitchen.composite.washing_fruits_and_vegetables.prepare_vegetable_roasting import (
    PrepareVegetableRoasting,
)
from lerobocasa.environments.kitchen.composite.washing_fruits_and_vegetables.prewash_food_assembly import (
    PrewashFoodAssembly,
)
from lerobocasa.environments.kitchen.composite.washing_fruits_and_vegetables.prewash_food_sorting import (
    PrewashFoodSorting,
)
from lerobocasa.environments.kitchen.composite.washing_fruits_and_vegetables.wash_fruit_colander import (
    WashFruitColander,
)
from lerobocasa.environments.kitchen.composite.washing_fruits_and_vegetables.wash_in_saucepan import (
    WashInSaucepan,
)

from lerobocasa.environments.kitchen.atomic.kitchen_blender import (
    CloseBlenderLid,
    OpenBlenderLid,
    TurnOnBlender,
)

from lerobocasa.environments.kitchen.atomic.kitchen_coffee import (
    StartCoffeeMachine,
    CoffeeServeMug,
    CoffeeSetupMug,
)
from lerobocasa.environments.kitchen.atomic.kitchen_doors import (
    OpenDoor,
    CloseDoor,
    OpenCabinet,
    CloseCabinet,
    OpenMicrowave,
    CloseMicrowave,
    OpenFridge,
    CloseFridge,
    OpenDishwasher,
    CloseDishwasher,
    OpenToasterOvenDoor,
    CloseToasterOvenDoor,
    OpenOven,
    CloseOven,
)
from lerobocasa.environments.kitchen.atomic.kitchen_drawer import (
    OpenDrawer,
    CloseDrawer,
    SlideDishwasherRack,
    OpenFridgeDrawer,
    CloseFridgeDrawer,
)
from lerobocasa.environments.kitchen.atomic.kitchen_electric_kettle import (
    CloseElectricKettleLid,
    OpenElectricKettleLid,
    TurnOnElectricKettle,
)
from lerobocasa.environments.kitchen.atomic.kitchen_microwave import (
    TurnOnMicrowave,
    TurnOffMicrowave,
)
from lerobocasa.environments.kitchen.atomic.kitchen_navigate import NavigateKitchen

from lerobocasa.environments.kitchen.atomic.kitchen_oven import (
    PreheatOven,
    SlideOvenRack,
)

from lerobocasa.environments.kitchen.atomic.kitchen_pick_place import (
    CheesyBread,
    MakeIcedCoffee,
    PackDessert,
    PickPlaceCounterToCabinet,
    PickPlaceCabinetToCounter,
    PickPlaceCounterToMicrowave,
    PickPlaceMicrowaveToCounter,
    PickPlaceCounterToSink,
    PickPlaceSinkToCounter,
    PickPlaceCounterToStove,
    PickPlaceStoveToCounter,
    PickPlaceCounterToOven,
    PickPlaceToasterToCounter,
    PickPlaceCounterToToasterOven,
    PickPlaceToasterOvenToCounter,
    PickPlaceCounterToStandMixer,
    PickPlaceCounterToBlender,
    PickPlaceFridgeShelfToDrawer,
    PickPlaceFridgeDrawerToShelf,
    PickPlaceCounterToDrawer,
    PickPlaceDrawerToCounter,
)
from lerobocasa.environments.kitchen.atomic.kitchen_sink import (
    TurnOnSinkFaucet,
    TurnOffSinkFaucet,
    TurnSinkSpout,
    AdjustWaterTemperature,
)
from lerobocasa.environments.kitchen.atomic.kitchen_stand_mixer import (
    OpenStandMixerHead,
    CloseStandMixerHead,
)
from lerobocasa.environments.kitchen.atomic.kitchen_stove import (
    LowerHeat,
    TurnOnStove,
    TurnOffStove,
)
from lerobocasa.environments.kitchen.atomic.kitchen_toaster_oven import (
    AdjustToasterOvenTemperature,
    SlideToasterOvenRack,
    TurnOnToasterOven,
)
from lerobocasa.environments.kitchen.atomic.kitchen_toaster import (
    TurnOnToaster,
)

try:
    import mimicgen
except ImportError:
    print(
        "WARNING: mimicgen environments not imported since mimicgen is not installed!"
    )

from lerobocasa.environments import ALL_KITCHEN_ENVIRONMENTS

# for gym environment compatibility
from lerobocasa.wrappers.gym_wrapper import RoboCasaGymEnv

# from robosuite.controllers import ALL_CONTROLLERS, load_controller_config
from robosuite.controllers import ALL_PART_CONTROLLERS, load_composite_controller_config
from robosuite.environments import ALL_ENVIRONMENTS
from robosuite.models.grippers import ALL_GRIPPERS
from robosuite.robots import ALL_ROBOTS

import mujoco

assert (
    mujoco.__version__ == "3.3.1"
), "MuJoCo version must be 3.3.1. Please run pip install mujoco==3.3.1"

import numpy

assert numpy.__version__ in [
    "2.2.5",
], "numpy version must be 2.2.5. Please install this version."

import robosuite

robosuite_version = [int(e) for e in robosuite.__version__.split(".")]
robosuite_check = True
if robosuite_version[0] < 1:
    robosuite_check = False
if robosuite_version[0] == 1 and robosuite_version[1] < 5:
    robosuite_check = False
if robosuite_version[0] == 1 and robosuite_version[1] == 5 and robosuite_version[2] < 2:
    robosuite_check = False
assert (
    robosuite_check
), "robosuite version must be >=1.5.2 Please install the correct version"

__version__ = "1.0.0"
__logo__ = """
      ;     /        ,--.
     ["]   ["]  ,<  |__**|
    /[_]\  [~]\/    |//  |
     ] [   OOO      /o|__|
"""
