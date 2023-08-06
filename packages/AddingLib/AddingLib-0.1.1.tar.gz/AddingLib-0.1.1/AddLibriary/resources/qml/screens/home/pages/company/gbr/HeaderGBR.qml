import QtQuick 2.12
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.13
import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/qml/screens/home/pages/events/parts/"


Item {
    id: topLevel
    width: stableWidth + accessCell.Layout.maximumWidth
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
        anchors.bottom: parent.bottom
        color: ui.colors.black
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
                Layout.minimumWidth: 0
                Layout.maximumWidth: 0
            }

            HeaderCell {
                text: tr.a911_pozivnoy
                Layout.preferredWidth: gbrListTopLevel.width * 0.25
            }

            TableDivider {}

            HeaderCell {
                text: tr.phone
                Layout.preferredWidth: gbrListTopLevel.width * 0.18
            }

            TableDivider {}

            HeaderCell {
                text:  tr.a911_transpotr
                Layout.preferredWidth: gbrListTopLevel.width * 0.4
            }

            TableDivider {}

            HeaderCell {
                id: accessCell
                text: tr.access_table_911
                Layout.maximumWidth: {
                    if (gbrListTopLevel.width - topLevel.stableWidth < 78) return 78
                    return gbrListTopLevel.width - topLevel.stableWidth
                }
                Layout.minimumWidth: Layout.maximumWidth
            }
        }
    }
}

