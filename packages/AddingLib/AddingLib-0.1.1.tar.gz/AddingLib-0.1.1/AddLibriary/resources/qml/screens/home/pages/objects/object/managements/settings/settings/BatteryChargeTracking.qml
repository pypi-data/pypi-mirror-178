import "qrc:/resources/qml/components/911/DS3/" as DS3
import "qrc:/resources/js/desktop/popups.js" as DesktopPopups


DS3.SettingsSwitch {
    title: tr.battery_charge_tracking
    checked: device.battery_charge_tracking
}