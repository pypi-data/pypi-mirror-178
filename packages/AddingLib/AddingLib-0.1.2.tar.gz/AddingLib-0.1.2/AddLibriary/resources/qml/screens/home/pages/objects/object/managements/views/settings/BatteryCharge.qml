import QtQuick 2.7
import QtQuick.Controls 2.1
import QtQuick.Layouts 1.3

import "qrc:/resources/qml/components/911/DS3/" as DS3


DS3.InfoTitle {
    property bool isBad: device.battery <= 20

    atomTitle {
        title: tr.battery_charge
        subtitle: device.battery != "N/A" ? device.battery + "%" : tr.na
    }
    leftIcon.source: "qrc:/resources/images/Athena/views_icons/BatteryCharge-M.svg"
    status: isBad ? ui.ds3.status.ATTENTION : ui.ds3.status.DEFAULT
}
