import "qrc:/resources/qml/components/911/DS3" as DS3
import "qrc:/resources/js/desktop/popups.js" as Popups


DS3.SettingsTitleSecondaryNavigation {
    title: tr.humidity_lq_value
    subtitle: `${util.insert(tr.humidity_value_desktop, [device.min_comfort_humidity, device.max_comfort_humidity])}%`

    onEntered: setChild(
        "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/comfort_ranges/HumidityComfortRange.qml"
    )
}
