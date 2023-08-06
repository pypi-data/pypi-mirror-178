import QtQuick 2.12
import QtQuick.Controls 2.13
import QtGraphicalEffects 1.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/screens/home/sidebar/" as CompanySidebar


Rectangle {
    id: sideBarRect
    color: ui.colors.black
    states: [
        State { when: visible;
            PropertyChanges { target: sideBarRect ; x: 0 }
        },
        State { when: !visible;
            PropertyChanges { target: sideBarRect ; x: -334 }
        }
    ]
    transitions: Transition {
        NumberAnimation { property: "x"; duration: 200; alwaysRunToEnd: true }
        NumberAnimation { property: "visible"; duration: 10; alwaysRunToEnd: true }
    }

    onVisibleChanged: {
        if (visible) {
            z = 1000
            color = ui.colors.black
            return
        }
        if (!visible) {
            z = -1
            color = "transparent"
            return
        }
    }

    MouseArea {
        anchors.fill: parent
    }

    ColumnLayout {
        width: parent.width
        spacing: 2

        CompanySidebar.SidebarItem {
            Layout.fillWidth: true
            height: 64
            index: 0
            text: tr.hubs
            sourceIcon: "qrc:/resources/images/icons/stack.svg"

            selectArea.onClicked: {
                application.debug("pro -> sidebar -> open hubs tab")
                header.currentState = index
                header.sidebarVisible = false
            }
        }

        CompanySidebar.SidebarItem {
            Layout.fillWidth: true
            height: 64
            index: 1
            text: tr.a911_company
            sourceIcon: "qrc:/resources/images/icons/company-add.svg"

            selectArea.onClicked: {
                application.debug("pro -> sidebar -> open company tab")
                header.currentState = index
                header.sidebarVisible = false
            }
        }
    }
}