function get_image(type, size=null, color_type=null, custom_alarm=null, subtype=null) {
    let path = "qrc:/resources/images/desktop/delegates/"

    let no_color_device = [
        "10", "11", "12", "13", "16", "17", "18", "1a", "1f",
        "22", "23", "24", "25", "2a", "2b", "2c", "2d", "2f",
        "30", "yavir_hub", "yavir_hub_plus",
    ].includes(type)
    if (no_color_device) {
        color_type = null
    }

    let device_name = {
        "01": "DoorProtect",
        "02": "MotionProtect",
        "03": "FireProtect",
        "04": "GlassProtect",
        "05": "LeaksProtect",
        "06": "MotionProtectCurtain",
        "07": "Hub",
        "08": "CombiProtect",
        "09" : "FireProtect",
        "10": "UniversalDevice",
        "11": "Transmitter",
        "12": "WallSwitch",
        "13": "MotionProtectOutdoor",
        "0a": "KeyPad",
        "0b": "SpaceControl",
        "0c": "Button",
        "0d": "MotionCam",
        "0e": "MotionProtect",
        "0f": "DoorProtect",
        "14": "StreetSiren",
        "15": "HomeSiren",
        "16": "WallSwitch",
        "17": "WallSwitch",
        "18": "MotionCamOutdoor",
        "19": "KeyPadPlus",
        "1a": "DualCurtainOutdoor",
        "1b": "StreetSirenDoubleDeck",
        "1c": "MultiTransmitter",
        "1d": "Wired",
        "1e": "Socket",
        "1f": "WallSwitch",
        "21": "Hub",
        "yavir_hub": "YavirHub",
        "fibra_hub": "MultiTransmitter",
        "yavir_hub_plus": "YavirHubPlus",
        "22": "UserPicture",
        "23": "GroupPicture",
        "24": "RoomPicture",
        "25": "Camera",
        "26": "Wired",
        "26-wired-tamper": "Wired",
        "26-wired-intrusion": "Wired",
        "27": "YavirSiren",
        "28": "YavirKeyPad",
        "28-keypad-yavir": "YavirKeyPad",
        "28-reader-yavir": "YavirReader",
        "29": "YavirKey",
        "2a": "ScenarioPicture",
        "2b": "CompanyPicture",
        "2f": "InstallerPicture",
        "2c": "SchedulePicture",
        "2e": "Pass",
        "30": "AccessCode",
        "42": "DoubleButton",
        "43": "KeyPadCombi",
        "44": "LightSwitch",
        "45": "MultiTransmitter",
        "47": "LeaksProtect", // LifeQuality
        "4c": "SocketBase",
        "4d": "FireProtect2Base",
        "61": "DoorProtectFibra",
        "62": "MotionProtectFibra",
        "6e": "MotionProtectFibra",
        "6f": "DoorProtectFibra",
        "46": "Hub",
        "64": "GlassProtectFibra",
        "68": "CombiProtectFibra",
        "6a": "KeyPad",
        "74": "StreetSiren",
        "75": "HomeSiren",
        "7b": "StreetSirenDoubleDeck",
        "7c": "MultiTransmitterFibra",
        "TAG": "Tag",
        "CARD": "Pass",
    }[type]

    // if Wire Input MT
    if (type == "1d"){
        return path + device_name + "/" + generate_wire_alarm_image_filename(color_type, size, custom_alarm)
    }

    // if Wire Input
    if (["26", "26-wired-tamper", "26-wired-intrusion"].includes(type)){
        let wire_name = type == "26-wired-intrusion" ? "Intrusion" : "Tamper"
        return path + device_name + "/" + wire_name + size + ".png"
    }
    if (!device_name) {
        device_name = "RoomPicture"
        color_type = null
    }

    // Add device class name to path
    let image_path = path + device_name + "/"

     // Add subtype dir and name if it's subtype
    if (subtype && subtype != "NO_SUBTYPE") {
        image_path += subtype + "/" + subtype
    } else {
        // Add type of the device
        image_path += device_name
    }

    // Add color to path if exists
    if (color_type) image_path += add_suffix_by_device_color(color_type)

    // Add size to path
    image_path += size

    // Add ending
    image_path += ".png"

    return image_path
}

function add_suffix_by_device_color(color_type) {
    let device_color = {
        "WHITE": "White",
        "WHITE_LABEL_WHITE": "White",
        "NO_COLOR_INFO": "White",
        "BLACK": "Black",
        "WHITE_LABEL_BLACK": "Black",
        "PANEL_COLOR_UNSPECIFIED": "White",
        "PANEL_COLOR_WHITE": "White",
        "PANEL_COLOR_BLACK": "Black",
        "PANEL_COLOR_FOG": "Fog",
        "PANEL_COLOR_GRAPHITE": "Graphite",
        "PANEL_COLOR_GREY": "Grey",
        "PANEL_COLOR_IVORY": "Ivory",
        "PANEL_COLOR_OLIVE": "Olive",
        "PANEL_COLOR_OYSTER": "Oyster",
    }[color_type]
    return device_color ? device_color : ""
}

function bridgeOutputs(type, size) {
    var path = "qrc:/resources/images/desktop/delegates/VHFOutputs/" + size + "/"
    return path + type + ".png"
}

function generate_wire_alarm_image_filename(color_type, size, custom_alarm="TAMPER_ALARM") {
    var image_name = "Tamper"

    if (color_type == 1) {
        const custom_alarm_map = {
            "BURGLARY_ALARM": "Intrusion",
            "FIRE_ALARM": "Fire",
            "MEDICAL_ALARM": "MedicalHelp",
            "PANIC_ALARM": "PanicButton",
            "GAS_ALARM": "Gas",
            "TAMPER_ALARM":"Tamper",
            "MALFUNCTION_ALARM": "Malfunction",
            "LEAK_ALARM": "Leak",
            "SERVICE_EVENT": "Service",
        }
        var image_name = custom_alarm_map[custom_alarm]
    }

    return image_name + size + ".png"
}
