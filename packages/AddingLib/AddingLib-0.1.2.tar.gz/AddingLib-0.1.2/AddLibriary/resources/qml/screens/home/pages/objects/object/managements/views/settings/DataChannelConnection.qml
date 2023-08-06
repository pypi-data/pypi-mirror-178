import QtQuick 2.7
import QtQuick.Controls 2.1

import "qrc:/resources/qml/components/911/DS3" as DS3

DS3.InfoTitle {
    property bool isBad: !["1", "N/A"].includes(device.data_channel_ok)

    atomTitle {
        title: tr.data_channel_connection
        subtitle:  {
            if (device.data_channel_ok == "N/A") { return tr.na }
            return (device.data_channel_ok == "1") ? tr.online : tr.offline
        }
    }
    leftIcon.source: "qrc:/resources/images/Athena/views_icons/Wings-M.svg"
    status: isBad ? ui.ds3.status.ATTENTION : ui.ds3.status.DEFAULT
}