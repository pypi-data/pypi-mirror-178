import "qrc:/resources/qml/components/911/DS3" as DS3
import "qrc:/resources/js/desktop/popups.js" as Popups


DS3.SettingsTitleSecondaryNavigation {
    title: tr.co_level_lq_value
    subtitle: `${util.insert(tr.co_value_desktop, [device.max_comfort_co2])} ${tr.ppm_co_level_value}`

    onEntered: setChild(
        "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/comfort_ranges/CO2ComfortRange.qml"
    )
}
