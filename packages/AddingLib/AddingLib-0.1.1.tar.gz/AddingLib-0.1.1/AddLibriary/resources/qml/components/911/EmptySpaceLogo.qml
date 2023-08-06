import QtQuick 2.12
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/911" as Custom


Item {
    id: emptySpaceLogo

    property var size: Math.min(parent.width, parent.height) / 3
    property var text: ""

    property alias emptyText: emptyText

    anchors.fill: parent

    opacity: 0.2

    Item {
        width: parent.width
        height: emptySpaceLogo.text ? emptySpaceLogo.size + emptyText.height : emptySpaceLogo.size

        anchors.centerIn: parent

        Image {
            anchors {
                top: parent.top
                horizontalCenter: parent.horizontalCenter
            }

            sourceSize.width: emptySpaceLogo.size
            sourceSize.height: emptySpaceLogo.size
            source: "qrc:/resources/images/icons/a-logo-pro.svg"
        }

        Custom.FontText {
            id: emptyText

            width: parent.width / 2
            height: contentHeight

            anchors {
                bottom: parent.bottom
                horizontalCenter: parent.horizontalCenter
            }

            text: emptySpaceLogo.text
            color: ui.colors.white
            font.pixelSize: 20
            wrapMode: Text.WordWrap
            textFormat: Text.PlainText
            elide: Text.ElideRight
            verticalAlignment: Text.AlignVCenter
            horizontalAlignment: Text.AlignHCenter
        }
    }
}