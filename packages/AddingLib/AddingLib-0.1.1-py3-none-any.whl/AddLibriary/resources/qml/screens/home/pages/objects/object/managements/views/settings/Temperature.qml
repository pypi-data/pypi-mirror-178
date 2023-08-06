import QtQuick 2.7
import QtQuick.Controls 2.1
import QtQuick.Layouts 1.3

import "qrc:/resources/qml/components/911/DS3" as DS3

DS3.InfoTitle {
    property var min: -10 // Celcium
    property var max: 40
    property bool isBad: device.temperature > max || device.temperature < min  // C

    atomTitle {
        title: tr.temperature
        subtitle: {
            if (device.temperature == "N/A") { return tr.na }
            return settings.measure_system == "imperial" ?
                Math.round(device.temperature * 9 / 5 + 32) + " °F" :
                device.temperature + " °C"
        }
    }
    leftIcon.source: "qrc:/resources/images/Athena/views_icons/Temperature-M.svg"
    status: isBad ? ui.ds3.status.ATTENTION : ui.ds3.status.DEFAULT
}