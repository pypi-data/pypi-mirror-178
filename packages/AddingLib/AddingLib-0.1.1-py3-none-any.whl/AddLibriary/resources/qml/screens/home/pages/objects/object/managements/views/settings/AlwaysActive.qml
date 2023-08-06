import QtQuick 2.7
import QtQuick.Controls 2.1

import "qrc:/resources/qml/components/911/DS3" as DS3

DS3.InfoTitle {
    atomTitle {
        title: tr.always_active
        subtitle: device.always_active ? tr.yes : tr.no
    }
    leftIcon.source: "qrc:/resources/images/Athena/views_icons/AlwaysActive-M.svg"
}