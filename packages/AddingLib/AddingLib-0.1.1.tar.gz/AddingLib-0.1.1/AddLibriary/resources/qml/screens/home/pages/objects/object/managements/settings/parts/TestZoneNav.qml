import "qrc:/resources/qml/components/911/DS3" as DS3
import "qrc:/resources/js/desktop/popups.js" as DesktopPopups


DS3.SettingsNavigationTitlePrimary {
    title: tr.detection_zone_test
    icon: "qrc:/resources/images/Athena/settings_icons/DetectionZoneSettings-L.svg"

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
            "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/tests/ZoneTest.qml"
        )
    }
}
