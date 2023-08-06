import QtQuick 2.7
import QtQuick.Controls 2.1

import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.InfoTitle {
    atomTitle {
        title: tr.panic_button_enabled
        subtitle: device.panic_enabled ? tr.enabled : tr.off
    }
    leftIcon.source: "qrc:/resources/images/Athena/views_icons/Alarm-M.svg"
}
