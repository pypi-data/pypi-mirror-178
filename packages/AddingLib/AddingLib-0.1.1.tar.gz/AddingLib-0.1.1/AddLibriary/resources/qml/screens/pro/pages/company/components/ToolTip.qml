import QtQuick 2.12
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/qml/screens/pro/pages/company/components" as Desktop


ToolTip {
    id: toolTip

    width: 236
    height: toolTipContentText.contentHeight + 24

    x: -(width + 16)
    y: (parent.height - height) / 2 + 8

    text: ""
    visible: false

    contentItem: Custom.FontText {
        id: toolTipContentText

        color: ui.colors.light3
        text: toolTip.text

        font.pixelSize: 12
        wrapMode: Text.Wrap
        textFormat: Text.PlainText
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter

        anchors.centerIn: parent
    }

    background: Rectangle {
        radius: 8
        color: ui.colors.dark4
        anchors.fill: parent
    }
}