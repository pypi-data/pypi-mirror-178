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
        color: ui.colors.black
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
                Layout.minimumWidth: 0
                Layout.maximumWidth: 0
            }

            HeaderCell {
                text: tr.name
                Layout.preferredWidth: staffBody.width * 0.3
            }

            TableDivider {}

            HeaderCell {
                text: tr.a911_role
                Layout.preferredWidth: staffBody.width * 0.14
            }

            TableDivider {}

            HeaderCell {
                text: tr.phone
                Layout.preferredWidth: staffBody.width * 0.18
            }

            TableDivider {}

            HeaderCell {
                text: tr.a911_mail
                Layout.preferredWidth: staffBody.width * 0.18
            }

            TableDivider {}

            HeaderCell {
                id: accessCell
                text: tr.access_table_911
                Layout.maximumWidth: {
                    if (staffBody.width - topLevel.stableWidth < 81) return 81
                    return staffBody.width - topLevel.stableWidth
                }
                Layout.minimumWidth: Layout.maximumWidth
                Layout.alignment: Qt.AlignRight
            }
        }
    }
}