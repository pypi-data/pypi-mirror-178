import QtQuick 2.12
import QtQuick.Controls 2.13
import QtGraphicalEffects 1.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/screens/home/pages/events/parts"

Rectangle {
    id: topLevel
    width: stableWidth + sourceCell.Layout.maximumWidth
    height: 34
    z: 3
    color: objectsStack.color

    property var stableWidth: {
        var s = 0
        for (var i = 0; i < headerRow.children.length - 1; i++ ) {
            s += headerRow.children[i].width
        }
        return s
    }

    property alias headerRow: headerRow

    Rectangle {
        width: parent.width
        height: parent.height - 1
        color: ui.colors.dark2
        anchors.top: parent.top

        RowLayout {
            id: headerRow
            spacing: 0
            height: parent.height

            Item {
                Layout.fillHeight: true
                Layout.minimumWidth: 16
                Layout.maximumWidth: 16
            }

            HeaderCell {
                text: tr.time_monitoring
                Layout.preferredWidth: 120
            }

            TableDivider {}

            HeaderCell {
                text: tr.a911_event
                Layout.preferredWidth: 600
            }

            TableDivider {}

            HeaderCell {
                id: sourceCell
                text: tr.source_monitoring
                Layout.maximumWidth: {
                    if (eventsBody.width - topLevel.stableWidth < 192) return 192
                    return eventsBody.width - topLevel.stableWidth
                }
                Layout.minimumWidth: Layout.maximumWidth
            }
        }
    }
}