import QtQuick 2.12
import QtQuick.Controls 2.13
import QtGraphicalEffects 1.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/screens/home/pages/events/parts"

Rectangle {
    id: topLevel
    width: stableWidth + additionalCell.Layout.maximumWidth
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
                Layout.minimumWidth: 0
                Layout.maximumWidth: 0
            }

            HeaderCell {
                text: tr.a911_employee_name
                Layout.preferredWidth: installersBody.width * 0.3
            }

            TableDivider {}

            HeaderCell {
                text: tr.a911_mail
                Layout.preferredWidth: installersBody.width * 0.3
            }

            TableDivider {}

            HeaderCell {
                text: tr.permissions
                Layout.preferredWidth: installersBody.width * 0.3
            }

            TableDivider {}

            HeaderCell {
                id: additionalCell
                text: ""
                Layout.maximumWidth: {
                    if (installersBody.width - topLevel.stableWidth < 72) return 72
                    return installersBody.width - topLevel.stableWidth
                }
                Layout.minimumWidth: Layout.maximumWidth
            }
        }
    }
}