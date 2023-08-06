import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.InfoTitle {
    atomTitle {
        title: tr.power_consumed
        subtitle: device.power_wth == "N/A" ? tr.na : device.power_wth + " " + tr.kwh
    }
    leftIcon.source: "qrc:/resources/images/Athena/views_icons/ElectricEnergyConsumed-M.svg"
}