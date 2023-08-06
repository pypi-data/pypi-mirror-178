import QtQuick 2.7
import QtQuick.Controls 2.1

import "qrc:/resources/qml/components/911/DS3" as DS3

DS3.InfoTitle {
    visible: device.test_signal_lost_available && device.transmission_power_mode > 0
    atomTitle {
        title: tr.power_management
        subtitle: {
            if (device.transmission_power_mode == 1) return tr.alt_6db
            if (device.transmission_power_mode == 3) return tr.max
            return ""
        }
    }
    leftIcon.source: "qrc:/resources/images/Athena/views_icons/SignalAttenuation-M.svg"
    status: ui.ds3.status.ATTENTION
}