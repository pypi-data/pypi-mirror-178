import "qrc:/resources/qml/components/911/DS3" as DS3
import "qrc:/resources/js/desktop/popups.js" as DesktopPopups


DS3.SettingsNavigationTitlePrimary {
    title: device.is_fibra ?
        tr.fibra_signal_strength_test :
        tr.signal_strength_test
    icon: device.is_fibra ?
        "qrc:/resources/images/Athena/settings_icons/FibraSettings-L.svg" :
        "qrc:/resources/images/Athena/settings_icons/JewellerSettings-L.svg"
    enabled: devEnable

    onEntered: {
        if (hub.scan_status == "SCAN_STARTED") {
            DesktopPopups.popupByPath("qrc:/resources/qml/screens/home/pages/objects/object/popups/Fibra_popups/FibraScanningInterruptPopup.qml", {"hub": hub})
            return
        }
        if (hub.max_power_test_state == "TEST_IN_PROGRESS") {
            DesktopPopups.popupByPath("qrc:/resources/qml/screens/home/pages/objects/object/popups/Fibra_popups/WireTestInterruptPopup.qml", {"hub": hub})
            return
        }
        setChild(
            "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/tests/SignalLevelTest.qml"
        )
    }
}