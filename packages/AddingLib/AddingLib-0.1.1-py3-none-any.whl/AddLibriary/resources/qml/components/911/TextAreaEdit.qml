import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/" as Custom


Rectangle {
    color: "transparent"
    border.color: "white"
    border.width: 0
    width: 400
    height: keyText.contentHeight + valueText.height + distance

    property var key: ""
    property var value: ""

    property var distance: 6
    property alias keyText: keyText
    property alias valueText: valueText

    Custom.FontText {
        id: keyText
        text: parent.key
        width: parent.width
        color: ui.colors.white
        opacity: 0.5
        font.pixelSize: 14
        font.weight: Font.Light
        wrapMode: Text.WordWrap
        horizontalAlignment: Text.AlignLeft
        anchors {
            top: parent.top
            left: parent.left
        }
    }

    Custom.TextArea {
        id: valueText
        width: parent.width
        control.text: parent.value
        placeHolderText: ""
        anchors {
            top: keyText.bottom
            topMargin: distance
            left: parent.left
        }
    }
}
