import "qrc:/resources/qml/components/911/DS3" as DS3
import "qrc:/resources/js/desktop/popups.js" as Popups


DS3.SettingsNavigationTitlePrimary {
    visible: hub.scenarios_available && hub.current_user.scenario_edit_access
    title: tr.scenarios
    icon: "qrc:/resources/images/Athena/settings_icons/ScenariosSettings-L.svg"
    enabled: devEnable

    onEntered: {
        if (device.obj_type == "0c") {
            management.filtered_scenarios_by_button.set_filter(device.device_id, device.obj_type)
        } else {
            management.filtered_scenarios_by_target.set_filter(device.device_id, device.obj_type)
        }
        Popups.popupByPath(
            "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/tests/scenarios/DeviceScenariosPopup.qml",
            {device: device}
        )
    }
}