function count_left_arrow(gridView) {
   if (gridView.currentIndex == 0 || currentIndex == -1) {
        gridView.currentIndex = gridView.model.length - 1
    } else {
        gridView.currentIndex -= 1
    }
    gridView.positionViewAtIndex(gridView.currentIndex, GridView.Contain)
}

function count_right_arrow(gridView) {
    if (gridView.currentIndex == gridView.model.length - 1) {
        gridView.currentIndex = 0
    } else {
        gridView.currentIndex += 1
    }
    gridView.positionViewAtIndex(gridView.currentIndex, GridView.Contain)
}

function createIconObject(parent, icon) {
    var path = "qrc:/resources/qml/screens/home/pages/objects/object/managements/delegates/parts/".concat("", icon)
    var component = Qt.createComponent(path);
    var element = component.createObject(parent);

    if (element == null) {
        // Error handling
        console.log("Error creating object");
    }
}

function get_data_hub_state(state) {
    var url;
    var text = tr.disarmed;
    var color = ui.colors.white

    switch(state) {
    case "DISARMED":
        url = "qrc:/resources/images/pro/icons_groups/disarmed.svg";
        text = tr.disarmed
        break;
    case "DISARMED_NIGHT_MODE_OFF":
        url = "qrc:/resources/images/pro/icons_groups/disarmed.svg";
        text = tr.disarmed
        break;
    case "ARMED":
        url = "qrc:/resources/images/pro/icons_groups/armed.svg";
        text = tr.armed
        break;
    case "ARMED_NIGHT_MODE_OFF":
        url = "qrc:/resources/images/pro/icons_groups/armed.svg";
        text = tr.armed
        break;
    case "ARMED_NIGHT_MODE_ON":
        url = "qrc:/resources/images/pro/icons_groups/armed.svg";
        text = tr.armed
        break;
    case "DISARMED_NIGHT_MODE_ON":
        url = "qrc:/resources/images/icons/night-mode.svg";
        text = tr.part_arm
        break;
    case "PARTIALLY_ARMED_NIGHT_MODE_ON":
        url = "qrc:/resources/images/icons/night-mode.svg";
        text = tr.part_arm
        break;
    case "NIGHT_MODE":
        url = "qrc:/resources/images/icons/night-mode.svg";
        text = tr.part_arm
        break;
    case "PARTIALLY_ARMED_NIGHT_MODE_OFF":
        url = "qrc:/resources/images/icons/icon-a-hub-status-icon-partially-armed.svg";
        text = tr.selective_armed
        break;
    case "PERIMETER_ARMED":
        url = "";
        text = tr.perimeter_armed
        break;
    case "APP_EXIT_TIMER_IN_PROGRESS":
        url = "qrc:/resources/images/icons/tsa-red.svg";
        text = tr.arming_in_progress;
        color = ui.colors.red2
        break;
    case "SECOND_STAGE_TIMER_IN_PROGRESS":
        url = "qrc:resources/images/icons/tsa-green.svg";
        text = tr.arming_in_progress;
        color = ui.colors.lime2
        break;
    case "ARMING_INCOMPLETE":
        url = "qrc:/resources/images/icons/tsa-yellow.svg";
        text = tr.arming_incomplete
        color = ui.colors.yellow1
        break;
    case "FINAL_DOOR_BOUNCE_TIMER_IN_PROGRESS":
        url = "qrc:resources/images/icons/tsa-green.svg";
        text = tr.arming_in_progress;
        color = ui.colors.lime2
        break;
    }
    return [url, text, color]
}

function check_feature_enabled(source_type, code) {
    // SOCKET TYPE G PLUS EVENTS
    if (code.toUpperCase().includes("4C_31")) return __socket_type_g_plus_features__

    let features_flag_map = {
        "44": __light_switch_features__,
        "47": __life_quality_features__,
        "4d": __fp2_features__,
    }

    return source_type in features_flag_map ? features_flag_map[source_type] : true
}