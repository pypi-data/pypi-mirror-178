import QtQuick 2.12
import QtQuick.Controls 2.13
import QtGraphicalEffects 1.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/screens/home/sidebar/"

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

    function openCompany() {
        companySidebarItem.selectArea.clicked(null)
    }

    MouseArea {
        anchors.fill: parent
    }

    ColumnLayout {
        width: parent.width
        spacing: 2

        SidebarItem {
            Layout.fillWidth: true
            height: 64
            index: 0
            text: tr.a911_monitoring
            sourceIcon: "qrc:/resources/images/icons/monitor.svg"
            visible: companyAccess.MONITORING

            selectArea.onClicked: {
                application.debug("company -> sidebar -> monitoring")
                header.currentState = index
                header.sidebarVisible = false
            }
        }

        SidebarItem {
            Layout.fillWidth: true
            height: 64
            index: 1
            text: tr.a911_list
            property var loaded: false
            sourceIcon: "qrc:/resources/images/icons/book.svg"
            visible: companyAccess.JOURNAL

            Component.onCompleted: {
                if (index == header.currentState) {
                    selectArea.clicked(true)
                }
            }

            selectArea.onClicked: {
                application.debug("company -> sidebar -> journal")
                if (!loaded) {
                    loaded = true
                    app.journal_module.get_log_entries_count()
                    // app.get_log_entries()
                }

                header.currentState = index
                header.sidebarVisible = false
            }
        }

        SidebarItem {
            id: categoriesSidebarItem
            Layout.fillWidth: true
            height: 64
            index: 2
            text: tr.a911_objects
            property var loaded: false
            sourceIcon: "qrc:/resources/images/icons/stack.svg"
            visible: companyAccess.OBJECTS

            Component.onCompleted: {
                if (index == header.currentState) {
                    selectArea.clicked(true)
                }
            }

            selectArea.onClicked: {
                application.debug("company -> sidebar -> facilities")
                if (!loaded) {
                    loaded = true
                }

                app.company_module.get_company_settings()

                header.currentState = index
                header.sidebarVisible = false
            }

            Connections {
                target: app

                onChangeScreen: {
                    categoriesSidebarItem.loaded = true
                    header.currentState = 2
                    header.sidebarVisible = false
                }

                onFacilityNotReceived: {
                    if (index == -5) {
                        if (header.currentState == 2) {
                            objectsStack.objectsSidebar.reloadModel()
                        } else {
                            categoriesSidebarItem.loaded = false
                        }
                    }
                }
            }
        }

        SidebarItem {
            id: companySidebarItem

            Layout.fillWidth: true
            height: 64
            index: 3
            text: tr.a911_company
            property var loaded: false
            visible: companyAccess.COMPANY

            sourceIcon: "qrc:/resources/images/icons/company.svg"

            Component.onCompleted: {
                if (index == header.currentState) {
                    selectArea.clicked(true)
                }
            }

            selectArea.onClicked: {
                application.debug("company -> sidebar -> company info")
                if (!loaded) {
                    loaded = true
                    app.fast_response_team_module.start_staff_gbr_stream()
                }

                header.currentState = index
                header.sidebarVisible = false
            }
        }
    }
}