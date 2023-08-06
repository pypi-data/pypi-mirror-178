import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.InfoTitle {
    atomTitle {
        title: tr.last_consumption_reset
        subtitle: {
            if (device.date_of_energy_counter_reset === "TODAY") return tr.today
            else return util.insert(tr.info_days_ago_desktop, [device.date_of_energy_counter_reset, device.number_of_days_of_last_energy_reset])
        }
    }
    leftIcon.source: "qrc:/resources/images/Athena/views_icons/ConsumptionReset-M.svg"
    visible: device.date_of_energy_counter_reset !== "N/A"
}