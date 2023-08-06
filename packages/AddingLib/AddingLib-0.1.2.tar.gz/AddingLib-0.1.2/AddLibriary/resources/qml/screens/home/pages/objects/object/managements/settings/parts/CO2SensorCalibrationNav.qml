import "qrc:/resources/qml/components/911/DS3" as DS3
import "qrc:/resources/js/desktop/popups.js" as Popups


DS3.SettingsNavigationTitlePrimary {
    icon: "qrc:/resources/images/Athena/settings_icons/ServiceSettingsCalibration-L.svg"
    title: tr.co_sensor_calibration

    onEntered: setChild(
        "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/tests/CO2SensorCalibrationPopupStep.qml"
    )
}
