import QtQuick 2.12
import QtQuick.Controls 2.13
import QtGraphicalEffects 1.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/qml/screens/home/sidebar/"


Item {
    id: companySidebar

    ColumnLayout {
        anchors.fill: parent
        spacing: 1

        Rectangle {
            color: ui.colors.dark3
            Layout.alignment: Qt.AlignTop
            Layout.minimumWidth: parent.width
            Layout.minimumHeight: 64
            Layout.maximumHeight: 64
        }

        Rectangle {
            Layout.alignment: Qt.AlignTop
            Layout.minimumWidth: parent.width
            Layout.minimumHeight: 56
            Layout.maximumHeight: 56
            visible: companyAccess.COMPANY_GENERAL_INFO
            enabled: visible
            color: companyStack.currentIndex == 0 ? companyStack.color : ui.colors.dark1

            SidebarItem {
                anchors.fill: parent
                index: 0
                text: tr.a911_general_info
                selected: companyStack.currentIndex == 0
                fontSize: 16
                fillRect.visible: false
                imageItem.sourceSize.width: 40
                imageItem.sourceSize.height: 40
                sourceIcon: "qrc:/resources/images/icons/company-info.svg"

                selectArea.onClicked: {
                    application.debug("company -> company info -> general info")
                    companyStack.currentIndex = 0

                    if (companyStack.companyEditMode) return
                    app.company_module.get_user_company()
                }
            }
        }

        Rectangle {
            color: companyStack.currentIndex == 1 ? companyStack.color : ui.colors.dark1
            Layout.alignment: Qt.AlignTop
            Layout.minimumWidth: parent.width
            Layout.minimumHeight: 56
            Layout.maximumHeight: 56
            visible: companyAccess.COMPANY_SERVICES_SETTINGS

            SidebarItem {
                anchors.fill: parent
                index: 1
                text: tr.services_settings
                selected: companyStack.currentIndex == 1
                fontSize: 16
                fillRect.visible: false
                imageItem.sourceSize.width: 24
                imageItem.sourceSize.height: 24
                sourceIcon: "qrc:/resources/images/icons/company.svg"

                selectArea.onClicked: {
                    application.debug("company -> company info -> functional settings")
                    companyStack.currentIndex = 1

                    if (companyAccess.COMPANY_SERVICES_SETTINGS) {
                        app.company_module.get_company_settings()
                    }
                    if (companyAccess.COMPANY_GENERAL_INFO_EDIT) {
                        app.company_module.get_media_policy_settings()
                    }
                }
            }
        }

        Rectangle {
            id: accessRightsTab

            color: companyStack.currentIndex == 2 ? companyStack.color : ui.colors.dark1

            visible: ((__phod_company_features__ && companyAccess.EMPLOYEE_ROLES_ACCESS_RIGHTS)
                || (__maintenance_report_features__ && companyAccess.MAINTENANCE_REPORT_TOGGLE))

            Layout.alignment: Qt.AlignTop
            Layout.minimumWidth: parent.width
            Layout.minimumHeight: 56
            Layout.maximumHeight: 56

            property var loaded: false

            SidebarItem {
                anchors.fill: parent
                index: 2
                text: tr.employees_access_rights_title
                selected: companyStack.currentIndex == 2
                fontSize: 16
                fillRect.visible: false
                imageItem.sourceSize.width: 24
                imageItem.sourceSize.height: 24
                sourceIcon: "qrc:/resources/images/icons/IconUserRole.svg"

                selectArea.onClicked: {
                    application.debug("company -> company info -> access rights")

                    companyStack.currentIndex = 2

//                    if (!workplacesTab.loaded) {
//                        workplacesTab.loaded = true
//                        app.workplaces_module.get_workplaces()
//                    }
                }
            }
        }

        Rectangle {
            color: companyStack.currentIndex == 3 ? companyStack.color : ui.colors.dark1
            Layout.alignment: Qt.AlignTop
            Layout.minimumWidth: parent.width
            Layout.minimumHeight: 56
            Layout.maximumHeight: 56
            visible: companyAccess.COMPANY_EMPLOYEES

            SidebarItem {
                anchors.fill: parent
                index: 3
                text: tr.a911_emploees
                selected: companyStack.currentIndex == 3
                fontSize: 16
                fillRect.visible: false
                imageItem.sourceSize.width: 40
                imageItem.sourceSize.height: 40
                sourceIcon: "qrc:/resources/images/icons/workers-icon.svg"

                selectArea.onClicked: {
                    application.debug("company -> company info -> employees")
                    companyStack.currentIndex = 3

                    if (companyAccess.COMPANY_SERVICES_SETTINGS) {
                        app.company_module.get_company_settings()
                    }
                }
            }
        }


        Rectangle {
            id: workplacesTab
            color: companyStack.currentIndex == 4 ? companyStack.color : ui.colors.dark1
            Layout.alignment: Qt.AlignTop
            Layout.minimumWidth: parent.width
            Layout.minimumHeight: 56
            Layout.maximumHeight: 56
            visible: companyAccess.COMPANY_WORKPLACES

            property var loaded: false

            SidebarItem {
                anchors.fill: parent
                index: 4
                text: tr.workplaces_911_menu
                selected: companyStack.currentIndex == 4
                fontSize: 16
                fillRect.visible: false
                imageItem.sourceSize.width: 24
                imageItem.sourceSize.height: 24
                sourceIcon: "qrc:/resources/images/icons/monitor.svg"

                selectArea.onClicked: {
                    application.debug("company -> company info -> workplaces")
                    companyStack.currentIndex = 4

                    if (!workplacesTab.loaded) {
                        workplacesTab.loaded = true
                        app.workplaces_module.get_workplaces()
                    }
                }
            }
        }

        Rectangle {
            color: companyStack.currentIndex == 5 ? companyStack.color : ui.colors.dark1
            Layout.alignment: Qt.AlignTop
            Layout.minimumWidth: parent.width
            Layout.minimumHeight: 56
            Layout.maximumHeight: 56
            visible: companyAccess.COMPANY_RRU

            SidebarItem {
                anchors.fill: parent
                index: 5
                text: tr.a911_gbr
                selected: companyStack.currentIndex == 5
                fontSize: 16
                fillRect.visible: false
                imageItem.sourceSize.width: 40
                imageItem.sourceSize.height: 40
                sourceIcon: "qrc:/resources/images/icons/gbr.svg"

                selectArea.onClicked: {
                    application.debug("company -> company info -> rru")
                    companyStack.currentIndex = 5
                }
            }
        }

        Rectangle {
            color: companyStack.currentIndex == 6 ? companyStack.color : ui.colors.dark1
            Layout.alignment: Qt.AlignTop
            Layout.minimumWidth: parent.width
            Layout.minimumHeight: 56
            Layout.maximumHeight: 56
            visible: companyAccess.COMPANY_HUBS

            property var loaded: false

            SidebarItem {
                anchors.fill: parent
                index: 6
                text: tr.connections_tab_911
                selected: companyStack.currentIndex == 6
                fontSize: 16
                fillRect.visible: false
                imageItem.sourceSize.width: 40
                imageItem.sourceSize.height: 40
                sourceIcon: "qrc:/resources/images/icons/company-add-40.svg"

                selectArea.onClicked: {
                    application.debug("company -> company info -> bindings")
                    companyStack.currentIndex = 6

                    if (!parent.loaded) {
                        app.bindings_module.get_hub_company_bindings(true)
                        parent.loaded = true
                    }
                }

                onVisibleChanged: {
                    if (companyStack.firstVisibleIndex == index && visible && !parent.loaded) {
                        app.bindings_module.get_hub_company_bindings(true)
                        parent.loaded = true
                    }
                }
            }
        }

        Rectangle {
            color: ui.colors.dark3
            Layout.alignment: Qt.AlignBottom
            Layout.fillHeight: true
            Layout.minimumWidth: parent.width
        }
    }
}