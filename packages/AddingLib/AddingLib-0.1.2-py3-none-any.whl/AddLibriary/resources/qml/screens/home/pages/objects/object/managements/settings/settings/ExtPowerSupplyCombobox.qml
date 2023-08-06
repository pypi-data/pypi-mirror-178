import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.SettingsPickerTitleSecondary {
    atomTitle.title: tr.extPowerSupply
    model: [tr.off, tr.disable_supply_while_hub_is_disarmed, tr.on]
    currentIndex: device.ext_power_supply - 1
}