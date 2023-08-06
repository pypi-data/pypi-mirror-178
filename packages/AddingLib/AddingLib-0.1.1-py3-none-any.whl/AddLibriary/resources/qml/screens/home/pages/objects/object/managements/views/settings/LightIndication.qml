import QtQuick 2.7
import QtQuick.Controls 2.1

import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.InfoTitle {
    atomTitle {
        title: tr.light_indication
        subtitle: ({
            0: tr.na,
            1: tr.disabled,
            2: tr.armed,
            3: tr.always_enable
        }[device.blink_while_armed])
    }
    leftIcon.source: "qrc:/resources/images/Athena/views_icons/BrightnessHigh-M.svg"
}
