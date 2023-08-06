import QtQuick 2.12
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.13
import QtGraphicalEffects 1.12

import "qrc:/resources/js/desktop/popups.js" as Popups
import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.ButtonContainedRect {
    property var popup: null
    property var fires: management.devices.fire_alarms
    property var state: hub.fire_interconnected && fires["flag"]

    Component.onCompleted: {
        if (state && hub.is_interconnected) popup = Popups.interconnect_popup(fires["fires"], null, fires["isCriticalCOAlarm"])
    }

    anchors.verticalCenter: parent.verticalCenter

    buttonIconSource: "qrc:/resources/images/Athena/common_icons/VolumeOff-S.svg"
    text: tr.interconnect
    status: DS3.ButtonRect.Status.Attention

    visible: {
        var state = (hub.fire_interconnected && management.devices.fire_alarms["flag"])
        return state && hub.is_interconnected
    }

    onVisibleChanged: {
        if (visible) {
            popup = Popups.interconnect_popup(fires["fires"], null, fires["isCriticalCOAlarm"])
        } else {
            if (popup) { popup.close() }
        }
    }

    onClicked: Popups.interconnect_popup(fires["fires"], null, fires["isCriticalCOAlarm"])
}