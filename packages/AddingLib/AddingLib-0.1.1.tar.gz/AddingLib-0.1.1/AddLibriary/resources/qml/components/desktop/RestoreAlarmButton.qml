
import QtQuick 2.7
import QtQuick.Controls 2.2
import QtGraphicalEffects 1.12

import "qrc:/resources/js/desktop/popups.js" as Popups


Rectangle {
    id: restoreAlarmButton
    width: 26
    height: 26
    radius: 5
    color: "#F64347"

    visible: hub.alarm_happened

    property var once: false
    property var popup: null

    anchors {
        verticalCenter: parent.verticalCenter
    }

    Image {
        id: volumeImg
        width: 20
        height: 20
        visible: false

        source: "qrc:/resources/images/desktop/icons/restore-after-alarm.png"
        anchors.centerIn: parent
    }

    ColorOverlay {
        anchors.fill: volumeImg
        source: volumeImg
        color: ui.colors.white
    }


    MouseArea {
        anchors.fill: parent
        hoverEnabled: true
        cursorShape: Qt.PointingHandCursor

        onClicked: {
            Popups.reset_alarm_popup(hub, management)
        }
    }
}
