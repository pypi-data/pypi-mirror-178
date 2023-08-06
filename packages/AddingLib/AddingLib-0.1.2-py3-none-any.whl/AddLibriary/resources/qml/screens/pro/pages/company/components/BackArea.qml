import QtQuick 2.12
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/911/" as Custom


Rectangle {
    width: 64
    height: parent.height
    color: ui.colors.dark4

    anchors.left: parent.left

    property alias backArea: backArea

    Image {
        source: "qrc:/resources/images/icons/back-arrow.svg"
        sourceSize.width: 24
        sourceSize.height: 24

        anchors {
            top: parent.top
            topMargin: 24
            horizontalCenter: parent.horizontalCenter
        }
    }

    Custom.HandMouseArea {
        id: backArea
    }
}
