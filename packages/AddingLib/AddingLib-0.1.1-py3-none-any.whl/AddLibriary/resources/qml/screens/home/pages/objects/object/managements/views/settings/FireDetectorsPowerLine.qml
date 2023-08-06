import QtQuick 2.7
import QtQuick.Controls 2.1
import QtQuick.Layouts 1.3

import "qrc:/resources/qml/components/911/DS3/" as DS3


DS3.InfoTitle {
    property bool isBad: device.external_fire_notifiers_power_broken && device.external_fire_notifiers_power_broken != -1

    atomTitle {
        title: tr.fire_detectors_power_line
        subtitle: {
            if (device.external_fire_notifiers_power_broken == -1) {
                return tr.na
            }
            if (device.external_fire_notifiers_power_broken) {
                return tr.detectors_shorted_out
            }
            return tr.ok
        }
    }
    leftIcon.source: "qrc:/resources/images/Athena/views_icons/PowerLine-M.svg"
    status: isBad ? ui.ds3.status.ATTENTION : ui.ds3.status.DEFAULT
}
