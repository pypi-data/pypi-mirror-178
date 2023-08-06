import QtQuick 2.12
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/qml/screens/home/pages/parts/"
import "qrc:/resources/qml/screens/home/pages/objects/parts/"


Rectangle {
    id: control

//    width: parent.width / 3
//    height: parent.height
    color: "transparent"

    ColumnLayout {
        id: columnTabs

        anchors.fill: parent
        spacing: 1

        Custom.RoundedRect {
            id: notesTab

            color: currentNotesIndex == 0 ? ui.colors.black : ui.colors.dark1
            radius: 10
            Layout.alignment: Qt.AlignTop
            Layout.fillWidth: true
            Layout.minimumHeight: 48
            Layout.maximumHeight: 48
            bottomRightCorner: currentNotesIndex == 1

            SidebarTab {
                name: tr.a911_notes
                selectArea.onClicked: {
                    currentNotesIndex = 0
                }
            }
        }

        Custom.RoundedRect {
            id: additionallyTab

            color: currentNotesIndex == 1 ? ui.colors.black : ui.colors.dark1
            radius: 10
            Layout.alignment: Qt.AlignTop
            Layout.fillWidth: true
            Layout.minimumHeight: 48
            Layout.maximumHeight: 48
            topRightCorner: currentNotesIndex == 0

            SidebarTab {
                name: tr.a911_additionally
                selectArea.onClicked: {
                    currentNotesIndex = 1
                }
            }
        }

        Custom.RoundedRect {

            color: ui.colors.dark3
            radius: 10
            Layout.alignment: Qt.AlignTop
            Layout.fillWidth: true
            Layout.fillHeight: true
            topRightCorner: currentNotesIndex == 1
        }
    }
}