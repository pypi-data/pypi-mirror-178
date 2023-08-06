import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.InfoTitle {
    status: device.battery_charge_volt <= 7 ?
        ui.ds3.status.ATTENTION :
        ui.ds3.status.DEFAULT
    atomTitle {
        title: tr.wire_supply_voltage_device_info
        subtitle: device.battery_charge_volt ? device.battery_charge_volt + ' V' : tr.na
    }
    leftIcon.source: "qrc:/resources/images/Athena/views_icons/Voltage-M.svg"
}
