import QtQuick 2.7
import QtQuick.Controls 2.1
import QtQuick.Layouts 1.3

import "qrc:/resources/qml/screens/home/pages/objects/object/managements/views/parts"

SettingField {
    sourceIcon: "qrc:/resources/images/Athena/views_icons/delay_exit.png"
    propertyName: tr.delay_when_leaving_in_night_mode_sec
    propertyValue: {
        if (!device.perimeter_protection_group) {
            return tr.off
        } else if (device.perimeter_arm_delay_seconds == 0) {
            return tr.off
        } else {
            return device.perimeter_arm_delay_seconds
        }
    }
}