import QtQuick 2.12
import QtQuick.Controls 2.13
import QtGraphicalEffects 1.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/911/" as Custom


Item {
    id: topLevel
    width: stableWidth + addressCell.Layout.maximumWidth
    height: 34
    z: 3

    property var stableWidth: {
        var s = 0;
        for (var i = 0; i < headerRow.children.length - 1; i++ ) {
            s += headerRow.children[i].width
        }
        return s
    }

    property alias headerRow: headerRow

    Rectangle {
        width: parent.width
        height: 1
        color: eventsStack.color
        anchors.bottom: parent.bottom
    }

    Rectangle {
        width: parent.width
        height: parent.height - 1
        color:  ui.colors.dark2
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
                text: tr.a911_time
                Layout.preferredWidth: 80
            }

            TableDivider {}

            HeaderCell {
                text: tr.a911_hub_id
                Layout.preferredWidth: 80
            }

            TableDivider {}

            HeaderCell {
                text: tr.object_number
                Layout.preferredWidth: 80
            }

            TableDivider {}

            HeaderCell {
                text: tr.a911_title
                Layout.preferredWidth: 120
            }

            TableDivider {}

            HeaderCell {
                text: tr.a911_event
                Layout.preferredWidth: 350
                // 130 is extra width for better display
                Layout.minimumWidth:  130 + children[0].contentWidth
            }

            TableDivider {}

//            HeaderCell {
//                text: tr.source_monitoring
//                Layout.preferredWidth: 90
//            }
//
//            TableDivider {}

            HeaderCell {
                id: addressCell
                text: tr.address
//                Layout.fillWidth: true
//                Layout.preferredWidth: 240
                Layout.maximumWidth: {
                    if (eventsBody.width - topLevel.stableWidth < 192) return 192
                    return eventsBody.width - topLevel.stableWidth
                }
                Layout.minimumWidth: Layout.maximumWidth
            }
        }
    }
}