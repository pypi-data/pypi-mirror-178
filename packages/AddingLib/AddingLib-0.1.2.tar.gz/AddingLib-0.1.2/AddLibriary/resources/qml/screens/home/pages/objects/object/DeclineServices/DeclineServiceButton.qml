import QtQuick 2.14
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.13

import "qrc:/resources/js/desktop/popups.js" as Popups
import "qrc:/resources/qml/components/911/DS3" as DS3


Item {
    Layout.minimumWidth: visible ? 40 : 0
    Layout.maximumWidth: 40
    Layout.minimumHeight: visible ? 40 : 0
    Layout.maximumHeight: 40
    Layout.alignment: Qt.AlignVCenter

    visible: accessibleServices.length > 0

    Connections {
        target: app.facility_module

        onScheduleChannel911RemovalIncidentExistsError: Popups.popupByPath(
            "qrc:/resources/qml/components/911/DS3/popups/Dialog.qml", {
                title: tr.unprocessed_incidents_left_tite,
                text: tr.unprocessed_incidents_left_descr,
                firstButtonText: tr.unprocessed_incidents_left_button,
                firstButtonCallback: () => {
                    app.facility_module.schedule_channel_911_removal({hub_id: facility.hub_id}, true)
                },
                isFirstButtonRed: true,
                firstButtonIsOutline: true,
                secondButtonIsOutline: false,
                secondButtonText: tr.cancel,
                isVertical: true
            }
        )
    }

//  List of services that are exists for hub and current user can manage them
    property var accessibleServices: []

    readonly property var monitoringRemovalPopupConfig: (
        !!facility && !!facility.data && !!facility.data.channel_state
            && (facility.data.channel_state == "PENDING_DELETION" || facility.data.status == "MONITORING_REQUESTED")
            ? {
                title: tr.a911_delete_object_permanently,
                text: tr.delete_object_permanently_description_911,
                firstButtonText: tr.stop_monitoring_button,
                firstButtonCallback: () => {
                    app.facility_module.remove_channel_911({hub_id: facility.hub_id})
                },
                isFirstButtonRed: true,
                firstButtonIsOutline: true,
                secondButtonText: tr.cancel,
                secondButtonIsOutline: false,
                isVertical: true
            }
            : {
                title: tr.move_object_to_trash_title,
                text: tr.move_object_to_trash,
                firstButtonText: tr.stop_monitoring_button,
                firstButtonCallback: () => {
                    app.facility_module.schedule_channel_911_removal({hub_id: facility.hub_id})
                },
                isFirstButtonRed: true,
                firstButtonIsOutline: true,
                secondButtonText: tr.cancel,
                secondButtonIsOutline: false,
                isVertical: true
            }
    )
    readonly property var installationRemovalPopupConfig: ({
        title: tr.remove_installer_911_title,
        text: tr.remove_installer_911_descr,
        firstButtonText: tr.remove_installer_911_button,
        firstButtonCallback: () => {
            app.facility_module.delete_installation_service_on_hub(facility.hub_id, appCompany.id)
        },
        isFirstButtonRed: true,
        firstButtonIsOutline: true,
        secondButtonText: tr.cancel,
        secondButtonIsOutline: false,
        isVertical: true
    })
    readonly property var buttonState: {
        if (["MONITORING", "INSTALLATION"].every(
            service => accessibleServices.includes(service)
        ))
            return "MONITORING_INSTALLATION"
        if (accessibleServices.includes("MONITORING"))
            return "MONITORING"
        if (accessibleServices.includes("INSTALLATION"))
            return "INSTALLATION"
    }
    readonly property var monitoringIcon: {
        if (!!facility && !!facility.scheduled_removal)
            return {
                1: "qrc:resources/images/Athena/common_icons/DaysLeft1.svg",
                2: "qrc:resources/images/Athena/common_icons/DaysLeft2.svg",
                3: "qrc:resources/images/Athena/common_icons/DaysLeft3.svg",
                4: "qrc:resources/images/Athena/common_icons/DaysLeft4.svg",
                5: "qrc:resources/images/Athena/common_icons/DaysLeft5.svg",
                6: "qrc:resources/images/Athena/common_icons/DaysLeft6.svg",
                7: "qrc:resources/images/Athena/common_icons/DaysLeft7.svg",
            }[facility.scheduled_removal]
        return "qrc:/resources/images/Athena/common_icons/DaysLeftNone.svg"
    }
    readonly property var installationIcon: {
        return "qrc:/resources/images/Athena/common_icons/DaysLeftNone.svg"
    }

    Connections {
        target: app.facility_module
        onCancelChannel911RemovalSuccess: {
            editButton.loading = false
            objectsStack.currentObjectIndex = -1
        }
        onCancelChannel911RemovalFailed: {
            editButton.loading = false
        }
    }

    DS3.Image {
        id: mainIcon

        width: 40
        height: 40

        // ToDo: update monitoring icon
        source: ({
            MONITORING_INSTALLATION: "qrc:/resources/images/icons/dropdown-button-three-dots.svg",
            MONITORING: monitoringIcon,
            INSTALLATION: installationIcon
        }[buttonState]) || "qrc:/resources/images/Athena/common_icons/DaysLeftNone.svg"
    }

    DS3.MouseArea {
        onClicked: {
            if (buttonState == "MONITORING_INSTALLATION")
                declineServicesDropDown.visible = !declineServicesDropDown.visible
            else if (buttonState == "MONITORING")
                Popups.popupByPath(
                    "qrc:/resources/qml/components/911/DS3/popups/Dialog.qml",
                    monitoringRemovalPopupConfig
                )
            else if (buttonState == "INSTALLATION")
                Popups.popupByPath(
                    "qrc:/resources/qml/components/911/DS3/popups/Dialog.qml",
                    installationRemovalPopupConfig
                )
            else
                Popups.popupByPath(
                    "qrc:/resources/qml/components/911/DS3/popups/ModalInfo.qml",
                    {
                        sections: [{
                            "description": tr.function_coming_soon
                        }]
                    }
                )
        }
    }

    Popup {
        id: declineServicesDropDown

        width: 260

        focus: true
        padding: 0
        topPadding: 16
        bottomPadding: 16
        closePolicy: Popup.CloseOnEscape | Popup.CloseOnPressOutside
        x: parent.width - width
        y: parent.height + 8
        enter: Transition {
            NumberAnimation { property: "opacity"; from: 0.0; to: 1.0; duration: 200 }
        }
        exit: Transition {
            NumberAnimation { property: "opacity"; from: 1.0; to: 0.0; duration: 200 }
        }
        background: Rectangle {
            color: ui.ds3.bg.high
            radius: 8
        }

        contentItem: Column {
            Repeater {
                model: [
                    {
                        text: tr.stop_monitoring_button,
                        service: "MONITORING",
                        icon: monitoringIcon,
                    },
                    {
                        text: tr.remove_installer_911_list_button,
                        service: "INSTALLATION",
                        icon: installationIcon,
                    }
                ]

                Rectangle {
                    width: parent.width
                    height: Math.max(declineServiceText.height, icon.height) + 16

                    color: ui.ds3.bg[area.containsMouse ? "high" : "highest"]

                    DS3.Icon {
                        id: icon

                        anchors {
                            verticalCenter: parent.verticalCenter
                            left: parent.left
                            margins: 12
                        }

                        source: modelData.icon
                    }

                    DS3.Text {
                        id: declineServiceText

                        style: ui.ds3.text.body.MRegular

                        anchors {
                            verticalCenter: parent.verticalCenter
                            left: icon.right
                            right: parent.right
                            margins: 8
                        }

                        text: modelData.text
                    }

                    Rectangle {
                        width: parent.width
                        height: 1

                        anchors.bottom: parent.bottom

                        color: ui.ds3.bg.base
                    }

                    DS3.MouseArea {
                        id: area

                        onClicked: {
                            Popups.popupByPath(
                                "qrc:/resources/qml/components/911/DS3/popups/Dialog.qml",
                                ({
                                    MONITORING: monitoringRemovalPopupConfig,
                                    INSTALLATION: installationRemovalPopupConfig
                                }[modelData.service])
                            )
                        }
                    }
                }
            }
        }

        Connections {
            target: app.login_module

            onLogoutSignal: {
                popup.close()
            }
        }
    }
}
