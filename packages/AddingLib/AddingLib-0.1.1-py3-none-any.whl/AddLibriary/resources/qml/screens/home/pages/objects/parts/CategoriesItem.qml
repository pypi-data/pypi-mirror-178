import QtQuick 2.12
import QtQuick.Controls 2.13
import QtGraphicalEffects 1.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/911/" as Custom


Custom.RoundedRect {
    id: categoriesItem
    radius: 8
    color: selected ? ui.colors.black : ui.colors.dark1

    property var mode: ""
    property var text: ""
    property var count: 0
    property var selected: false
    property var attention: false

    property var lWidth: parent.width
    property var lHeight: 40

    property var tCorner: false
    property var bCorner: false

    property alias mouseArea: mouseArea

    Layout.alignment: Qt.AlignTop

    topRightCorner: tCorner
    bottomRightCorner: bCorner

    Item {
        width: 24
        height: parent.height
        visible: parent.selected

        Custom.Triangle {
            rotation: -90
            scale: 0.9
            opacity: 0.9
            colorTriangle: ui.colors.green1
            anchors.centerIn: parent
        }
    }

    Custom.FontText {
        text: parent.text
        visible: parent.text != ""
        width: parent.width - 80
        height: parent.height
        color: ui.colors.light3
        font.pixelSize: 14
        font.weight: Font.Light
        wrapMode: Text.WordWrap
        horizontalAlignment: Text.AlignLeft
        verticalAlignment: Text.AlignVCenter
        anchors {
            left: parent.left
            leftMargin: 24
            verticalCenter: parent.verticalCenter
        }
    }

    Custom.FontText {
        text: parent.count
        visible: parent.text != ""
        width: 40
        height: parent.height
        color: parent.attention ? ui.colors.red1 : ui.colors.white
        font.pixelSize: 14
        font.weight: Font.Light
        wrapMode: Text.WordWrap
        horizontalAlignment: Text.AlignRight
        verticalAlignment: Text.AlignVCenter
        anchors {
            right: parent.right
            rightMargin: 16
            verticalCenter: parent.verticalCenter
        }
    }

    Component.onCompleted: {
        if (lWidth) {
            categoriesItem.Layout.minimumWidth = Qt.binding(function() {
                return categoriesItem.lWidth
            })
            categoriesItem.Layout.maximumWidth = Qt.binding(function() {
                return categoriesItem.lWidth
            })
        }

        if (lHeight) {
            categoriesItem.Layout.minimumHeight = Qt.binding(function() {
                return categoriesItem.lHeight
            })
            categoriesItem.Layout.maximumHeight = Qt.binding(function() {
                return categoriesItem.lHeight
            })
        }
    }

    Custom.HandMouseArea {
        id: mouseArea
        enabled: parent.text != "" && !parent.selected
        cursorShape: enabled ? Qt.PointingHandCursor : Qt.ArrowCursor

        onClicked: {
            objectsSidebar.reloadModel()
        }
    }
}