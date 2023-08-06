import QtQuick 2.12
import QtQuick.Controls 2.13
import QtGraphicalEffects 1.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/911/" as Custom

Rectangle {
    color: ui.colors.dark4
    Layout.fillWidth: true
    Layout.fillHeight: true

    Custom.EmptySpaceLogo {
        size: parent.height / 5
        visible: listView.model.length == 0
    }

    ListView {
        id: listView
        clip: true
        spacing: 4
        width: parent.width
        boundsBehavior: Flickable.StopAtBounds

        anchors {
            top: parent.top
            bottom: parent.bottom
        }

        model: {
            if (incident == null) return []
            return incident.filtered_rapid_response_teams
        }

        delegate: GBR {
            height: 240
            width: listView.width

            Rectangle {
                width: parent.width + 32
                height: 4
                color: ui.colors.black
                anchors.top: parent.bottom
                anchors.topMargin: 16
                anchors.horizontalCenter: parent.horizontalCenter
            }
        }
    }
}