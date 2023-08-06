import "qrc:/resources/qml/components/911/DS3" as DS3
import "qrc:/resources/js/desktop/popups.js" as Popups


DS3.SettingsTitleSecondaryNavigation {
    title: tr.temperature
    subtitle: `${util.insert(
        tr.temperature_value_desktop, [
            `${settings.measure_system == "imperial"
                ? Math.round((device.min_comfort_temperature * 9 / 5 + 32) / 2) * 2
                : device.min_comfort_temperature}°`,
            `${settings.measure_system == "imperial"
                ? Math.round((device.max_comfort_temperature * 9 / 5 + 32) / 2) * 2
                : device.max_comfort_temperature}°`,
        ])}${settings.measure_system == "imperial" ? "F" : "C"}`

    onEntered: setChild(
        "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/comfort_ranges/TemperatureComfortRange.qml"
    )
}
