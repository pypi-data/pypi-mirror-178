import "qrc:/resources/qml/components/911/DS3/" as DS3


DS3.InfoTitle {
    property bool isBad: false

    atomTitle {
        title: tr.voltage
        subtitle: device.voltage == "N/A" ? tr.na : device.voltage + " " + tr.v
    }
    leftIcon.source: "qrc:/resources/images/Athena/views_icons/Voltage-M.svg"
    status: isBad ? ui.ds3.status.ATTENTION : ui.ds3.status.DEFAULT
}