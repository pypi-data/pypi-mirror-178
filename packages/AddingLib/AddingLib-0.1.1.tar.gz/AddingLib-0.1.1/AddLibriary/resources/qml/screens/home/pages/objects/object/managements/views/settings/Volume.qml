import QtQuick 2.7
import QtQuick.Controls 2.1

import "qrc:/resources/qml/components/911/DS3" as DS3

DS3.InfoTitle {
    atomTitle {
        title: tr.siren_volume
        subtitle: {
            if (device.siren_volume_level == 1) {
                return tr.volume_max
            }
            else if (device.siren_volume_level == 18) {
                return tr.volume_mid
            }
            else if (device.siren_volume_level == 29) {
                return tr.volume_min
            }
            else if (device.siren_volume_level == 32) {
                return tr.volume_silent
            }
            return tr.na
        }
    }
    leftIcon.source: "qrc:/resources/images/Athena/views_icons/Volume-M.svg"
}
