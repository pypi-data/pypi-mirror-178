import QtQuick 2.12
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/911/" as Custom

Item {
    id: stateHubWithoutGroups
    anchors.fill: parent
    property var stateHub: null

    Connections {
        target: stateHubWithoutGroups
        onStateHubChanged: {
            switch(stateHub) {
                case "DISARMED":
                    mainImage.source = "qrc:/resources/images/pro/icons_groups/disarmed.svg";
                    signature.text = tr.disarmed;
                    signature.color = ui.colors.light4;
                    break;
                case "ARMED":
                    mainImage.source = "qrc:/resources/images/pro/icons_groups/armed.svg";
                    signature.text = tr.armed;
                    break;
                case "NIGHT_MODE":
                    mainImage.source = "qrc:/resources/images/icons/night-mode.svg";
                    signature.text = tr.perimeter_armed;
                    break;
            }
        }
    }
    Rectangle {
        id: iconMode
        width: 86
        height: 86
        anchors.centerIn: parent
        color: "transparent"
        anchors {
            top: parent.top
            topMargin: 201
            horizontalCenter: parent.horizontalCenter
        }
        Image {
            id: mainImage
            anchors.centerIn: parent
            width: 86
            height: 86
            sourceSize.width: 86
            sourceSize.height: 86
        }
    }

    Custom.FontText {
        id: signature
        text: tr.armed
        font.pixelSize: 18
        color: ui.colors.green1
        anchors {
            top: iconMode.bottom
            topMargin: 13
            horizontalCenter: iconMode.horizontalCenter
        }
    }
}