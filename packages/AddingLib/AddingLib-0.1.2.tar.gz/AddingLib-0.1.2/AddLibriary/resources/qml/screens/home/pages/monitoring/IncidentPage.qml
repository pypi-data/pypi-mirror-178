import QtQuick 2.12
import QtQuick.Controls 2.13
import QtGraphicalEffects 1.13
import QtQuick.Layouts 1.13

import "qrc:/resources/js/incidents.js" as Incidents
import "qrc:/resources/qml/components/911" as Custom

Rectangle {
    border.width: 0
    border.color: "red"
    color: "transparent"

    Rectangle {
        anchors.fill: parent
        color: ui.colors.dark4
        visible: currentId == null

        Custom.FontText {
            width: parent.width * 0.5
            color: ui.colors.middle1
            font.pixelSize: 16
            wrapMode: Text.WordWrap
            anchors.centerIn: parent
            text: tr.a911_select_an_incident_from_the_list_to_get_started_alt
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
        }
    }
}