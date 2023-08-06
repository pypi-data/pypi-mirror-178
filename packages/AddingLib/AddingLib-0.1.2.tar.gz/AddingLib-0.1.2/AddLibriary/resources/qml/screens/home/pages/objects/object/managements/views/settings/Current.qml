import "qrc:/resources/qml/components/911/DS3/" as DS3


DS3.InfoTitle {
    property bool isBad: false

    atomTitle {
        title: tr.current
        subtitle: device.current == "N/A" ? tr.na : device.current + " A"
    }
    leftIcon.source: "qrc:/resources/images/Athena/views_icons/Current-M.svg"
    status: isBad ? ui.ds3.status.ATTENTION : ui.ds3.status.DEFAULT
}