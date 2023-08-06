import QtQuick 2.7
import QtQuick.Controls 2.1
import QtQuick.Layouts 1.3

import "qrc:/resources/qml/components/911/DS3" as DS3

DS3.InfoTitle {
    atomTitle {
        title: tr.sensitivity
        subtitle: {
            if (device.sensitivity == 1) {
                return tr.normal
            } else if (device.sensitivity == 0) {
                return tr.device_settings_sensitivity_array_0
            } else if (device.sensitivity == 2) {
                return tr.device_settings_sensitivity_array_2
            } else {
                return tr.na
            }
        }
    }
    leftIcon.source: "qrc:/resources/images/Athena/views_icons/Sensitivity-M.svg"
}