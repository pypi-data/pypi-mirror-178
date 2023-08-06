import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.SettingsNavigationTitlePrimary {
    title: tr.bypass_mode
    icon: "qrc:/resources/images/Athena/settings_icons/TemporaryDeactivationSettings-L.svg"
    visible: {
        if (device.obj_type == "14" || device.obj_type == "1b") {
            return device.bypass_available
        }
        return hub.firmware_version_dec >= 208107
    }
    enabled: hub && hub.online && (device.assigned_extender_name == "" || device.is_assigned_extender_online)

    onEntered: {
        setChild(
            "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/tests/BypassPopupStep.qml"
        )
    }
}