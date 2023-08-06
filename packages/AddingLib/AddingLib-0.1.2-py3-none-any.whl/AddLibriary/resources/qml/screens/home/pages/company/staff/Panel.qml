import QtQuick 2.12
import QtQuick.Controls 2.13
import QtGraphicalEffects 1.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/qml/screens/home/pages/parts/"
import "qrc:/resources/qml/screens/popups/user_settings"
import "qrc:/resources/js/popups.js" as Popups


Rectangle {
    color: ui.colors.dark3
    Layout.alignment: Qt.AlignTop | Qt.AlignLeft
    Layout.fillWidth: true
    Layout.minimumHeight: 112
    Layout.maximumHeight: 112
    Layout.rightMargin: infoStaffComponent.visible ? 0 : 8

    clip: true

    RowLayout {
        spacing: 24
        width: parent.width - 48
        height: 48
        anchors {
            top: parent.top
            topMargin: 8
            horizontalCenter: parent.horizontalCenter
        }

        Item {
            id: searchItem
            Layout.fillWidth: true
            Layout.minimumHeight: parent.height
            Layout.maximumHeight: parent.height

            Custom.SearchField {
                width: parent.width - 8
                height: 38
                anchors.centerIn: parent
                placeHolderText: tr.a911_search_via_emploee

                onSearchStarted: {
                    appCompany.filtered_employees_model.set_filter_text(data)
                }
            }
        }

        Item {
            id: addItem
            visible: Object.keys(roles.uiRoles).some((role) => companyAccessAPI.canEditEmployee(JSON.stringify([role])))
            Layout.alignment: Qt.AlignTop | Qt.AlignRight
            Layout.minimumHeight: parent.height
            Layout.minimumWidth: 220
            Layout.maximumHeight: parent.height
            Layout.maximumWidth: 220

            Roles {
                id: roles

                property var currentObject: null

                visible: false
            }

            Item {
                anchors.fill: parent

                Custom.Button {
                    width: parent.width
                    text: tr.a911_add_empoyee
                    transparent: true
                    color: ui.colors.green1
                    anchors.centerIn: parent

                    onClicked: {
                        application.debug("company -> company info -> employees -> add employee")
                        Popups.add_employee_popup()
                    }
                }
            }
        }
    }

    RowLayout {
        id: tabRow
        spacing: 6
        height: 42

        anchors {
            bottom: parent.bottom
            bottomMargin: 6
            left: parent.left
            leftMargin: 24
        }

        property var installationEnabled: appCompany.data.provided_services.installation

        onInstallationEnabledChanged: {
            if (installersTab.selected) {
                tabRow.currentTab = allTab
                appCompany.filtered_employees_model.set_filter_role(["OWNER", "SENIOR_CMS_ENGINEER", "CMS_ENGINEER", "HEAD_OF_INSTALLERS", "INSTALLER", "HEAD_OF_OPERATORS", "OPERATOR"])
            }
        }

        property var currentTab: allTab

        PanelTab {
            id: allTab
            text: tr.scenario_trigger_all
            selected: tabRow.currentTab == allTab

            Custom.HandMouseArea {
                anchors.fill: parent
                onClicked: {
                    tabRow.currentTab = allTab
                    appCompany.filtered_employees_model.set_filter_role(["OWNER", "SENIOR_CMS_ENGINEER", "CMS_ENGINEER", "HEAD_OF_INSTALLERS", "INSTALLER", "HEAD_OF_OPERATORS", "OPERATOR"])
                }
            }
        }

        PanelTab {
            id: adminTab
            text: tr.owner_911
            selected: tabRow.currentTab == adminTab
            visible: appUser.role.includes("OWNER")

            Custom.HandMouseArea {
                anchors.fill: parent
                onClicked: {
                    tabRow.currentTab = adminTab
                    appCompany.filtered_employees_model.set_filter_role(["OWNER"])
                }
            }
        }

        PanelTab {
            id: engTab
            text: tr.a911_ingeneers
            selected: tabRow.currentTab == engTab
            visible: ["MIX", "MONITORING"].includes(appCompany.company_type) && (
                appUser.role.includes("CMS_ENGINEER") || companyAccessAPI.canEditEmployee(
                    JSON.stringify(["CMS_ENGINEER"])
                )
            )

            Custom.HandMouseArea {
                anchors.fill: parent
                onClicked: {
                    tabRow.currentTab = engTab
                    appCompany.filtered_employees_model.set_filter_role(["SENIOR_CMS_ENGINEER", "CMS_ENGINEER"])
                }
            }
        }

        PanelTab {
            id: installersTab
            text: tr.installers
            selected: tabRow.currentTab == installersTab

            visible: appCompany.data.provided_services.installation && (
                appUser.role.includes("INSTALLER") || companyAccessAPI.canEditEmployee(
                    JSON.stringify(["INSTALLER"])
                )
            )

            Custom.HandMouseArea {
                anchors.fill: parent
                onClicked: {
                    tabRow.currentTab = installersTab
                    appCompany.filtered_employees_model.set_filter_role(["HEAD_OF_INSTALLERS", "INSTALLER"])
                }
            }
        }

        PanelTab {
            id: operTab
            text: tr.a911_operators
            visible: ["MIX", "MONITORING"].includes(appCompany.company_type) && (
                appUser.role.includes("OPERATOR") || companyAccessAPI.canEditEmployee(
                    JSON.stringify(["OPERATOR"])
                )
            )
            selected: tabRow.currentTab == operTab

            Custom.HandMouseArea {
                anchors.fill: parent
                onClicked: {
                    tabRow.currentTab = operTab
                    appCompany.filtered_employees_model.set_filter_role(["HEAD_OF_OPERATORS", "OPERATOR"])
                }
            }
        }

        /*
        PanelTab {
            id: gbrTab
            text: tr.a911_gbr
            selected: tabRow.currentTab == gbrTab

            Custom.HandMouseArea {
                anchors.fill: parent
                onClicked: {
                    tabRow.currentTab = gbrTab
                    appCompany.filtered_employees_model.set_filter_role(["RAPID_RESPONSE_TEAM"])
                }
            }
        }

        PanelTab {
            id: seniorEngTab
            text: tr.a911_Senior_monitoring_station_engineer
            selected: tabRow.currentTab == seniorEngTab

            Custom.HandMouseArea {
                anchors.fill: parent
                onClicked: {
                    tabRow.currentTab = seniorEngTab
                    appCompany.filtered_employees_model.set_filter_role(["SENIOR_CMS_ENGINEER"])
                }
            }
        }

        PanelTab {
            id: engTab
            text: tr.a911_ingeneers
            selected: tabRow.currentTab == engTab

            Custom.HandMouseArea {
                anchors.fill: parent
                onClicked: {
                    tabRow.currentTab = engTab
                    appCompany.filtered_employees_model.set_filter_role(["CMS_ENGINEER"])
                }
            }
        }

        PanelTab {
            id: installersTab
            text: tr.installers
            selected: tabRow.currentTab == installersTab

            Custom.HandMouseArea {
                anchors.fill: parent
                onClicked: {
                    tabRow.currentTab = installersTab
                    appCompany.filtered_employees_model.set_filter_role(["INSTALLER", "HEAD_OF_INSTALLERS"])
                }
            }
        }
        */
    }
}
