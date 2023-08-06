import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.InfoTitle {
    atomTitle {
        title: tr.power
        subtitle: device.watt_sec == "N/A" ? tr.na : device.watt_sec + " " + tr.watt
    }
    leftIcon.source: "qrc:/resources/images/Athena/views_icons/Watt-M.svg"
}