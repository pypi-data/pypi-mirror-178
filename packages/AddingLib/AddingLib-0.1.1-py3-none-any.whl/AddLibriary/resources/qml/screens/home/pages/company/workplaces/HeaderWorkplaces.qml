import QtQuick 2.12
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/qml/screens/home/pages/events/parts/"


Item {
    id: topLevel
    width: stableWidth + additionalCell.Layout.maximumWidth
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
                text: tr.a911_operator
                Layout.preferredWidth: workplacesListTopLevel.width * 0.25
            }

            TableDivider {}

            HeaderCell {
                text: tr.machine_id
                Layout.preferredWidth: workplacesListTopLevel.width * 0.2
            }

            TableDivider {}

            HeaderCell {
                text: tr.workplaces_911_popup
                Layout.preferredWidth: workplacesListTopLevel.width * 0.2
            }

            TableDivider {}

            HeaderCell {
                text: tr.a911_status
                Layout.preferredWidth: workplacesListTopLevel.width * 0.12
            }

            TableDivider {}

            HeaderCell {
                id: additionalCell
                text: appCompany.filtered_workplaces_model.verification_filter == "UNVERIFIED" ? tr.add : ""
                Layout.maximumWidth: {
                    if (workplacesListTopLevel.width - topLevel.stableWidth < 72) return 72
                    return workplacesListTopLevel.width - topLevel.stableWidth
                }
                Layout.minimumWidth: Layout.maximumWidth
            }
        }
    }
}

