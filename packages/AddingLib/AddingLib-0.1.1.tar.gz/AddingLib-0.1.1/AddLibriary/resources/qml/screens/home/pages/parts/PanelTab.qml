import QtQuick 2.12
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/911/" as Custom

Item {
    id: panelTab
    property var text: ""
    property var color: ui.colors.black
    property var defaultColor: "transparent"
    property var selected: false

    Layout.minimumHeight: 36
    Layout.maximumHeight: 36
    Layout.minimumWidth: tabText.contentWidth + 24
    Layout.alignment: Qt.AlignBottom | Qt.AlignLeft

    Rectangle {
        width: tabText.contentWidth + 36
        height: parent.height
        radius: parent.height / 2
        color: panelTab.selected ? panelTab.color : panelTab.defaultColor

        Custom.FontText {
            id: tabText
            text: panelTab.text
            color: ui.colors.white
            opacity: 0.6
            font.pixelSize: 14
            anchors.centerIn: parent
        }
    }
}