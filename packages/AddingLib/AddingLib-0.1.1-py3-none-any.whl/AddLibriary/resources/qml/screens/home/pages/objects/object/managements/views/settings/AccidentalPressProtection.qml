import QtQuick 2.7
import QtQuick.Controls 2.1

import "qrc:/resources/qml/components/911/DS3" as DS3

DS3.InfoTitle {
    atomTitle {
        title: tr.falsePressFilter
        subtitle: {
            var items = [tr.off, tr.long_press, tr.double_press]
            return items[device.false_press_filter - 1]
        }
    }
    leftIcon.source: "qrc:/resources/images/Athena/views_icons/AccidentalPressProtection-M.svg"
}