"""Feature names, so callers don't have to write them as strings.

Each enum holds one kind of feature (the third part of its name, like `Status` in
`BSH.Common.Status.DoorState`). A member's name is the feature name without that part, in upper
snake case: `StatusKey.BSH_COMMON_DOOR_STATE`. This follows the keys in `aiohomeconnect`, the
library of Home Assistant's cloud Home Connect integration.

These are the names Home Connect Local and this library use, not every name an appliance can
report. Add a name here when something starts using it. Two washer options exist with and
without a dot before `Active` (`IDos1Active` and `IDos1.Active`); the dotted one ends in
`_DOTTED`. Features numbered per oven cavity or per favorite are only listed for the numbers
in use, so build those names with the appliance's group IDs instead.
"""

from enum import StrEnum


class StatusKey(StrEnum):
    """Names of status values the appliance reports."""

    BSH_COMMON_BACKEND_CONNECTED = "BSH.Common.Status.BackendConnected"
    BSH_COMMON_DOOR_STATE = "BSH.Common.Status.DoorState"
    BSH_COMMON_FLEX_START = "BSH.Common.Status.FlexStart"
    BSH_COMMON_INTERIOR_ILLUMINATION_ACTIVE = "BSH.Common.Status.InteriorIlluminationActive"
    BSH_COMMON_LOCAL_CONTROL_ACTIVE = "BSH.Common.Status.LocalControlActive"
    BSH_COMMON_OPERATION_STATE = "BSH.Common.Status.OperationState"
    BSH_COMMON_PROGRAM_ALL_COUNT_COMPLETED = "BSH.Common.Status.Program.All.Count.Completed"
    BSH_COMMON_PROGRAM_ALL_COUNT_STARTED = "BSH.Common.Status.Program.All.Count.Started"
    BSH_COMMON_PROGRAM_ALL_ENERGY_CONSUMED = "BSH.Common.Status.Program.All.Energy.Consumed"
    BSH_COMMON_PROGRAM_ALL_WATER_CONSUMED = "BSH.Common.Status.Program.All.Water.Consumed"
    BSH_COMMON_PROGRAM_LAST_ENERGY_CONSUMED = "BSH.Common.Status.Program.Last.Energy.Consumed"
    BSH_COMMON_PROGRAM_LAST_WATER_CONSUMED = "BSH.Common.Status.Program.Last.Water.Consumed"
    BSH_COMMON_PROGRAM_RUN_DETAIL_END_TRIGGER = "BSH.Common.Status.ProgramRunDetail.EndTrigger"
    BSH_COMMON_PROGRAM_SESSION_SUMMARY_LATEST = "BSH.Common.Status.ProgramSessionSummary.Latest"
    BSH_COMMON_REMOTE_CONTROL_ACTIVE = "BSH.Common.Status.RemoteControlActive"
    BSH_COMMON_REMOTE_CONTROL_START_ALLOWED = "BSH.Common.Status.RemoteControlStartAllowed"
    BSH_COMMON_STOP_WATCH_STATE = "BSH.Common.Status.StopWatchState"
    BSH_COMMON_STOP_WATCH_TIME = "BSH.Common.Status.StopWatchTime"
    CONSUMER_PRODUCTS_COFFEE_MAKER_BEVERAGE_COUNTDOWN_CALC_N_CLEAN = (
        "ConsumerProducts.CoffeeMaker.Status.BeverageCountdownCalcNClean"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_BEVERAGE_COUNTDOWN_CLEANING = (
        "ConsumerProducts.CoffeeMaker.Status.BeverageCountdownCleaning"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_BEVERAGE_COUNTDOWN_DESCALING = (
        "ConsumerProducts.CoffeeMaker.Status.BeverageCountdownDescaling"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_BEVERAGE_COUNTDOWN_WATERFILTER = (
        "ConsumerProducts.CoffeeMaker.Status.BeverageCountdownWaterfilter"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_BEVERAGE_COUNTER_COFFEE = (
        "ConsumerProducts.CoffeeMaker.Status.BeverageCounterCoffee"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_BEVERAGE_COUNTER_COFFEE_AND_MILK = (
        "ConsumerProducts.CoffeeMaker.Status.BeverageCounterCoffeeAndMilk"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_BEVERAGE_COUNTER_FROTHY_MILK = (
        "ConsumerProducts.CoffeeMaker.Status.BeverageCounterFrothyMilk"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_BEVERAGE_COUNTER_HOT_MILK = (
        "ConsumerProducts.CoffeeMaker.Status.BeverageCounterHotMilk"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_BEVERAGE_COUNTER_HOT_WATER = (
        "ConsumerProducts.CoffeeMaker.Status.BeverageCounterHotWater"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_BEVERAGE_COUNTER_HOT_WATER_CUPS = (
        "ConsumerProducts.CoffeeMaker.Status.BeverageCounterHotWaterCups"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_BEVERAGE_COUNTER_POWDER_COFFEE = (
        "ConsumerProducts.CoffeeMaker.Status.BeverageCounterPowderCoffee"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_BEVERAGE_COUNTER_RISTRETTO_ESPRESSO = (
        "ConsumerProducts.CoffeeMaker.Status.BeverageCounterRistrettoEspresso"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_PROCESS_PHASE = (
        "ConsumerProducts.CoffeeMaker.Status.ProcessPhase"
    )
    COOKING_HOB_ZONE = "Cooking.Hob.Status.Zone"
    COOKING_HOOD_CARBON_FILTER_SATURATION = "Cooking.Hood.Status.CarbonFilterSaturation"
    COOKING_HOOD_GREASE_FILTER_SATURATION = "Cooking.Hood.Status.GreaseFilterSaturation"
    COOKING_OVEN_CAVITY = "Cooking.Oven.Status.Cavity"
    COOKING_OVEN_CURRENT_CAVITY_TEMPERATURE = "Cooking.Oven.Status.CurrentCavityTemperature"
    COOKING_OVEN_CURRENT_MEATPROBE_TEMPERATURE = "Cooking.Oven.Status.CurrentMeatprobeTemperature"
    COOKING_OVEN_CURRENT_MEATPROBE_TEMPERATURE_FAHRENHEIT = (
        "Cooking.Oven.Status.CurrentMeatprobeTemperatureFahrenheit"
    )
    COOKING_OVEN_MEATPROBE_PLUGGED = "Cooking.Oven.Status.MeatprobePlugged"
    COOKING_OVEN_WATER_TANK_EMPTY = "Cooking.Oven.Status.WaterTankEmpty"
    COOKING_OVEN_WATER_TANK_UNPLUGGED = "Cooking.Oven.Status.WaterTankUnplugged"
    DISHCARE_DISHWASHER_ECO_DRY_ACTIVE = "Dishcare.Dishwasher.Status.EcoDryActive"
    DISHCARE_DISHWASHER_MACHINE_CARE_REMINDER_REMAINING_PROGRAM_RUNS = (
        "Dishcare.Dishwasher.Status.MachineCareReminder.RemainingProgramRuns"
    )
    DISHCARE_DISHWASHER_PROGRAM_PHASE = "Dishcare.Dishwasher.Status.ProgramPhase"
    LAUNDRY_CARE_COMMON_LAUNDRY_RELOAD = "LaundryCare.Common.Status.Laundry.Reload"
    LAUNDRY_CARE_DRYER_REFRESHER_FILL_LEVEL = "LaundryCare.Dryer.Status.RefresherFillLevel"
    LAUNDRY_CARE_WASHER_DETERGENT_ALL_CONSUMED = "LaundryCare.Washer.Status.Detergent.All.Consumed"
    LAUNDRY_CARE_WASHER_I_DOS_1_FILL_LEVEL = "LaundryCare.Washer.Status.IDos1FillLevel"
    LAUNDRY_CARE_WASHER_I_DOS_2_FILL_LEVEL = "LaundryCare.Washer.Status.IDos2FillLevel"
    LAUNDRY_CARE_WASHER_PROCESSING_DATA_LAUNDRY_LOAD = (
        "LaundryCare.Washer.Status.ProcessingData.LaundryLoad"
    )
    LAUNDRY_CARE_WASHER_SOFTENER_ALL_CONSUMED = "LaundryCare.Washer.Status.Softener.All.Consumed"
    REFRIGERATION_COMMON_DISPENSER_ICE_HOPPER_FULL = (
        "Refrigeration.Common.Status.Dispenser.IceHopperFull"
    )
    REFRIGERATION_COMMON_DISPENSER_WATER_FILTER_SATURATION = (
        "Refrigeration.Common.Status.Dispenser.WaterFilterSaturation"
    )
    REFRIGERATION_COMMON_DOOR_CHILLER_COMMON = "Refrigeration.Common.Status.Door.ChillerCommon"
    REFRIGERATION_COMMON_DOOR_FREEZER = "Refrigeration.Common.Status.Door.Freezer"
    REFRIGERATION_COMMON_DOOR_REFRIGERATOR = "Refrigeration.Common.Status.Door.Refrigerator"
    REFRIGERATION_COMMON_FREEZER_DEFROST = "Refrigeration.Common.Status.Freezer.Defrost"
    REFRIGERATION_COMMON_FREEZER_MEMORY_TEMPERATURE = (
        "Refrigeration.Common.Status.Freezer.MemoryTemperature"
    )
    REFRIGERATION_COMMON_TEMPERATURE_AMBIENT = "Refrigeration.Common.Status.TemperatureAmbient"
    REFRIGERATION_FRIDGE_FREEZER_CHILLER_COMMON = "Refrigeration.FridgeFreezer.Status.ChillerCommon"
    REFRIGERATION_FRIDGE_FREEZER_DEFROST_FREEZER = (
        "Refrigeration.FridgeFreezer.Status.DefrostFreezer"
    )
    REFRIGERATION_FRIDGE_FREEZER_DOOR_FREEZER = "Refrigeration.FridgeFreezer.Status.DoorFreezer"
    REFRIGERATION_FRIDGE_FREEZER_DOOR_REFRIGERATOR = (
        "Refrigeration.FridgeFreezer.Status.DoorRefrigerator"
    )
    REFRIGERATION_FRIDGE_FREEZER_TEMPERATURE_AMBIENT = (
        "Refrigeration.FridgeFreezer.Status.TemperatureAmbient"
    )


class SettingKey(StrEnum):
    """Names of settings."""

    BSH_COMMON_ALARM_CLOCK = "BSH.Common.Setting.AlarmClock"
    BSH_COMMON_ALLOW_BACKEND_CONNECTION = "BSH.Common.Setting.AllowBackendConnection"
    BSH_COMMON_ALLOW_CONSUMER_INSIGHTS = "BSH.Common.Setting.AllowConsumerInsights"
    BSH_COMMON_AMBIENT_LIGHT_BRIGHTNESS = "BSH.Common.Setting.AmbientLightBrightness"
    BSH_COMMON_AMBIENT_LIGHT_COLOR = "BSH.Common.Setting.AmbientLightColor"
    BSH_COMMON_AMBIENT_LIGHT_CUSTOM_COLOR = "BSH.Common.Setting.AmbientLightCustomColor"
    BSH_COMMON_AMBIENT_LIGHT_ENABLED = "BSH.Common.Setting.AmbientLightEnabled"
    BSH_COMMON_APPLIANCE_DATE_TIME = "BSH.Common.Setting.ApplianceDateTime"
    BSH_COMMON_CHILD_LOCK = "BSH.Common.Setting.ChildLock"
    BSH_COMMON_DATE_FORMAT = "BSH.Common.Setting.DateFormat"
    BSH_COMMON_LANGUAGE = "BSH.Common.Setting.Language"
    BSH_COMMON_LOCAL_TIME = "BSH.Common.Setting.LocalTime"
    BSH_COMMON_POWER_STATE = "BSH.Common.Setting.PowerState"
    BSH_COMMON_REMOTE_CONTROL_LEVEL = "BSH.Common.Setting.RemoteControlLevel"
    BSH_COMMON_SYNCHRONIZE_WITH_TIME_SERVER = "BSH.Common.Setting.SynchronizeWithTimeServer"
    BSH_COMMON_TEMPERATURE_UNIT = "BSH.Common.Setting.TemperatureUnit"
    BSH_COMMON_TIME_FORMAT = "BSH.Common.Setting.TimeFormat"
    BSH_COMMON_WEIGHT_UNIT = "BSH.Common.Setting.WeightUnit"
    CONSUMER_PRODUCTS_COFFEE_MAKER_BRIGHTNESS_DISPLAY = (
        "ConsumerProducts.CoffeeMaker.Setting.BrightnessDisplay"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_COFFEE_MILK_ORDER = (
        "ConsumerProducts.CoffeeMaker.Setting.CoffeeMilkOrder"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_CUP_WARMER = "ConsumerProducts.CoffeeMaker.Setting.CupWarmer"
    CONSUMER_PRODUCTS_COFFEE_MAKER_DEFAULT_BEAN_CONTAINER_SELECTION = (
        "ConsumerProducts.CoffeeMaker.Setting.DefaultBeanContainerSelection"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_LEAVE_PROFILES_AUTOMATICALLY = (
        "ConsumerProducts.CoffeeMaker.Setting.LeaveProfilesAutomatically"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_MACCHIATO_PAUSE = (
        "ConsumerProducts.CoffeeMaker.Setting.MacchiatoPause"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_REMIND_FOR_MILK_AFTER = (
        "ConsumerProducts.CoffeeMaker.Setting.RemindForMilkAfter"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_SWITCH_OFF_AFTER = (
        "ConsumerProducts.CoffeeMaker.Setting.SwitchOffAfter"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_USER_MODE = "ConsumerProducts.CoffeeMaker.Setting.UserMode"
    CONSUMER_PRODUCTS_COFFEE_MAKER_WATER_HARDNESS = (
        "ConsumerProducts.CoffeeMaker.Setting.WaterHardness"
    )
    COOKING_COMMON_BUTTON_TONE_TYPE = "Cooking.Common.Setting.ButtonToneType"
    COOKING_COMMON_BUTTON_TONE_VOLUME = "Cooking.Common.Setting.ButtonToneVolume"
    COOKING_COMMON_DISPLAY_BRIGHTNESS = "Cooking.Common.Setting.DisplayBrightness"
    COOKING_COMMON_LIGHTING = "Cooking.Common.Setting.Lighting"
    COOKING_COMMON_LIGHTING_BRIGHTNESS = "Cooking.Common.Setting.LightingBrightness"
    COOKING_COMMON_SIGNAL_VOLUME = "Cooking.Common.Setting.SignalVolume"
    COOKING_HOB_AUTOMATIC_KEY_LOCK = "Cooking.Hob.Setting.AutomaticKeyLock"
    COOKING_HOB_AUTOMATIC_TIMER = "Cooking.Hob.Setting.AutomaticTimer"
    COOKING_HOB_BRIDGE_ZONE_MODE = "Cooking.Hob.Setting.BridgeZoneMode"
    COOKING_HOB_BUZZER_BEEP_LEVEL = "Cooking.Hob.Setting.BuzzerBeepLevel"
    COOKING_HOB_END_TIMER_SIGNALDURATION = "Cooking.Hob.Setting.EndTimerSignalduration"
    COOKING_HOB_ENERGY_CONSUMPTION_INDICATION = "Cooking.Hob.Setting.EnergyConsumptionIndication"
    COOKING_HOB_HOOD_AFTER_RUN = "Cooking.Hob.Setting.HoodAfterRun"
    COOKING_HOB_HOOD_AUTOMATIC_LIGHT_OFF = "Cooking.Hob.Setting.HoodAutomaticLightOff"
    COOKING_HOB_HOOD_AUTOMATIC_LIGHT_ON = "Cooking.Hob.Setting.HoodAutomaticLightOn"
    COOKING_HOB_HOOD_AUTOMATIC_START = "Cooking.Hob.Setting.HoodAutomaticStart"
    COOKING_HOB_POWER_MANAGEMENT = "Cooking.Hob.Setting.PowerManagement"
    COOKING_HOB_VENTILATION = "Cooking.Hob.Setting.Ventilation"
    COOKING_HOOD_BOOST_TIME = "Cooking.Hood.Setting.BoostTime"
    COOKING_HOOD_CARBON_FILTER_TYPE = "Cooking.Hood.Setting.CarbonFilterType"
    COOKING_HOOD_COLOR_TEMPERATURE = "Cooking.Hood.Setting.ColorTemperature"
    COOKING_HOOD_COLOR_TEMPERATURE_PERCENT = "Cooking.Hood.Setting.ColorTemperaturePercent"
    COOKING_HOOD_DELAYED_SHUT_OFF_STAGE = "Cooking.Hood.Setting.DelayedShutOffStage"
    COOKING_HOOD_DELAYED_SHUT_OFF_TIME = "Cooking.Hood.Setting.DelayedShutOffTime"
    COOKING_HOOD_INTERVAL_STAGE = "Cooking.Hood.Setting.IntervalStage"
    COOKING_HOOD_INTERVAL_TIME_OFF = "Cooking.Hood.Setting.IntervalTimeOff"
    COOKING_HOOD_INTERVAL_TIME_ON = "Cooking.Hood.Setting.IntervalTimeOn"
    COOKING_HOOD_LIGHTING_BRIGHTNESS = "Cooking.Hood.Setting.LightingBrightness"
    COOKING_HOOD_NOISE_REDUCTION = "Cooking.Hood.Setting.NoiseReduction"
    COOKING_HOOD_SENSOR_SENSITIVITY = "Cooking.Hood.Setting.SensorSensitivity"
    COOKING_HOOD_WORKING_LIGHT_SHUTDOWN_SETTING = "Cooking.Hood.Setting.WorkingLightShutdownSetting"
    COOKING_HOOD_WORKING_LIGHT_STARTUP_SETTING = "Cooking.Hood.Setting.WorkingLightStartupSetting"
    COOKING_OVEN_BUTTON_TONES = "Cooking.Oven.Setting.ButtonTones"
    COOKING_OVEN_CAVITY = "Cooking.Oven.Setting.Cavity"
    COOKING_OVEN_CLOCK_DISPLAY = "Cooking.Oven.Setting.ClockDisplay"
    COOKING_OVEN_CONFIGURE_CHILD_LOCK = "Cooking.Oven.Setting.ConfigureChildLock"
    COOKING_OVEN_CONVECTION_CONVERSION = "Cooking.Oven.Setting.ConvectionConversion"
    COOKING_OVEN_COOLING_FAN_RUN_ON_TIME = "Cooking.Oven.Setting.CoolingFanRunOnTime"
    COOKING_OVEN_DISPLAY_BRAND_LOGO = "Cooking.Oven.Setting.DisplayBrandLogo"
    COOKING_OVEN_DISPLAY_BRIGHTNESS = "Cooking.Oven.Setting.DisplayBrightness"
    COOKING_OVEN_DISPLAY_STANDBY_DIMMED = "Cooking.Oven.Setting.DisplayStandbyDimmed"
    COOKING_OVEN_DOOR_OPENER_DELAY = "Cooking.Oven.Setting.DoorOpenerDelay"
    COOKING_OVEN_FAST_PRE_HEAT = "Cooking.Oven.Setting.FastPreHeat"
    COOKING_OVEN_HEATING_SIGNAL = "Cooking.Oven.Setting.HeatingSignal"
    COOKING_OVEN_IDLE_SCREEN = "Cooking.Oven.Setting.IdleScreen"
    COOKING_OVEN_LIGHT_CAVITY_001_BRIGHTNESS = "Cooking.Oven.Setting.Light.Cavity.001.Brightness"
    COOKING_OVEN_LIGHT_CAVITY_001_POWER = "Cooking.Oven.Setting.Light.Cavity.001.Power"
    COOKING_OVEN_NIGHT_DIMOUT = "Cooking.Oven.Setting.NightDimout"
    COOKING_OVEN_OVEN_LIGHT_DURING_OPERATION = "Cooking.Oven.Setting.OvenLightDuringOperation"
    COOKING_OVEN_SABBATH_MODE = "Cooking.Oven.Setting.SabbathMode"
    COOKING_OVEN_SIGNAL_DURATION = "Cooking.Oven.Setting.SignalDuration"
    COOKING_OVEN_SOUND_VOLUME = "Cooking.Oven.Setting.SoundVolume"
    COOKING_OVEN_STANDBY_DISPLAY = "Cooking.Oven.Setting.StandbyDisplay"
    COOKING_OVEN_SWITCH_ON_DELAY = "Cooking.Oven.Setting.SwitchOnDelay"
    COOKING_OVEN_TELOSCOPIC_SLIDE_OUT_REFITED = "Cooking.Oven.Setting.TeloscopicSlideOutRefited"
    COOKING_OVEN_TOUCHKEY_COLOR = "Cooking.Oven.Setting.TouchkeyColor"
    DISHCARE_DISHWASHER_AUTO_POWER_OFF = "Dishcare.Dishwasher.Setting.AutoPowerOff"
    DISHCARE_DISHWASHER_DRYING_ASSISTANT_ALL_PROGRAMS = (
        "Dishcare.Dishwasher.Setting.DryingAssistantAllPrograms"
    )
    DISHCARE_DISHWASHER_ECO_AS_DEFAULT = "Dishcare.Dishwasher.Setting.EcoAsDefault"
    DISHCARE_DISHWASHER_EXTRA_DRY = "Dishcare.Dishwasher.Setting.ExtraDry"
    DISHCARE_DISHWASHER_FLEX_SPRAY_CUSTOM_BACK_LEFT = (
        "Dishcare.Dishwasher.Setting.FlexSpray.Custom.BackLeft"
    )
    DISHCARE_DISHWASHER_FLEX_SPRAY_CUSTOM_BACK_RIGHT = (
        "Dishcare.Dishwasher.Setting.FlexSpray.Custom.BackRight"
    )
    DISHCARE_DISHWASHER_FLEX_SPRAY_CUSTOM_FRONT_LEFT = (
        "Dishcare.Dishwasher.Setting.FlexSpray.Custom.FrontLeft"
    )
    DISHCARE_DISHWASHER_FLEX_SPRAY_CUSTOM_FRONT_RIGHT = (
        "Dishcare.Dishwasher.Setting.FlexSpray.Custom.FrontRight"
    )
    DISHCARE_DISHWASHER_HOT_WATER = "Dishcare.Dishwasher.Setting.HotWater"
    DISHCARE_DISHWASHER_INFO_LIGHT = "Dishcare.Dishwasher.Setting.InfoLight"
    DISHCARE_DISHWASHER_RINSE_AID = "Dishcare.Dishwasher.Setting.RinseAid"
    DISHCARE_DISHWASHER_SENSITIVITY_TURBIDITY = "Dishcare.Dishwasher.Setting.SensitivityTurbidity"
    DISHCARE_DISHWASHER_SOUND_LEVEL_KEY = "Dishcare.Dishwasher.Setting.SoundLevelKey"
    DISHCARE_DISHWASHER_SOUND_LEVEL_SIGNAL = "Dishcare.Dishwasher.Setting.SoundLevelSignal"
    DISHCARE_DISHWASHER_SPEED_ON_DEMAND = "Dishcare.Dishwasher.Setting.SpeedOnDemand"
    DISHCARE_DISHWASHER_TIME_LIGHT = "Dishcare.Dishwasher.Setting.TimeLight"
    DISHCARE_DISHWASHER_WATER_HARDNESS = "Dishcare.Dishwasher.Setting.WaterHardness"
    LAUNDRY_CARE_COMMON_AUTO_POWER_OFF = "LaundryCare.Common.Setting.AutoPowerOff"
    LAUNDRY_CARE_COMMON_BRIGHTNESS = "LaundryCare.Common.Setting.Brightness"
    LAUNDRY_CARE_COMMON_BRIGHTNESS_LEVEL = "LaundryCare.Common.Setting.BrightnessLevel"
    LAUNDRY_CARE_COMMON_DOOR_LIGHT_RING_ACTIVE = "LaundryCare.Common.Setting.DoorLightRing.Active"
    LAUNDRY_CARE_COMMON_DOOR_LIGHT_RING_ACTIVE_MODE = (
        "LaundryCare.Common.Setting.DoorLightRing.ActiveMode"
    )
    LAUNDRY_CARE_COMMON_DOOR_LIGHT_RING_BRIGHTNESS = (
        "LaundryCare.Common.Setting.DoorLightRing.Brightness"
    )
    LAUNDRY_CARE_COMMON_DOOR_LIGHT_RING_BRIGHTNESS_LEVEL = (
        "LaundryCare.Common.Setting.DoorLightRing.BrightnessLevel"
    )
    LAUNDRY_CARE_COMMON_DRUM_LIGHT_ACTIVE = "LaundryCare.Common.Setting.DrumLight.Active"
    LAUNDRY_CARE_COMMON_END_SIGNAL = "LaundryCare.Common.Setting.EndSignal"
    LAUNDRY_CARE_COMMON_END_SIGNAL_VOLUME = "LaundryCare.Common.Setting.EndSignalVolume"
    LAUNDRY_CARE_COMMON_KEY_SIGNAL_VOLUME = "LaundryCare.Common.Setting.KeySignalVolume"
    LAUNDRY_CARE_COMMON_SOUND_MUTE = "LaundryCare.Common.Setting.Sound.Mute"
    LAUNDRY_CARE_COMMON_SOUND_VOLUME = "LaundryCare.Common.Setting.Sound.Volume"
    LAUNDRY_CARE_COMMON_SUPPLY_POWER_POWER_RATING = (
        "LaundryCare.Common.Setting.SupplyPower.PowerRating"
    )
    LAUNDRY_CARE_COMMON_TIME_LIGHT_ACTIVE = "LaundryCare.Common.Setting.TimeLight.Active"
    LAUNDRY_CARE_COMMON_WRINKLE_GUARD = "LaundryCare.Common.Setting.WrinkleGuard"
    LAUNDRY_CARE_DRYER_CUPBOARD_DRY_FINE_ADJUST = "LaundryCare.Dryer.Setting.CupboardDryFineAdjust"
    LAUNDRY_CARE_DRYER_CUPBOARD_DRY_PLUS_FINE_ADJUST = (
        "LaundryCare.Dryer.Setting.CupboardDryPlusFineAdjust"
    )
    LAUNDRY_CARE_DRYER_IRON_DRY_FINE_ADJUST = "LaundryCare.Dryer.Setting.IronDryFineAdjust"
    LAUNDRY_CARE_DRYER_SPIN_SPEED_BEFORE_DRYING = "LaundryCare.Dryer.Setting.SpinSpeedBeforeDrying"
    LAUNDRY_CARE_WASHER_I_DOS_1_BASE_LEVEL = "LaundryCare.Washer.Setting.IDos1BaseLevel"
    LAUNDRY_CARE_WASHER_I_DOS_2_BASE_LEVEL = "LaundryCare.Washer.Setting.IDos2BaseLevel"
    LAUNDRY_CARE_WASHER_I_DOS_2_CONTENT = "LaundryCare.Washer.Setting.IDos2Content"
    REFRIGERATION_COMMON_CHILLER_COMMON_PRESET = "Refrigeration.Common.Setting.ChillerCommon.Preset"
    REFRIGERATION_COMMON_CHILLER_COMMON_SETPOINT_TEMPERATURE = (
        "Refrigeration.Common.Setting.ChillerCommon.SetpointTemperature"
    )
    REFRIGERATION_COMMON_CHILLER_COMMON_SETPOINT_TEMPERATURE_FAHRENHEIT = (
        "Refrigeration.Common.Setting.ChillerCommon.SetpointTemperatureFahrenheit"
    )
    REFRIGERATION_COMMON_CHILLER_LEFT_HUMIDITY = "Refrigeration.Common.Setting.ChillerLeft.Humidity"
    REFRIGERATION_COMMON_CHILLER_RIGHT_HUMIDITY = (
        "Refrigeration.Common.Setting.ChillerRight.Humidity"
    )
    REFRIGERATION_COMMON_DISPENSER_ENABLED = "Refrigeration.Common.Setting.Dispenser.Enabled"
    REFRIGERATION_COMMON_DISPENSER_PARTY_MODE = "Refrigeration.Common.Setting.Dispenser.PartyMode"
    REFRIGERATION_COMMON_DOOR_ASSISTANT_FORCE_FREEZER = (
        "Refrigeration.Common.Setting.Door.AssistantForceFreezer"
    )
    REFRIGERATION_COMMON_DOOR_ASSISTANT_FORCE_FRIDGE = (
        "Refrigeration.Common.Setting.Door.AssistantForceFridge"
    )
    REFRIGERATION_COMMON_DOOR_ASSISTANT_FREEZER = (
        "Refrigeration.Common.Setting.Door.AssistantFreezer"
    )
    REFRIGERATION_COMMON_DOOR_ASSISTANT_FRIDGE = "Refrigeration.Common.Setting.Door.AssistantFridge"
    REFRIGERATION_COMMON_DOOR_ASSISTANT_TIMEOUT_FREEZER = (
        "Refrigeration.Common.Setting.Door.AssistantTimeoutFreezer"
    )
    REFRIGERATION_COMMON_DOOR_ASSISTANT_TIMEOUT_FRIDGE = (
        "Refrigeration.Common.Setting.Door.AssistantTimeoutFridge"
    )
    REFRIGERATION_COMMON_DOOR_ASSISTANT_TRIGGER_FREEZER = (
        "Refrigeration.Common.Setting.Door.AssistantTriggerFreezer"
    )
    REFRIGERATION_COMMON_DOOR_ASSISTANT_TRIGGER_FRIDGE = (
        "Refrigeration.Common.Setting.Door.AssistantTriggerFridge"
    )
    REFRIGERATION_COMMON_ECO_MODE = "Refrigeration.Common.Setting.EcoMode"
    REFRIGERATION_COMMON_FREEZER_SETPOINT_TEMPERATURE = (
        "Refrigeration.Common.Setting.Freezer.SetpointTemperature"
    )
    REFRIGERATION_COMMON_FREEZER_SETPOINT_TEMPERATURE_FAHRENHEIT = (
        "Refrigeration.Common.Setting.Freezer.SetpointTemperatureFahrenheit"
    )
    REFRIGERATION_COMMON_FREEZER_SUPER_MODE = "Refrigeration.Common.Setting.Freezer.SuperMode"
    REFRIGERATION_COMMON_FRESH_MODE = "Refrigeration.Common.Setting.FreshMode"
    REFRIGERATION_COMMON_LIGHT_INTERNAL_BRIGHTNESS = (
        "Refrigeration.Common.Setting.Light.Internal.Brightness"
    )
    REFRIGERATION_COMMON_LIGHT_INTERNAL_ENABLE_THEATER_MODE = (
        "Refrigeration.Common.Setting.Light.Internal.EnableTheaterMode"
    )
    REFRIGERATION_COMMON_LIGHT_INTERNAL_POWER = "Refrigeration.Common.Setting.Light.Internal.Power"
    REFRIGERATION_COMMON_LIGHT_LOGO_POWER = "Refrigeration.Common.Setting.Light.Logo.Power"
    REFRIGERATION_COMMON_REFRIGERATOR_SETPOINT_TEMPERATURE = (
        "Refrigeration.Common.Setting.Refrigerator.SetpointTemperature"
    )
    REFRIGERATION_COMMON_REFRIGERATOR_SETPOINT_TEMPERATURE_FAHRENHEIT = (
        "Refrigeration.Common.Setting.Refrigerator.SetpointTemperatureFahrenheit"
    )
    REFRIGERATION_COMMON_REFRIGERATOR_SUPER_MODE = (
        "Refrigeration.Common.Setting.Refrigerator.SuperMode"
    )
    REFRIGERATION_COMMON_SABBATH_MODE = "Refrigeration.Common.Setting.SabbathMode"
    REFRIGERATION_COMMON_SABBATH_MODE_DURATION = "Refrigeration.Common.Setting.SabbathModeDuration"
    REFRIGERATION_COMMON_VACATION_MODE = "Refrigeration.Common.Setting.VacationMode"
    REFRIGERATION_FRIDGE_FREEZER_ECO_MODE = "Refrigeration.FridgeFreezer.Setting.EcoMode"
    REFRIGERATION_FRIDGE_FREEZER_FRESH_MODE = "Refrigeration.FridgeFreezer.Setting.FreshMode"
    REFRIGERATION_FRIDGE_FREEZER_SABBATH_MODE = "Refrigeration.FridgeFreezer.Setting.SabbathMode"
    REFRIGERATION_FRIDGE_FREEZER_SETPOINT_TEMPERATURE_FREEZER = (
        "Refrigeration.FridgeFreezer.Setting.SetpointTemperatureFreezer"
    )
    REFRIGERATION_FRIDGE_FREEZER_SETPOINT_TEMPERATURE_REFRIGERATOR = (
        "Refrigeration.FridgeFreezer.Setting.SetpointTemperatureRefrigerator"
    )
    REFRIGERATION_FRIDGE_FREEZER_SUPER_MODE_FREEZER = (
        "Refrigeration.FridgeFreezer.Setting.SuperModeFreezer"
    )
    REFRIGERATION_FRIDGE_FREEZER_SUPER_MODE_REFRIGERATOR = (
        "Refrigeration.FridgeFreezer.Setting.SuperModeRefrigerator"
    )
    REFRIGERATION_FRIDGE_FREEZER_VACATION_MODE = "Refrigeration.FridgeFreezer.Setting.VacationMode"


class EventKey(StrEnum):
    """Names of events."""

    BSH_COMMON_ALARM_CLOCK_ELAPSED = "BSH.Common.Event.AlarmClockElapsed"
    BSH_COMMON_AQUA_STOP_OCCURED = "BSH.Common.Event.AquaStopOccured"
    BSH_COMMON_CONFIRM_PERMANENT_REMOTE_START = "BSH.Common.Event.ConfirmPermanentRemoteStart"
    BSH_COMMON_CUSTOMER_SERVICE_REQUEST = "BSH.Common.Event.CustomerServiceRequest"
    BSH_COMMON_FAVORITE_001_EXTERNAL_TRIGGER = "BSH.Common.Event.Favorite.001.ExternalTrigger"
    BSH_COMMON_FAVORITE_002_EXTERNAL_TRIGGER = "BSH.Common.Event.Favorite.002.ExternalTrigger"
    BSH_COMMON_LOW_WATER_PRESSURE = "BSH.Common.Event.LowWaterPressure"
    BSH_COMMON_PROGRAM_ABORTED = "BSH.Common.Event.ProgramAborted"
    BSH_COMMON_PROGRAM_FINISHED = "BSH.Common.Event.ProgramFinished"
    BSH_COMMON_SOFTWARE_DOWNLOAD_AVAILABLE = "BSH.Common.Event.SoftwareDownloadAvailable"
    BSH_COMMON_SOFTWARE_UPDATE_AVAILABLE = "BSH.Common.Event.SoftwareUpdateAvailable"
    BSH_COMMON_SOFTWARE_UPDATE_SUCCESSFUL = "BSH.Common.Event.SoftwareUpdateSuccessful"
    CONSUMER_PRODUCTS_COFFEE_MAKER_BEAN_CONTAINER_EMPTY = (
        "ConsumerProducts.CoffeeMaker.Event.BeanContainerEmpty"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_BREWING_UNIT_IS_MISSING = (
        "ConsumerProducts.CoffeeMaker.Event.BrewingUnitIsMissing"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_CLEAN_BREWING_UNIT = (
        "ConsumerProducts.CoffeeMaker.Event.CleanBrewingUnit"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_CLEAN_FILL_WATER_TANK = (
        "ConsumerProducts.CoffeeMaker.Event.CleanFillWaterTank"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_CLEAN_MILK_TANK = (
        "ConsumerProducts.CoffeeMaker.Event.CleanMilkTank"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_CLOSE_DOOR = "ConsumerProducts.CoffeeMaker.Event.CloseDoor"
    CONSUMER_PRODUCTS_COFFEE_MAKER_COFFEE_OUTLET_MISSING = (
        "ConsumerProducts.CoffeeMaker.Event.CoffeeOutletMissing"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_DEVICE_DESCALING_BLOCKAGE = (
        "ConsumerProducts.CoffeeMaker.Event.DeviceDescalingBlockage"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_DEVICE_DESCALING_OVERDUE = (
        "ConsumerProducts.CoffeeMaker.Event.DeviceDescalingOverdue"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_DEVICE_SHOULD_BE_CALC_N_CLEANED = (
        "ConsumerProducts.CoffeeMaker.Event.DeviceShouldBeCalcNCleaned"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_DEVICE_SHOULD_BE_CLEANED = (
        "ConsumerProducts.CoffeeMaker.Event.DeviceShouldBeCleaned"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_DEVICE_SHOULD_BE_DESCALED = (
        "ConsumerProducts.CoffeeMaker.Event.DeviceShouldBeDescaled"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_DRIP_TRAY_FULL = (
        "ConsumerProducts.CoffeeMaker.Event.DripTrayFull"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_DRIP_TRAY_NOT_INSERTED = (
        "ConsumerProducts.CoffeeMaker.Event.DripTrayNotInserted"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_EMPTY_DRIP_TRAY = (
        "ConsumerProducts.CoffeeMaker.Event.EmptyDripTray"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_EMPTY_DRIP_TRAY_REMOVE_CONTAINER = (
        "ConsumerProducts.CoffeeMaker.Event.EmptyDripTrayRemoveContainer"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_EMPTY_MILK_TANK = (
        "ConsumerProducts.CoffeeMaker.Event.EmptyMilkTank"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_FILL_DESCALER = "ConsumerProducts.CoffeeMaker.Event.FillDescaler"
    CONSUMER_PRODUCTS_COFFEE_MAKER_MILK_REMINDER = "ConsumerProducts.CoffeeMaker.Event.MilkReminder"
    CONSUMER_PRODUCTS_COFFEE_MAKER_PLACE_CONTAINER_UNDER_OUTLET = (
        "ConsumerProducts.CoffeeMaker.Event.PlaceContainerUnderOutlet"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_PLACE_EMPTY_GLASS_UNDER_OUTLET = (
        "ConsumerProducts.CoffeeMaker.Event.PlaceEmptyGlassUnderOutlet"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_REMOVE_CONTAINER_UNDER_OUTLET = (
        "ConsumerProducts.CoffeeMaker.Event.RemoveContainerUnderOutlet"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_SERVICE_PROGRAM_FINISHED = (
        "ConsumerProducts.CoffeeMaker.Event.ServiceProgramFinished"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_THROW_CLEANING_DISC_IN_THE_DRAWER = (
        "ConsumerProducts.CoffeeMaker.Event.ThrowCleaningDiscInTheDrawer"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_WATER_FILTER_SHOULD_BE_CHANGED = (
        "ConsumerProducts.CoffeeMaker.Event.WaterFilterShouldBeChanged"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_WATER_TANK_EMPTY = (
        "ConsumerProducts.CoffeeMaker.Event.WaterTankEmpty"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_WATER_TANK_NEARLY_EMPTY = (
        "ConsumerProducts.CoffeeMaker.Event.WaterTankNearlyEmpty"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_WATER_TANK_NOT_INSERTED = (
        "ConsumerProducts.CoffeeMaker.Event.WaterTankNotInserted"
    )
    COOKING_COMMON_APPLIANCE_MODULE_ERROR = "Cooking.Common.Event.ApplianceModuleError"
    COOKING_COMMON_PREHEAT_FINISHED = "Cooking.Common.Event.PreheatFinished"
    COOKING_OVEN_CAVITY = "Cooking.Oven.Event.Cavity"
    COOKING_OVEN_CAVITY_HEATUP = "Cooking.Oven.Event.CavityHeatup"
    COOKING_OVEN_CAVITY_TEMPERATURE_TOO_HIGH = "Cooking.Oven.Event.CavityTemperatureTooHigh"
    COOKING_OVEN_CLEANING_REQUEST = "Cooking.Oven.Event.CleaningRequest"
    COOKING_OVEN_DESCALING_REQUEST = "Cooking.Oven.Event.DescalingRequest"
    COOKING_OVEN_EMPTY_WATER_CONTAINER = "Cooking.Oven.Event.EmptyWaterContainer"
    COOKING_OVEN_FORCE_FLUSHING = "Cooking.Oven.Event.ForceFlushing"
    COOKING_OVEN_OPERATING_TIME_LIMIT_REACHED = "Cooking.Oven.Event.OperatingTimeLimitReached"
    COOKING_OVEN_OVEN_LOCK_WHILE_COOLING_DOWN = "Cooking.Oven.Event.OvenLockWhileCoolingDown"
    COOKING_OVEN_USER_INTERACTION_REQUIRED = "Cooking.Oven.Event.UserInteractionRequired"
    COOKING_OVEN_WATER_SUPPLY_CLOSED = "Cooking.Oven.Event.WaterSupplyClosed"
    DISHCARE_DISHWASHER_CHECK_FILTER_SYSTEM = "Dishcare.Dishwasher.Event.CheckFilterSystem"
    DISHCARE_DISHWASHER_DRAIN_PUMP_BLOCKED = "Dishcare.Dishwasher.Event.DrainPumpBlocked"
    DISHCARE_DISHWASHER_DRAINING_NOT_POSSIBLE = "Dishcare.Dishwasher.Event.DrainingNotPossible"
    DISHCARE_DISHWASHER_FLEX_SPRAY_ERROR_BLOCKED = (
        "Dishcare.Dishwasher.Event.FlexSpray.Error.Blocked"
    )
    DISHCARE_DISHWASHER_FLEX_SPRAY_ERROR_GENERAL = (
        "Dishcare.Dishwasher.Event.FlexSpray.Error.General"
    )
    DISHCARE_DISHWASHER_FLEX_SPRAY_ERROR_SPRAY_ARM_NOT_MOUNTED = (
        "Dishcare.Dishwasher.Event.FlexSpray.Error.SprayArmNotMounted"
    )
    DISHCARE_DISHWASHER_LOW_VOLTAGE = "Dishcare.Dishwasher.Event.LowVoltage"
    DISHCARE_DISHWASHER_MACHINE_CARE_AND_FILTER_CLEANING_REMINDER = (
        "Dishcare.Dishwasher.Event.MachineCareAndFilterCleaningReminder"
    )
    DISHCARE_DISHWASHER_MACHINE_CARE_REMINDER = "Dishcare.Dishwasher.Event.MachineCareReminder"
    DISHCARE_DISHWASHER_RINSE_AID_LACK = "Dishcare.Dishwasher.Event.RinseAidLack"
    DISHCARE_DISHWASHER_RINSE_AID_NEARLY_EMPTY = "Dishcare.Dishwasher.Event.RinseAidNearlyEmpty"
    DISHCARE_DISHWASHER_SALT_LACK = "Dishcare.Dishwasher.Event.SaltLack"
    DISHCARE_DISHWASHER_SALT_NEARLY_EMPTY = "Dishcare.Dishwasher.Event.SaltNearlyEmpty"
    DISHCARE_DISHWASHER_SMART_FILTER_CLEANING_REMINDER = (
        "Dishcare.Dishwasher.Event.SmartFilterCleaningReminder"
    )
    DISHCARE_DISHWASHER_WATERHEATER_CALCIFIED = "Dishcare.Dishwasher.Event.WaterheaterCalcified"
    LAUNDRY_CARE_COMMON_DOOR_LOCK_WATER_LEVEL_TOO_HIGH = (
        "LaundryCare.Common.Event.DoorLock.WaterLevelTooHigh"
    )
    LAUNDRY_CARE_COMMON_DOOR_NOT_LOCKABLE = "LaundryCare.Common.Event.DoorNotLockable"
    LAUNDRY_CARE_COMMON_DOOR_NOT_UNLOCKABLE = "LaundryCare.Common.Event.DoorNotUnlockable"
    LAUNDRY_CARE_COMMON_FATAL_ERROR_OCCURED = "LaundryCare.Common.Event.FatalErrorOccured"
    LAUNDRY_CARE_COMMON_FOAM_DETECTION = "LaundryCare.Common.Event.FoamDetection"
    LAUNDRY_CARE_COMMON_SUPPLY_POWER_SUPPLY_VOLTAGE_TOO_LOW = (
        "LaundryCare.Common.Event.SupplyPower.SupplyVoltageTooLow"
    )
    LAUNDRY_CARE_DRYER_CONDENSATE_CONTAINER_FULL = "LaundryCare.Dryer.Event.CondensateContainerFull"
    LAUNDRY_CARE_DRYER_LINT_FILTER_FULL = "LaundryCare.Dryer.Event.LintFilterFull"
    LAUNDRY_CARE_DRYER_MAINTENANCE_REMIND = "LaundryCare.Dryer.Event.Maintenance.Remind"
    LAUNDRY_CARE_WASHER_DRUM_CLEAN_REMINDER = "LaundryCare.Washer.Event.DrumCleanReminder"
    LAUNDRY_CARE_WASHER_I_DOS_I_DOS_OPEN_TRAY = "LaundryCare.Washer.Event.IDos.IDosOpenTray"
    LAUNDRY_CARE_WASHER_I_DOS_1_FILL_LEVEL_POOR = "LaundryCare.Washer.Event.IDos1FillLevelPoor"
    LAUNDRY_CARE_WASHER_I_DOS_2_FILL_LEVEL_POOR = "LaundryCare.Washer.Event.IDos2FillLevelPoor"
    LAUNDRY_CARE_WASHER_I_DOS_UNIT_DEFECT = "LaundryCare.Washer.Event.IDosUnitDefect"
    LAUNDRY_CARE_WASHER_PUMP_ERROR = "LaundryCare.Washer.Event.PumpError"
    LAUNDRY_CARE_WASHER_RELEASE_RINSE_HOLD_PENDING = (
        "LaundryCare.Washer.Event.ReleaseRinseHoldPending"
    )
    LAUNDRY_CARE_WASHER_SPIN_SPIN_ABORT = "LaundryCare.Washer.Event.Spin.SpinAbort"
    REFRIGERATION_COMMON_APPLIANCE_ERROR = "Refrigeration.Common.Event.ApplianceError"
    REFRIGERATION_COMMON_CHILLER_COMMON_TEMPERATURE_ALARM = (
        "Refrigeration.Common.Event.ChillerCommon.TemperatureAlarm"
    )
    REFRIGERATION_COMMON_DISPENSER_ICE_EXPIRED = "Refrigeration.Common.Event.Dispenser.IceExpired"
    REFRIGERATION_COMMON_DISPENSER_PARTY_MODE_EMPTY_ICE_HOPPER = (
        "Refrigeration.Common.Event.Dispenser.PartyModeEmptyIceHopper"
    )
    REFRIGERATION_COMMON_DISPENSER_WATER_FILTER_ALMOST_FULL = (
        "Refrigeration.Common.Event.Dispenser.WaterFilterAlmostFull"
    )
    REFRIGERATION_COMMON_DISPENSER_WATER_FILTER_FULL = (
        "Refrigeration.Common.Event.Dispenser.WaterFilterFull"
    )
    REFRIGERATION_COMMON_DOOR_ALARM_CHILLER_COMMON = (
        "Refrigeration.Common.Event.Door.AlarmChillerCommon"
    )
    REFRIGERATION_COMMON_DOOR_ALARM_FREEZER = "Refrigeration.Common.Event.Door.AlarmFreezer"
    REFRIGERATION_COMMON_DOOR_ALARM_REFRIGERATOR = (
        "Refrigeration.Common.Event.Door.AlarmRefrigerator"
    )
    REFRIGERATION_COMMON_FREEZER_TEMPERATURE_ALARM = (
        "Refrigeration.Common.Event.Freezer.TemperatureAlarm"
    )
    REFRIGERATION_COMMON_LOW_VOLTAGE_HINT = "Refrigeration.Common.Event.LowVoltageHint"
    REFRIGERATION_COMMON_WATER_EXPIRED = "Refrigeration.Common.Event.WaterExpired"
    REFRIGERATION_FRIDGE_FREEZER_APPLIANCE_ERROR = (
        "Refrigeration.FridgeFreezer.Event.ApplianceError"
    )
    REFRIGERATION_FRIDGE_FREEZER_DOOR_ALARM_CHILLER_COMMON = (
        "Refrigeration.FridgeFreezer.Event.DoorAlarmChillerCommon"
    )
    REFRIGERATION_FRIDGE_FREEZER_DOOR_ALARM_FREEZER = (
        "Refrigeration.FridgeFreezer.Event.DoorAlarmFreezer"
    )
    REFRIGERATION_FRIDGE_FREEZER_DOOR_ALARM_REFRIGERATOR = (
        "Refrigeration.FridgeFreezer.Event.DoorAlarmRefrigerator"
    )
    REFRIGERATION_FRIDGE_FREEZER_LOW_VOLTAGE_HINT = (
        "Refrigeration.FridgeFreezer.Event.LowVoltageHint"
    )
    REFRIGERATION_FRIDGE_FREEZER_TEMPERATURE_ALARM_FREEZER = (
        "Refrigeration.FridgeFreezer.Event.TemperatureAlarmFreezer"
    )


class OptionKey(StrEnum):
    """Names of program options."""

    BSH_COMMON_DURATION = "BSH.Common.Option.Duration"
    BSH_COMMON_ELAPSED_PROGRAM_TIME = "BSH.Common.Option.ElapsedProgramTime"
    BSH_COMMON_ENERGY_FORECAST = "BSH.Common.Option.EnergyForecast"
    BSH_COMMON_ESTIMATED_TOTAL_PROGRAM_TIME = "BSH.Common.Option.EstimatedTotalProgramTime"
    BSH_COMMON_FINISH_IN_RELATIVE = "BSH.Common.Option.FinishInRelative"
    BSH_COMMON_PROGRAM_PROGRESS = "BSH.Common.Option.ProgramProgress"
    BSH_COMMON_REMAINING_PROGRAM_TIME = "BSH.Common.Option.RemainingProgramTime"
    BSH_COMMON_REMAINING_PROGRAM_TIME_IS_ESTIMATED = (
        "BSH.Common.Option.RemainingProgramTimeIsEstimated"
    )
    BSH_COMMON_START_IN_RELATIVE = "BSH.Common.Option.StartInRelative"
    BSH_COMMON_WATER_FORECAST = "BSH.Common.Option.WaterForecast"
    CONSUMER_PRODUCTS_COFFEE_MAKER_AROMA_SELECT = "ConsumerProducts.CoffeeMaker.Option.AromaSelect"
    CONSUMER_PRODUCTS_COFFEE_MAKER_BEAN_AMOUNT = "ConsumerProducts.CoffeeMaker.Option.BeanAmount"
    CONSUMER_PRODUCTS_COFFEE_MAKER_BEAN_CONTAINER_SELECTION = (
        "ConsumerProducts.CoffeeMaker.Option.BeanContainerSelection"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_BEVERAGE_SIZE = (
        "ConsumerProducts.CoffeeMaker.Option.BeverageSize"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_COARSNESS = "ConsumerProducts.CoffeeMaker.Option.Coarsness"
    CONSUMER_PRODUCTS_COFFEE_MAKER_COFFEE_MILK_RATIO = (
        "ConsumerProducts.CoffeeMaker.Option.CoffeeMilkRatio"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_COFFEE_STRENGTH = (
        "ConsumerProducts.CoffeeMaker.Option.CoffeeStrength"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_COFFEE_TEMPERATURE = (
        "ConsumerProducts.CoffeeMaker.Option.CoffeeTemperature"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_CUPS = "ConsumerProducts.CoffeeMaker.Option.Cups"
    CONSUMER_PRODUCTS_COFFEE_MAKER_FILL_QUANTITY = (
        "ConsumerProducts.CoffeeMaker.Option.FillQuantity"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_FLOW_RATE = "ConsumerProducts.CoffeeMaker.Option.FlowRate"
    CONSUMER_PRODUCTS_COFFEE_MAKER_HOT_WATER_TEMPERATURE = (
        "ConsumerProducts.CoffeeMaker.Option.HotWaterTemperature"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_MULTIPLE_BEVERAGES = (
        "ConsumerProducts.CoffeeMaker.Option.MultipleBeverages"
    )
    CONSUMER_PRODUCTS_COFFEE_MAKER_SHOT_COUNT = "ConsumerProducts.CoffeeMaker.Option.Shot.Count"
    COOKING_COMMON_HOOD_BOOST = "Cooking.Common.Option.Hood.Boost"
    COOKING_COMMON_HOOD_INTENSIVE_LEVEL = "Cooking.Common.Option.Hood.IntensiveLevel"
    COOKING_COMMON_HOOD_VENTING_LEVEL = "Cooking.Common.Option.Hood.VentingLevel"
    COOKING_OVEN_FAST_PRE_HEAT = "Cooking.Oven.Option.FastPreHeat"
    COOKING_OVEN_HEATUP_PROGRESS = "Cooking.Oven.Option.HeatupProgress"
    COOKING_OVEN_LEVEL = "Cooking.Oven.Option.Level"
    COOKING_OVEN_MEAT_PROBE_TEMPERATURE_V_2 = "Cooking.Oven.Option.MeatProbeTemperatureV2"
    COOKING_OVEN_PYROLYSIS_LEVEL = "Cooking.Oven.Option.PyrolysisLevel"
    COOKING_OVEN_QUICK_ROAST = "Cooking.Oven.Option.QuickRoast"
    COOKING_OVEN_ROTARY_SPIT = "Cooking.Oven.Option.RotarySpit"
    COOKING_OVEN_SETPOINT_TEMPERATURE = "Cooking.Oven.Option.SetpointTemperature"
    COOKING_OVEN_SETPOINT_TEMPERATURE_FAHRENHEIT = (
        "Cooking.Oven.Option.SetpointTemperatureFahrenheit"
    )
    COOKING_OVEN_USED_HEATING_MODE = "Cooking.Oven.Option.UsedHeatingMode"
    COOKING_OVEN_WEIGHT = "Cooking.Oven.Option.Weight"
    DISHCARE_DISHWASHER_BRILLIANCE_DRY = "Dishcare.Dishwasher.Option.BrillianceDry"
    DISHCARE_DISHWASHER_ECO_DRY = "Dishcare.Dishwasher.Option.EcoDry"
    DISHCARE_DISHWASHER_EXTRA_DRY = "Dishcare.Dishwasher.Option.ExtraDry"
    DISHCARE_DISHWASHER_EXTRA_RINSE = "Dishcare.Dishwasher.Option.ExtraRinse"
    DISHCARE_DISHWASHER_FLEX_SPRAY_BACK_LEFT = "Dishcare.Dishwasher.Option.FlexSpray.BackLeft"
    DISHCARE_DISHWASHER_FLEX_SPRAY_BACK_RIGHT = "Dishcare.Dishwasher.Option.FlexSpray.BackRight"
    DISHCARE_DISHWASHER_FLEX_SPRAY_FRONT_LEFT = "Dishcare.Dishwasher.Option.FlexSpray.FrontLeft"
    DISHCARE_DISHWASHER_FLEX_SPRAY_FRONT_RIGHT = "Dishcare.Dishwasher.Option.FlexSpray.FrontRight"
    DISHCARE_DISHWASHER_FLEX_SPRAY_TYPE = "Dishcare.Dishwasher.Option.FlexSpray.Type"
    DISHCARE_DISHWASHER_HALF_LOAD = "Dishcare.Dishwasher.Option.HalfLoad"
    DISHCARE_DISHWASHER_HYGIENE_PLUS = "Dishcare.Dishwasher.Option.HygienePlus"
    DISHCARE_DISHWASHER_INTENSIV_ZONE = "Dishcare.Dishwasher.Option.IntensivZone"
    DISHCARE_DISHWASHER_PRETREATMENT = "Dishcare.Dishwasher.Option.Pretreatment"
    DISHCARE_DISHWASHER_SANITATION_UC = "Dishcare.Dishwasher.Option.SanitationUC"
    DISHCARE_DISHWASHER_SILENCE_ON_DEMAND = "Dishcare.Dishwasher.Option.SilenceOnDemand"
    DISHCARE_DISHWASHER_VARIO_SPEED_PLUS = "Dishcare.Dishwasher.Option.VarioSpeedPlus"
    DISHCARE_DISHWASHER_ZEOLITE_DRY = "Dishcare.Dishwasher.Option.ZeoliteDry"
    LAUNDRY_CARE_COMMON_HYGIENIC_STEAM_INTENSITY = (
        "LaundryCare.Common.Option.HygienicSteamIntensity"
    )
    LAUNDRY_CARE_COMMON_LOAD_RECOMMENDATION = "LaundryCare.Common.Option.LoadRecommendation"
    LAUNDRY_CARE_COMMON_LOW_TEMPERATURE_HYGIENE = "LaundryCare.Common.Option.LowTemperatureHygiene"
    LAUNDRY_CARE_COMMON_PROCESS_PHASE = "LaundryCare.Common.Option.ProcessPhase"
    LAUNDRY_CARE_COMMON_SILENT_MODE = "LaundryCare.Common.Option.SilentMode"
    LAUNDRY_CARE_COMMON_SPEED_PERFECT = "LaundryCare.Common.Option.SpeedPerfect"
    LAUNDRY_CARE_COMMON_VARIO_PERFECT = "LaundryCare.Common.Option.VarioPerfect"
    LAUNDRY_CARE_DRYER_DRYING_TARGET = "LaundryCare.Dryer.Option.DryingTarget"
    LAUNDRY_CARE_DRYER_GENTLE = "LaundryCare.Dryer.Option.Gentle"
    LAUNDRY_CARE_DRYER_HALF_LOAD = "LaundryCare.Dryer.Option.HalfLoad"
    LAUNDRY_CARE_DRYER_HYGIENE = "LaundryCare.Dryer.Option.Hygiene"
    LAUNDRY_CARE_DRYER_PROCESS_PHASE = "LaundryCare.Dryer.Option.ProcessPhase"
    LAUNDRY_CARE_DRYER_REFRESHER = "LaundryCare.Dryer.Option.Refresher"
    LAUNDRY_CARE_DRYER_SPIN_CLASS = "LaundryCare.Dryer.Option.SpinClass"
    LAUNDRY_CARE_DRYER_WRINKLE_GUARD = "LaundryCare.Dryer.Option.WrinkleGuard"
    LAUNDRY_CARE_WASHER_DISINFECTANT = "LaundryCare.Washer.Option.Disinfectant"
    LAUNDRY_CARE_WASHER_HYGIENIC_STEAM = "LaundryCare.Washer.Option.HygienicSteam"
    LAUNDRY_CARE_WASHER_HYGIENIC_STEAM_INTENSITY = (
        "LaundryCare.Washer.Option.HygienicSteamIntensity"
    )
    LAUNDRY_CARE_WASHER_I_DOS_1_ACTIVE_DOTTED = "LaundryCare.Washer.Option.IDos1.Active"
    LAUNDRY_CARE_WASHER_I_DOS_1_ACTIVE = "LaundryCare.Washer.Option.IDos1Active"
    LAUNDRY_CARE_WASHER_I_DOS_1_DOSING_LEVEL = "LaundryCare.Washer.Option.IDos1DosingLevel"
    LAUNDRY_CARE_WASHER_I_DOS_2_ACTIVE_DOTTED = "LaundryCare.Washer.Option.IDos2.Active"
    LAUNDRY_CARE_WASHER_I_DOS_2_ACTIVE = "LaundryCare.Washer.Option.IDos2Active"
    LAUNDRY_CARE_WASHER_I_DOS_2_DOSING_LEVEL = "LaundryCare.Washer.Option.IDos2DosingLevel"
    LAUNDRY_CARE_WASHER_INTENSIVE_PLUS = "LaundryCare.Washer.Option.IntensivePlus"
    LAUNDRY_CARE_WASHER_LESS_IRONING = "LaundryCare.Washer.Option.LessIroning"
    LAUNDRY_CARE_WASHER_MINI_LOAD = "LaundryCare.Washer.Option.MiniLoad"
    LAUNDRY_CARE_WASHER_MULTIPLE_SOAK = "LaundryCare.Washer.Option.MultipleSoak"
    LAUNDRY_CARE_WASHER_PRE_TREATMENT = "LaundryCare.Washer.Option.PreTreatment"
    LAUNDRY_CARE_WASHER_PREWASH = "LaundryCare.Washer.Option.Prewash"
    LAUNDRY_CARE_WASHER_RINSE_HOLD = "LaundryCare.Washer.Option.RinseHold"
    LAUNDRY_CARE_WASHER_RINSE_PLUS = "LaundryCare.Washer.Option.RinsePlus"
    LAUNDRY_CARE_WASHER_RINSE_PLUS_1 = "LaundryCare.Washer.Option.RinsePlus1"
    LAUNDRY_CARE_WASHER_RINSE_PLUS_3 = "LaundryCare.Washer.Option.RinsePlus3"
    LAUNDRY_CARE_WASHER_SILENT_WASH = "LaundryCare.Washer.Option.SilentWash"
    LAUNDRY_CARE_WASHER_SOAK = "LaundryCare.Washer.Option.Soak"
    LAUNDRY_CARE_WASHER_SOAK_DURATION = "LaundryCare.Washer.Option.SoakDuration"
    LAUNDRY_CARE_WASHER_SOAK_TEMPERATURE = "LaundryCare.Washer.Option.SoakTemperature"
    LAUNDRY_CARE_WASHER_SPEED_PERFECT = "LaundryCare.Washer.Option.SpeedPerfect"
    LAUNDRY_CARE_WASHER_SPIN_SPEED = "LaundryCare.Washer.Option.SpinSpeed"
    LAUNDRY_CARE_WASHER_STAINS = "LaundryCare.Washer.Option.Stains"
    LAUNDRY_CARE_WASHER_TEMPERATURE = "LaundryCare.Washer.Option.Temperature"
    LAUNDRY_CARE_WASHER_WATER_AND_RINSE_PLUS = "LaundryCare.Washer.Option.WaterAndRinsePlus"
    LAUNDRY_CARE_WASHER_WATER_AND_RINSE_PLUS_1 = "LaundryCare.Washer.Option.WaterAndRinsePlus1"
    LAUNDRY_CARE_WASHER_WATER_PLUS = "LaundryCare.Washer.Option.WaterPlus"
    LAUNDRY_CARE_WASHER_DRYER_ACTIVITY_AFTER_WASHING = (
        "LaundryCare.WasherDryer.Option.ActivityAfterWashing"
    )
    LAUNDRY_CARE_WASHER_DRYER_DRYING_TARGET = "LaundryCare.WasherDryer.Option.DryingTarget"
    LAUNDRY_CARE_WASHER_DRYER_LOW_TEMPERATURE_HYGIENE = (
        "LaundryCare.WasherDryer.Option.LowTemperatureHygiene"
    )
    LAUNDRY_CARE_WASHER_DRYER_PROGRAM_MODE = "LaundryCare.WasherDryer.Option.ProgramMode"
    LAUNDRY_CARE_WASHER_DRYER_REFRESH_INTENSITY = "LaundryCare.WasherDryer.Option.RefreshIntensity"
    LAUNDRY_CARE_WASHER_DRYER_REFRESH_TEXTILE_TYPE = (
        "LaundryCare.WasherDryer.Option.RefreshTextileType"
    )
    LAUNDRY_CARE_WASHER_DRYER_WRINKLE_GUARD_BOOST = (
        "LaundryCare.WasherDryer.Option.WrinkleGuardBoost"
    )


class ProgramKey(StrEnum):
    """Names of programs."""

    BSH_COMMON_FAVORITE = "BSH.Common.Program.Favorite"
    COOKING_COMMON_HOOD_VENTING = "Cooking.Common.Program.Hood.Venting"


class CommandKey(StrEnum):
    """Names of commands."""

    BSH_COMMON_ABORT_PROGRAM = "BSH.Common.Command.AbortProgram"
    BSH_COMMON_ACKNOWLEDGE_EVENT = "BSH.Common.Command.AcknowledgeEvent"
    BSH_COMMON_ALLOW_SOFTWARE_DOWNLOAD = "BSH.Common.Command.AllowSoftwareDownload"
    BSH_COMMON_ALLOW_SOFTWARE_UPDATE_LOCAL_WI_FI = "BSH.Common.Command.AllowSoftwareUpdateLocalWiFi"
    BSH_COMMON_DEACTIVATE_REMOTE_CONTROL = "BSH.Common.Command.DeactivateRemoteControl"
    BSH_COMMON_DEACTIVATE_REMOTE_CONTROL_START = "BSH.Common.Command.DeactivateRemoteControlStart"
    BSH_COMMON_MAINS_POWER_OFF = "BSH.Common.Command.MainsPowerOff"
    BSH_COMMON_OPEN_DOOR = "BSH.Common.Command.OpenDoor"
    BSH_COMMON_PAUSE_PROGRAM = "BSH.Common.Command.PauseProgram"
    BSH_COMMON_REJECT_EVENT = "BSH.Common.Command.RejectEvent"
    BSH_COMMON_RESUME_PROGRAM = "BSH.Common.Command.ResumeProgram"
    BSH_COMMON_STOP_WATCH_RESET = "BSH.Common.Command.StopWatchReset"
    BSH_COMMON_STOP_WATCH_START_PAUSE_RESUME = "BSH.Common.Command.StopWatchStartPauseResume"
    COOKING_COMMON_HOOD_CARBON_FILTER_RESET = "Cooking.Common.Command.Hood.CarbonFilterReset"
    COOKING_COMMON_HOOD_GREASE_FILTER_RESET = "Cooking.Common.Command.Hood.GreaseFilterReset"
    COOKING_COMMON_HOOD_REGENERATIVE_CARBON_FILTER_LIFE_TIME_RESET = (
        "Cooking.Common.Command.Hood.RegenerativeCarbonFilterLifeTimeReset"
    )
    COOKING_COMMON_HOOD_REGENERATIVE_CARBON_FILTER_RESET = (
        "Cooking.Common.Command.Hood.RegenerativeCarbonFilterReset"
    )
    REFRIGERATION_COMMON_DISPENSER_WATER_FILTER_RESET = (
        "Refrigeration.Common.Command.Dispenser.WaterFilterReset"
    )


class RootKey(StrEnum):
    """Names of the selected and active program."""

    BSH_COMMON_ACTIVE_PROGRAM = "BSH.Common.Root.ActiveProgram"
    BSH_COMMON_SELECTED_PROGRAM = "BSH.Common.Root.SelectedProgram"
