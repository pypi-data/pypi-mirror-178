import QtQuick 2.12
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/911/" as Custom


Item {
    id: divider
    Layout.fillHeight: true
    Layout.minimumWidth: 4
    Layout.maximumWidth: 4

    property var isHeader: true

    property var leftItem: null
    property var rightItem: null

    Component.onCompleted: {
        if (!isHeader) return
        // indexOf doesn`t exist
        for (var i = 0; i < headerRow.children.length; i++ ) {
            if (headerRow.children[i] == divider) {
                leftItem = headerRow.children[i - 1]
                rightItem = headerRow.children[i + 1]
            }
        }
    }

    Rectangle {
        width: 1
        height: parent.height - 12
        color:  ui.colors.dark1
        visible: divider.isHeader
        anchors.centerIn: parent
    }

    Custom.HandMouseArea {
        id: dividerArea
        enabled: divider.isHeader
        preventStealing: true
        propagateComposedEvents: true
        cursorShape: divider.isHeader ? Qt.SizeHorCursor : Qt.ArrowCursor

        onPositionChanged: {
            if (!pressed) return

            if (leftItem.Layout.preferredWidth + mouseX < leftItem.Layout.minimumWidth) return
            leftItem.Layout.preferredWidth += mouseX
        }
    }
}