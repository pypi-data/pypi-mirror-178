import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.SettingsNavigationTitlePrimary {
    property var isReX2: false

    title: tr.pair_with_device
    icon: "qrc:/resources/images/Athena/settings_icons/PairWithDeviceSettings-L.svg"

    onEntered: {
        setChild(
            "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/tests/RexDevices.qml",
            {"rangeExtender": device, "isReX2": isReX2}
        )
    }
}