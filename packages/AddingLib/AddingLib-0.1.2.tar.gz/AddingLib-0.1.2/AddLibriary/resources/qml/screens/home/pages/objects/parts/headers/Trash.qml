import QtQuick 2.12
import QtQuick.Controls 2.13
import QtGraphicalEffects 1.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/qml/screens/home/pages/events/parts"
import "qrc:/resources/qml/screens/home/pages/objects/parts"


Item {
    id: topLevel
    width: stableWidth + endCell.Layout.maximumWidth
    height: 32
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
        color: objectsStack.color
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

            HeaderCell {
                text: ""
                Layout.preferredWidth: 48
            }

            TableDivider {}

            HeaderCell {
                text: tr.number
                Layout.preferredWidth: 104
            }

            TableDivider {}

            HeaderCell {
                text: tr.object_name
                Layout.preferredWidth: 256
            }

            TableDivider {}

            HeaderCell {
                text: tr.address
                Layout.preferredWidth: 292
            }

            TableDivider {}

            HeaderCell {
                text: tr.a911_hub_id
                Layout.preferredWidth: 120
            }

            TableDivider {}

            HeaderCell {
                id: endCell
                text: tr.deleting_after
                Layout.maximumWidth: {
                    if (objectsBody.width - topLevel.stableWidth < 152) return 152
                    return objectsBody.width - topLevel.stableWidth
                }
                Layout.minimumWidth: Layout.maximumWidth
            }
        }
    }
}