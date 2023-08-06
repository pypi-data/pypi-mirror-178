import QtQuick 2.12
import QtQuick.Controls 2.13
import QtGraphicalEffects 1.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/qml/screens/home/pages/company/info"
import "qrc:/resources/qml/screens/pro/pages/company/components" as Desktop
import "qrc:/resources/qml/components/911/DS3" as DS3
import "qrc:/resources/js/desktop/popups.js" as Popups


Rectangle {
    id: functionalSettingsRect

    property var roles: {
        'OWNER': tr.owner_911,
        'SENIOR_CMS_ENGINEER': tr.a911_Senior_monitoring_station_engineer,
        'CMS_ENGINEER': tr.a911_monitoring_station_engineer,
        'HEAD_OF_INSTALLERS': tr.a911_head_of_installers,
        'INSTALLER': tr.a911_installer,
        'HEAD_OF_OPERATORS': tr.a911_head_of_operators,
        'OPERATOR': tr.a911_operator
    }

    property var filtered_roles_for_phod: companyAccessAPI.getRolesForComanyAccessEdit()
    property var filtered_roles_for_mr: {
        var availableRoles = companyAccessAPI.getRolesForComanyAccessEdit()
        availableRoles = availableRoles.filter( ( roles ) => !roles.includes( 'OPERATOR', 'HEAD_OF_OPERATORS' ) );

        return availableRoles
    }

    property var rights: appUser.employee_roles_access_rights
    property var currentItem: __phod_company_features__ ?
        filtered_roles_for_phod[0] || "OWNER" :
        filtered_roles_for_mr[0] || "OWNER"
    function updateToggles() {
        if (!!currentItem) {
            takeViewPhodPermission.checked = rights[currentItem].includes('PHOTO_ON_DEMAND_READ_MAKE')
            viewCameraStreamingsPermission.checked = rights[currentItem].includes('CAMERA_STREAMING_READ')
            viewPhotosByAlarmScenarios.checked = rights[currentItem].includes('PHOTOS_BY_ALARM_SCENARIO_READ')
            createMaintenanceReportPermission.checked = rights[currentItem].includes('MAINTENANCE_REPORT_MAKE')
        }
    }

    color: companyStack.color

    Connections {
        target: appUser

        onEmployeeRolesAccessResponse: {
            rights = appUser.employee_roles_access_rights
            updateToggles()
        }
    }

    onCurrentItemChanged: {
        updateToggles()
    }

    Component.onCompleted: {
        updateToggles()
    }

    Rectangle {
        id: accessRights

        anchors.fill: parent

        color: ui.ds3.bg.base

        DS3.ScrollView {
            id: scrollView

            anchors.fill: parent

            padding: 32
            clip: true

            DS3.Text {
                text: tr.employees_access_rights_title
                style: ui.ds3.text.title.LBold
            }

            DS3.Spacing {
                height: 32
            }

            Row {

                width: parent.width

                spacing: 32

                Column {
                    id: roleSelector

                    width: 320

                    Repeater {
                        id: roleItems

                        model: __phod_company_features__ ?
                                functionalSettingsRect.filtered_roles_for_phod :
                                functionalSettingsRect.filtered_roles_for_mr

                        DS3.SettingsContainer {
                            DS3.SettingsNavigationTitlePrimary {
                                title: roles[modelData]
                                color: currentItem == modelData ?
                                    ui.ds3.special.selection :
                                    ui.ds3.figure.transparent
                                onEntered: {
                                    currentItem = modelData
                                }
                            }
                        }
                    }
                }

                Column {
                    id: permissions

                    width: parent.width - roleSelector.width - 32

                    Column {
                        id: companyPhodPermissions

                        width: parent.width

                        function update_permission(permission_name) {
                            var access_rights_list = rights[currentItem]
                            if (access_rights_list.includes(permission_name)) {
                                access_rights_list = access_rights_list.filter(function(e) { return e !== permission_name })
                            }
                            else {
                                access_rights_list.push(permission_name)
                            }
                            var data = {
                                'role': currentItem,
                                'access_rights': access_rights_list,
                            }

                            Popups.please_wait_popup()
                            appUser.set_employee_role_access_rights(data)
                        }

                        visible: __phod_company_features__

                        DS3.TitleSection {
                            text: tr.system
                            isCaps: true
                            forceTextToLeft: true
                            isBgTransparent: true
                        }

                        DS3.SettingsContainer {
                            DS3.SettingsSwitch {
                                id: takeViewPhodPermission

                                title: tr.take_view_phod_permission

                                onSwitched: () => {
                                    companyPhodPermissions.update_permission('PHOTO_ON_DEMAND_READ_MAKE')
                                }
                            }

                            DS3.SettingsSwitch {
                                id: viewCameraStreamingsPermission

                                title: tr.view_camera_streamings_permission

                                onSwitched: () => {
                                    companyPhodPermissions.update_permission('CAMERA_STREAMING_READ')
                                }
                            }

                            DS3.SettingsSwitch {
                                id: viewPhotosByAlarmScenarios

                                title: tr.view_photos_by_alarm_permission

                                onSwitched: () => {
                                    companyPhodPermissions.update_permission('PHOTOS_BY_ALARM_SCENARIO_READ')
                                }
                            }
                        }
                    }

                    Column {
                        id: maintenanceReportsPermission

                        width: parent.width

                        visible: __maintenance_report_features__ && companyAccess.MAINTENANCE_REPORT_TOGGLE

                        DS3.Spacing {
                           height: __phod_company_features__ ? 36 : 0
                        }

                        DS3.TitleSection {
                            text: tr.service_title
                            isCaps: true
                            forceTextToLeft: true
                            isBgTransparent: true
                        }

                        DS3.SettingsContainer {
                            DS3.SettingsSwitch {
                                id: createMaintenanceReportPermission

                                title: tr.create_maintenance_reports_permission

                                onSwitched: () => {
                                    companyPhodPermissions.update_permission('MAINTENANCE_REPORT_MAKE')
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}