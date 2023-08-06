import QtQuick 2.7
import QtQuick.Controls 2.1

import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.InfoTitle {
    property bool isBad: !device.card_enabled

    atomTitle {
        title: tr.card_is_active
        subtitle: device.card_enabled ? tr.yes : tr.no
    }

    leftIcon.source: "qrc:/resources/images/Athena/views_icons/PassTag-M.svg"
    status: isBad ? ui.ds3.status.ATTENTION : ui.ds3.status.DEFAULT
}
