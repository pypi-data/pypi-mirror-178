import QtQuick 2.12
import QtQuick.Controls 2.13
import QtGraphicalEffects 1.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/911/" as Custom

Item {
    id: objectsTab
    anchors.fill: parent

    property var name: ""
    property var value: ""
    property var attention: false

    property alias valueText: valueText
    property alias selectArea: selectArea

    Custom.FontText {
        width: parent.width - 80
        height: 20
        text: objectsTab.name
        color: ui.colors.light3
        font.pixelSize: 14
        font.weight: Font.Light
        wrapMode: Text.WordWrap
        horizontalAlignment: Text.AlignLeft
        anchors {
            left: parent.left
            leftMargin: 24
            verticalCenter: parent.verticalCenter
        }
    }

    Custom.FontText {
        id: valueText
        width: 80
        height: 20
        visible: false
        text: objectsTab.value
        color: objectsTab.attention ? ui.colors.red1 : ui.colors.white
        font.pixelSize: 14
        font.weight: Font.Light
        wrapMode: Text.WordWrap
        horizontalAlignment: Text.AlignRight
        anchors {
            right: parent.right
            rightMargin: 24
            verticalCenter: parent.verticalCenter
        }
    }

    Custom.HandMouseArea {
        id: selectArea
    }
}
