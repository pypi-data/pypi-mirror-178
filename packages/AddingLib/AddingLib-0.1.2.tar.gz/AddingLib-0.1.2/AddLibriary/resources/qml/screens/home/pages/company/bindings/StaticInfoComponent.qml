import QtQuick 2.12
import QtQuick.Controls 2.13
import QtGraphicalEffects 1.13
import QtQuick.Layouts 1.13

import "qrc:/resources/js/popups.js" as Popups
import "qrc:/resources/js/desktop/popups.js" as DesktopPopups
import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/qml/components/911/DS3" as DS3


Rectangle {
    id: bindingInfo

    property bool installation_service_state: !!(currentObject && currentObject.installation_service_state && currentObject.installation_service_state.state == "ACTIVE")
    property bool translator_channel_state: !!(currentObject && currentObject.translator_channel_state && currentObject.translator_channel_state.state == "ACTIVE")
    property bool canInstallationServiceRemove: false

    anchors.fill: parent

    color: ui.ds3.bg.base

    Component.onCompleted: {
        // Check if current installer has access to delete the installation binding on this hub
        if (
            appUser.role.includes("INSTALLER")
            && !appUser.role.includes("HEAD_OF_INSTALLERS")
            && !!currentObject.a911_channel_info.facility_id
        ) {
            app.bindings_module.get_access_rights_facility(currentObject.a911_channel_info.facility_id)
        } else {
            canInstallationServiceRemove = true
        }
    }

    Connections {
        target: app.bindings_module

        onGetAccessRightsFacilitySuccess: (access_type) => {
            canInstallationServiceRemove = access_type != "EXPIRED"
        }

        onScheduleChannel911RemovalIncidentExistsError: DesktopPopups.popupByPath(
            "qrc:/resources/qml/components/911/DS3/popups/Dialog.qml", {
                title: tr.unprocessed_incidents_left_tite,
                text: tr.unprocessed_incidents_left_descr,
                firstButtonText: tr.unprocessed_incidents_left_button,
                firstButtonCallback: () => {
                    app.bindings_module.schedule_channel_911_removal({hub_id: currentObject.hub_id}, true)
                },
                isFirstButtonRed: true,
                firstButtonIsOutline: true,
                secondButtonIsOutline: false,
                secondButtonText: tr.cancel,
                isVertical: true
            }
        )

        onHubCompanyBindingRemovalIncidentExistsError: DesktopPopups.popupByPath(
            "qrc:/resources/qml/components/911/DS3/popups/Dialog.qml", {
                title: tr.unprocessed_incidents_left_tite,
                text: tr.unprocessed_incidents_left_descr,
                firstButtonText: tr.unprocessed_incidents_left_button,
                firstButtonCallback: () => {
                    app.bindings_module.delete_hub_company_binding({hub_id: currentObject.hub_id}, true)
                },
                isFirstButtonRed: true,
                firstButtonIsOutline: true,
                secondButtonIsOutline: false,
                secondButtonText: tr.cancel,
                isVertical: true
            }
        )
    }

    DS3.ScrollView {
        id: scrollView

        width: parent.width

        anchors {
            fill: undefined
            top: parent.top
            bottom: actionButtons.top
        }

        clip: true
        padding: 16

        Column {
            id: columnLayout

            width: parent.width

            anchors.horizontalCenter: parent.horizontalCenter

            spacing: 16
            
            DS3.Spacing {
                height: 24 - columnLayout.spacing
            }

            Column {
                // hub id
                spacing: 8

                DS3.Text {
                    style: ui.ds3.text.body.MRegular
                    text: tr.a911_hub_id
                    color: ui.ds3.figure.nonessential
                }

                DS3.Text {
                    style: ui.ds3.text.title.SBold
                    text: currentObject && currentObject.hub_id ? currentObject.hub_id : ui.empty
                    color: ui.ds3.figure.base
                }
            }
            Column {
                width: parent.width

                // obj name
                spacing: 8

                DS3.Text {
                    style: ui.ds3.text.body.MRegular
                    text: tr.object_name
                    color: ui.ds3.figure.nonessential
                }

                DS3.Text {
                    width: parent.width

                    style: ui.ds3.text.body.LRegular
                    text: currentObject && currentObject.a911_channel_info ? currentObject.a911_channel_info.name : ui.empty
                    color: ui.ds3.figure.base
                }
            }
            Column {
                // object number
                spacing: 8

                DS3.Text {
                    style: ui.ds3.text.body.MRegular
                    text: tr.account_number
                    color: ui.ds3.figure.nonessential
                }

                DS3.Text {
                    style: ui.ds3.text.body.LRegular
                    text: currentObject && currentObject.a911_channel_info && currentObject.a911_channel_info.registration_number ? currentObject.a911_channel_info.registration_number : ui.empty
                    color: ui.ds3.figure.base
                }
            }
            Column {
                // monitoring service status
                id: monitoringStatus

                width: parent.width

                visible: appCompany.company_type != "INSTALLATION"
                spacing: 8
                                      
                DS3.Text {
                    style: ui.ds3.text.body.MRegular
                    color: ui.ds3.figure.nonessential
                    text: tr.a911_binding_status
                }
                Flow {
                    id: monitoringStatusFlow

                    width: parent.width

                    DS3.Text {
                        height: 40

                        style: ui.ds3.text.body.LRegular
                        text: {
                            return {
                                ACTIVE:tr.on_monitoring,
                                NO_MONITORING:tr.no_monitoring_911_hubs,
                                IN_SLEEP_MODE:tr.sleep_mode_objects_911,
                                NO_OBJECT:tr.no_object_911,
                                WAITING_FOR_APPROVAL:tr.monitoring_requested,
                                WAITING_FOR_REMOVAL:tr.binding_status_pending_deletion,
                            }[currentObject.pro_desktop_status_preview.pro_desktop_status]
                        }
                        color:{
                            return {
                                ACTIVE:ui.ds3.figure.positiveContrast,
                                NO_MONITORING:ui.ds3.figure.secondary,
                                IN_SLEEP_MODE:ui.ds3.figure.secondary,
                                NO_OBJECT:ui.ds3.figure.secondary,
                                WAITING_FOR_APPROVAL:ui.ds3.figure.secondary,
                                WAITING_FOR_REMOVAL:ui.ds3.figure.attention,
                            }[currentObject.pro_desktop_status_preview.pro_desktop_status]
                        }
                    }
                    Item {
                        width: monitoringDeleteIcon.visible ? monitoringDeleteIcon.width + 32 : 16
                        height: monitoringDeleteIcon.height

                        DS3.Icon {
                            id: monitoringDeleteIcon

                            anchors.centerIn: parent

                            visible: ["IN_SLEEP_MODE","ACTIVE","WAITING_FOR_REMOVAL"].includes(currentObject.pro_desktop_status_preview.pro_desktop_status)
                                && !!currentObject.hub_id
                            source: {
                                if (!!currentObject.a911_channel_info && !!currentObject.a911_channel_info.active_until)
                                    return {
                                        1: "qrc:resources/images/Athena/common_icons/DaysLeft1.svg",
                                        2: "qrc:resources/images/Athena/common_icons/DaysLeft2.svg",
                                        3: "qrc:resources/images/Athena/common_icons/DaysLeft3.svg",
                                        4: "qrc:resources/images/Athena/common_icons/DaysLeft4.svg",
                                        5: "qrc:resources/images/Athena/common_icons/DaysLeft5.svg",
                                        6: "qrc:resources/images/Athena/common_icons/DaysLeft6.svg",
                                        7: "qrc:resources/images/Athena/common_icons/DaysLeft7.svg",
                                    }[currentObject.a911_channel_info.active_until]
                                return "qrc:/resources/images/Athena/common_icons/DaysLeftNone.svg"
                            }

                            DS3.MouseArea {
                                onClicked: {
                                    if (currentObject.pro_desktop_status_preview.pro_desktop_status == "WAITING_FOR_REMOVAL") {
                                        DesktopPopups.popupByPath(
                                            "qrc:/resources/qml/components/911/DS3/popups/Dialog.qml", {
                                                title: tr.a911_delete_object_permanently,
                                                text: tr.delete_object_permanently_description_911,
                                                firstButtonText: tr.stop_monitoring_button,
                                                firstButtonCallback: () => {
                                                    app.bindings_module.remove_channel_911({hub_id: currentObject.hub_id})
                                                },
                                                isFirstButtonRed: true,
                                                firstButtonIsOutline: true,
                                                secondButtonIsOutline: false,
                                                secondButtonText: tr.cancel,
                                                isVertical: true
                                            }
                                        )
                                    } else {
                                        DesktopPopups.popupByPath(
                                            "qrc:/resources/qml/components/911/DS3/popups/Dialog.qml", {
                                                title: tr.move_object_to_trash_title,
                                                text: tr.move_object_to_trash,
                                                firstButtonText: tr.stop_monitoring_button,
                                                firstButtonCallback: () => {
                                                    app.bindings_module.schedule_channel_911_removal({hub_id: currentObject.hub_id})
                                                },
                                                isFirstButtonRed: true,
                                                firstButtonIsOutline: true,
                                                secondButtonIsOutline: true,
                                                secondButtonText: tr.cancel,
                                                isVertical: true
                                            }
                                        )
                                    }
                                }
                            }
                        }
                    }
                    DS3.Text {
                        height: monitoringStatusFlow.height > 40 ? undefined : 40

                        style: ui.ds3.text.button.MBold
                        text: tr.add
                        color: ui.ds3.figure.interactive
                        visible: currentObject.pro_desktop_status_preview.pro_desktop_status == "WAITING_FOR_APPROVAL" || currentObject.pro_desktop_status_preview.pro_desktop_status == "NO_OBJECT"

                        Custom.HandMouseArea {
                            onClicked: {
                                var settings = {}
                                settings["hub_id"] = currentObject && currentObject.hub_id ? currentObject.hub_id : ""
                                settings["registration_number"] = currentObject && currentObject.a911_channel_info && currentObject.a911_channel_info.registration_number ? currentObject.a911_channel_info.registration_number : ""
                                settings["name"] = currentObject && currentObject.a911_channel_info ? currentObject.a911_channel_info.name : ""
                                settings["facility_id"] = currentObject && currentObject.facility_id ? currentObject.facility_id : ""
                                Popups.create_911_channel_popup(settings, "binding")
                            }
                        }
                    }
                    DS3.Text {
                        height: monitoringStatusFlow.height > 40 ? undefined : 40

                        style: ui.ds3.text.button.MBold
                        text: tr.restore_object
                        color: ui.ds3.figure.interactive
                        visible: currentObject.pro_desktop_status_preview.pro_desktop_status == "WAITING_FOR_REMOVAL" &&
                            companyAccess.NEW_OBJECT_ADD

                        DS3.MouseArea {
                            onClicked: app.bindings_module.cancel_channel_911_removal(currentObject)
                        }
                    }
                }
            }
            Column {
                // installation service status
                visible: appCompany.company_type != "MONITORING"
                spacing: 8

                DS3.Text {
                    style: ui.ds3.text.body.MRegular
                    text: tr.installation_services_911
                    color: ui.ds3.figure.nonessential
                }

                Row {
                    width: parent.width

                    spacing: 16
                    
                    DS3.Text {
                        anchors.verticalCenter: parent.verticalCenter

                        style: ui.ds3.text.body.LRegular
                        text: bindingInfo.installation_service_state ? tr.with_installers_filter : tr.without_installers_filter
                        color: bindingInfo.installation_service_state ? ui.ds3.figure.positiveContrast : ui.ds3.figure.base
                    }

                    DS3.Icon {
                        anchors.verticalCenter: parent.verticalCenter

                        visible: companyAccess.OBJECT_INSTALLATION_DELETE && bindingInfo.installation_service_state
                            && !!currentObject.hub_id && canInstallationServiceRemove
                        source: "qrc:/resources/images/Athena/common_icons/DaysLeftNone.svg"
                        
                        DS3.MouseArea {
                            onClicked: DesktopPopups.popupByPath(
                                "qrc:/resources/qml/components/911/DS3/popups/Dialog.qml", {
                                    title: tr.remove_installer_911_title,
                                    text: tr.remove_installer_911_descr,
                                    firstButtonText: tr.remove_installer_911_button,
                                    firstButtonCallback: () => {
                                        app.bindings_module.disable_installation_service(currentObject.hub_id)
                                    },
                                    isFirstButtonRed: true,
                                    firstButtonIsOutline: true,
                                    secondButtonText: tr.cancel,
                                    isVertical: true
                                }
                            )
                        }
                    }
                }
            }
            Column {
                // translator status
                spacing: 8

                DS3.Text {
                    style: ui.ds3.text.body.MRegular
                    text: tr.translator_binding_status
                    color: ui.ds3.figure.nonessential
                }

                DS3.Text {
                    style: ui.ds3.text.body.LRegular
                    text: bindingInfo.translator_channel_state ? tr.binding_status_active : tr.no_object_911
                    color: bindingInfo.translator_channel_state ? ui.ds3.figure.positiveContrast : ui.ds3.figure.base
                }
            }
        }
    }

    Column {
        id: actionButtons

        width: parent.width - (16 * 2)

        anchors.bottom: parent.bottom
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.bottomMargin: 24

        spacing: 16
        
        Custom.Button {
            width: parent.width

            visible: currentObject.pro_desktop_status_preview.pro_desktop_status != "NO_OBJECT"
                && (currentObject.pro_desktop_status_preview.pro_desktop_status != "NO_MONITORING" || companyAccess.OBJECTS_WITH_INSTALLATION_SERVICE)
                && companyAccess.OBJECTS
            text: tr.to_hub_details_911
            color: ui.ds3.figure.interactive
            transparent: true

            onClicked: {
                if (!currentObject) return

                if (currentObject.a911_channel_info && currentObject.a911_channel_info.facility_id) {
                    if (objectsStack.currentObjectIndex != -4) objectsStack.currentObjectIndex = -4

                    objectsStack.startLoading()
                    app.facility_module.get_facility(currentObject.a911_channel_info.facility_id, -5)
                    return
                }

                var objName = currentObject.a911_channel_info && currentObject.a911_channel_info.name ? currentObject.a911_channel_info.name : ""
                var objNumber = currentObject.a911_channel_info && currentObject.a911_channel_info.registration_number ? currentObject.a911_channel_info.registration_number : ""

                if (currentObject.hub_id) {
                    if (objectsStack.currentObjectIndex != -4) objectsStack.currentObjectIndex = -4

                    objectsStack.startLoading()
                    app.facility_module.get_null_facility(currentObject.hub_id, objName, objNumber, -5, {})
                    return
                }
            }
        }

        Custom.Button {
            width: parent.width
            
            text: tr.delete_binding
            color: ui.ds3.figure.attention
            transparent: true
            visible: companyAccess.OBJECT_MONITORING_DELETE || companyAccess.OBJECT_INSTALLATION_DELETE

            onClicked: {
                var settings = {}
                settings["hub_id"] = currentObject ? currentObject.hub_id : ""
                Popups.delete_hub_company_binding(settings, "binding")
            }
        }
    }
}
