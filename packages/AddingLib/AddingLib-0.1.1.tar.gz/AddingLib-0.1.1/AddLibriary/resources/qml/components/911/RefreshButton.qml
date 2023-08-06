import QtQuick 2.12
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/911/" as Custom


Item {
    id: button
    anchors.fill: parent

    property alias refreshArea: refreshArea
    property alias refreshAnim: refreshAnim

    Image {
        id: image
        source: "qrc:/resources/images/desktop/button_icons/ic-hub-refresh@2x.png"
        anchors {
            verticalCenter: parent.verticalCenter
        }

        RotationAnimation on rotation {
            id: refreshAnim
            loops: 1
            from: 0
            to: 360
            running: false
            duration: 500
        }
    }

    Text {
        text: tr.Refresh_button_desktop
        color: ui.colors.green1
        font.pixelSize: 14
        font.family: roboto.name
        font.weight: Font.Light

        anchors {
            verticalCenter: parent.verticalCenter
            left: image.right
            leftMargin: 7
        }
    }

    Custom.HandMouseArea {
        id: refreshArea
    }
}
