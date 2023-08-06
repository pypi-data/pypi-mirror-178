import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/" as Custom


Rectangle {
    color: "transparent"
    border.color: "white"
    border.width: 0
    width: 200
    height: keyText.contentHeight + valueText.height + distance

    property var key: ""
    property var value: ""

    property var distance: 6
    property alias keyText: keyText
    property alias valueText: valueText
//    property alias copyItem: copyItem

    /* ---------------------------------------------------- */
    /* desktop tests */
    property var accessibleKeyName: ""
    property var accessibleKeyDescription: ""

    property var accessibleValueName: ""
    property var accessibleValueDescription: ""
    /* ---------------------------------------------------- */

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

        /* ---------------------------------------------------- */
        /* desktop tests */
        Accessible.name: accessibleKeyName
        Accessible.description: accessibleKeyDescription
        Accessible.role: Accessible.Paragraph
        /* ---------------------------------------------------- */
    }

    Custom.FontText {
        id: valueText
        text: parent.value
        width: parent.width
        color: ui.colors.white
        font.pixelSize: 16
        font.weight: Font.Light
        wrapMode: Text.WordWrap
        horizontalAlignment: Text.AlignLeft
        anchors {
            top: keyText.bottom
            topMargin: distance
            left: parent.left
        }

        /* ---------------------------------------------------- */
        /* desktop tests */
        Accessible.name: accessibleValueName
        Accessible.description: accessibleValueDescription
        Accessible.role: Accessible.Paragraph
        /* ---------------------------------------------------- */
    }
//
//    MouseArea {
//       id: mouse
//       hoverEnabled: true
//       anchors.fill: parent
//    }

//    CopyItem {
//        id: copyItem
//    }
}