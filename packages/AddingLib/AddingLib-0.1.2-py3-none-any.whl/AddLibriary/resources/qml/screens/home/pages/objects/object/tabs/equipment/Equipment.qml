import QtQuick 2.12
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/" as Root
import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/qml/screens/home/pages/parts/"
import "qrc:/resources/qml/screens/home/pages/parts/"
import "qrc:/resources/qml/screens/home/pages/objects/object/managements"
import "qrc:/resources/qml/components/911/DS/components" as DSComponents
import "qrc:/resources/qml/components/911/DS3/" as DS3

import "qrc:/resources/js/desktop/popups.js" as Popups


Rectangle {
    id: equipment

    color: ui.colors.black

    property var rooms: {
        return appCompany.current_facility && appCompany.current_facility.management ? appCompany.current_facility.management.rooms : null
    }
    property var users: {
        return appCompany.current_facility && appCompany.current_facility.management ? appCompany.current_facility.management.users : null
    }
    property var groups: {
        return appCompany.current_facility && appCompany.current_facility.management ? appCompany.current_facility.management.groups : null
    }
    property var management: {
        return appCompany.current_facility && appCompany.current_facility.management ? appCompany.current_facility.management : null
    }
    property var currentTab: "DEVICES"

    readonly property var hubConfigContext: hubPageLoader.contextTarget.hubConfig

    property var rights: appUser.employee_roles_access_rights

    property var providedServices: facility.data.provided_services

    property var mrRights: {
        let availableRoles = []
        let access = []

        if (providedServices.includes("MONITORING") && providedServices.length === 1) {
            availableRoles = ["SENIOR_CMS_ENGINEER", "CMS_ENGINEER", "OWNER"]
        }
        else if (providedServices.includes("INSTALLATION") && providedServices.length === 1) {
            availableRoles = ["INSTALLER","HEAD_OF_INSTALLERS", "OWNER"]
        }
        else availableRoles = ["INSTALLER","HEAD_OF_INSTALLERS", "OWNER", "SENIOR_CMS_ENGINEER", "CMS_ENGINEER"]

        let allUserRoles = new Set(appUser.role)
        let bindingRoles = new Set(availableRoles)

        let resultRoles = new Set(
            [...allUserRoles].filter(role => bindingRoles.has(role))
        )

        resultRoles.forEach((role) => {
            access.push(rights[role].includes("MAINTENANCE_REPORT_MAKE"))
        })

        if (access.some(item => item)) {
            return true
        }
        return false
    }

    Root.ContextLoader {
        // TODO: replace whole page with this loader
        id: hubPageLoader

        contextTarget: appCompany.current_facility && appCompany.current_facility.hub_page || null
    }

    ColumnLayout {
        anchors.fill: parent
        spacing: 1

        Rectangle {
            color: ui.colors.dark3
            Layout.minimumHeight: 48
            Layout.maximumHeight: 48
            Layout.fillWidth: true

            RowLayout {
                id: logsTabPanel
                spacing: 12
                height: 42
                anchors {
                    left: parent.left
                    leftMargin: 8
                    verticalCenter: parent.verticalCenter
                }

                property var indexTabs: 0

                PanelTab {
                    id: groupsTab
                    text: tr.devices
                    selected: currentTab == "DEVICES"
                    Layout.alignment: Qt.AlignLeft

                    Custom.HandMouseArea {
                        onClicked: {
                            currentTab = "DEVICES"
                            logsTabPanel.indexTabs = 0
                        }
                    }
                }

                PanelTab {
                    id: roomsTab
                    text: tr.rooms
                    selected: currentTab == "ROOMS"
                    Layout.alignment: Qt.AlignLeft

                    Custom.HandMouseArea {
                        onClicked: {
                            currentTab = "ROOMS"
                            logsTabPanel.indexTabs = 1
                        }
                    }
                }

                PanelTab {
                    id: deviceTypesTab
                    text: tr.groups_hub_settings
                    selected: currentTab == "GROUPS"
                    Layout.alignment: Qt.AlignLeft

                    Custom.HandMouseArea {
                        onClicked: {
                           currentTab = "GROUPS"
                           logsTabPanel.indexTabs = 2
                        }
                    }
                }
            }

            DSComponents.HubPermissions {
                id: hubPermissions

                visible: companyAccess.OBJECT_EQUIPMENT_ADJUST
                    && management.employee_access_type_to_hub != "EMPLOYEE_ACCESS_TYPE_UNSPECIFIED"
                    && facility.data.provided_services.includes("INSTALLATION")

                anchors {
                    verticalCenter: parent.verticalCenter
                    right: parent.right
                    rightMargin: 16
                }

                endTimestamp: management.facility_expiration_time
                isPermanentAccess: management.employee_access_type_to_hub == "EMPLOYEE_ACCESS_TYPE_PERMANENT"
                    && management.company_permission_type_to_hub == "COMPANY_PERMISSION_TYPE_FULL"
            }

            DS3.ButtonTextRect {
                anchors {
                    verticalCenter: parent.verticalCenter
                    right: hubPermissions.visible ? hubPermissions.left : parent.right
                    rightMargin: 16
                }

                text: tr.maintenance_reports_menu
                visible: {
                    appCompany.workplaces_model.incidents_settings.maintenance_report_settings.report_enabled == "ON"
                    && __maintenance_report_features__
                    && mrRights
                }
                status: DS3.ButtonRect.Status.Secondary
                onClicked: {
                    Popups.popupByPath(
                        "qrc:/resources/qml/screens/home/pages/objects/object/popups/maintenance_report/ArchiveOfObjectReportsPopup.qml"
                    )
                }
            }
        }

        Rectangle {
            id: backgroundRect
            color: ui.colors.black
            Layout.fillWidth: true
            Layout.fillHeight: true
            StackLayout {
                id: stackLayout
                width: parent.width
                height: parent.height
                currentIndex: logsTabPanel.indexTabs

                Devices {}
                Rooms {}
                Groups {}
            }
        }
    }

    Component.onCompleted: {
        app.start_stream_object_hub_changes(facility.hub_id)
    }
}
