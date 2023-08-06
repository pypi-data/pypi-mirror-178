import QtQuick 2.12
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/js/popups.js" as Popups
import "qrc:/resources/js/desktop/popups.js" as PopupsDesk
import "qrc:/resources/qml/components/911/DS3" as DS3
import "qrc:/resources/js/utils.js" as Utils


Rectangle {
    id: eventDelegate
    width: header.width
    color: readable.event_type == "HUB_EVENT" ? ui.colors.dark1 : ui.colors.dark2
    height: stubText.lineCount < 3 ? 41 : 14 * stubText.lineCount + 13  //  autoextend on textwrap (by @Volodimir_Kovalov)

    property var header: eventsTable.headerItem
    property var mouseX: 0
    property var mouseY: 0
    property bool is_device_feature_enabled: !event.hub_event || Utils.check_feature_enabled(
    event["hub_event"]["source_type"],
    event["hub_event"]["code"]
    )

    Rectangle {
        width: parent.width
        height: 1
        color: ui.colors.black
        anchors.bottom: parent.bottom
    }

    RowLayout {
        spacing: 0
        height: parent.height - 1

        Item {
            Layout.fillHeight: true
            Layout.minimumWidth: header.headerRow.children[0].width
            Layout.maximumWidth: header.headerRow.children[0].width

            Rectangle {
                width: 4
                height: parent.height
                color: {
                    if (!eventDelegate.is_device_feature_enabled) return ui.ds3.figure.disabled
                    if (!!event_color) return event_color
                    return readable.event_type == "HUB_EVENT" ? ui.ds3.bg.highest : ui.ds3.bg.high
                }
            }
        }

        Item {
            clip: true
            Layout.fillHeight: true
            Layout.minimumWidth: header.headerRow.children[1].width
            Layout.maximumWidth: header.headerRow.children[1].width

            Custom.FontText {
                id: dateText
                text: ""
                color: eventDelegate.is_device_feature_enabled ? ui.colors.light2 : ui.ds3.figure.nonessential
                font.pixelSize: 14
                font.bold: true
                anchors {
                    left: parent.left
                    verticalCenter: parent.verticalCenter
                }

                Component.onCompleted: {
                    var dt = new Date(timestamp * 1000)
                    text = dt.toLocaleTimeString(
                        application.locale,
                        settings.is_ampm_time_format ? "hh:mm:ss ap" : "HH:mm:ss"
                    )
                }
            }
        }

        TableDivider { isHeader: false }

        Item {
            clip: true
            Layout.fillHeight: true
            Layout.minimumWidth: header.headerRow.children[3].width
            Layout.maximumWidth: header.headerRow.children[3].width

            Custom.FontText {
                text: eventDelegate.is_device_feature_enabled ? readable.hub_id : ""
                color: ui.colors.white
                font.pixelSize: 14
                anchors {
                    left: parent.left
                    leftMargin: 12
                    verticalCenter: parent.verticalCenter
                }
            }
        }

        TableDivider { isHeader: false }

        Item {
            clip: true
            Layout.fillHeight: true
            Layout.minimumWidth: header.headerRow.children[5].width
            Layout.maximumWidth: header.headerRow.children[5].width

            Custom.FontText {
                text: eventDelegate.is_device_feature_enabled ? readable.number : ""
                color: ui.colors.white
                font.pixelSize: 14
                anchors {
                    left: parent.left
                    leftMargin: 12
                    verticalCenter: parent.verticalCenter
                }

                Custom.HandMouseArea {
                    onClicked: {
                        if (!eventsSidebar.rangeToggle.checked) {
                            eventsSidebar.rangeToggle.mouseArea.clicked(true)
                        }
                        eventsSidebar.rangeArea.valueText.control.text = readable.number
                        eventsSidebar.rangeArea.valueText.control.accepted()
                    }
                }
            }
        }

        TableDivider { isHeader: false }

        Item {
            clip: true
            Layout.fillHeight: true
            Layout.minimumWidth: header.headerRow.children[7].width
            Layout.maximumWidth: header.headerRow.children[7].width

            Custom.FontText {
                width: parent.width - 16
                text: eventDelegate.is_device_feature_enabled ? readable.name : ""
                color: ui.colors.light3
                font.pixelSize: 13
                textFormat: Text.PlainText
                elide: Text.ElideRight
                maximumLineCount: 1
                anchors {
                    left: parent.left
                    leftMargin: 12
                    verticalCenter: parent.verticalCenter
                }
            }
        }

        TableDivider { isHeader: false }

        Item {
            clip: true
            Layout.fillHeight: true
            Layout.minimumWidth: header.headerRow.children[9].width
            Layout.maximumWidth: header.headerRow.children[9].width

            DS3.Icon {
                id: iconIncident

                property var image_with_color: {
                    if (event.system_event) return app.get_system_icon(event.system_event.type)
                    return eventDelegate.is_device_feature_enabled ?
                        app.get_notification_icon(event.hub_event.code) :
                        app.get_notification_icon("not_supported")
                }

                anchors {
                    left: parent.left
                    verticalCenter: parent.verticalCenter
                }

                source: image_with_color.source
                color: image_with_color.color

                Custom.HandMouseArea {
                    id: cursorArea
                    enabled: {
                        if (!eventDelegate.is_device_feature_enabled) return false
                        if (!event) return false
                        if (event.system_event && event.system_event.type == "NO_EMPLOYEE_ACTION_TYPE") return false
                        return true
                    }

                    onClicked: {
                        eventsStack.newEventClick(iconIncident.source, iconIncident.color, event, "Image")
                    }

                    onEntered: {
                        if (enabled) {
                            cursorArea.cursorShape = Qt.PointingHandCursor
                        } else {
                            cursorArea.cursorShape = Qt.ArrowCursor
                        }
                    }

                }
            }

            Custom.FontText {
//            see A911-673
                id: stubText
                text: eventDelegate.is_device_feature_enabled ? util.clear_html(readable.text) : ""
                wrapMode: Text.Wrap
                width: eventText.width
                font.pixelSize: 13
                textFormat: Text.PlainText
                visible: false
            }

            Custom.FontText {
                id: eventText

                text: eventDelegate.is_device_feature_enabled ? readable.text : tr.event_not_supported
                color: eventDelegate.is_device_feature_enabled ? ui.colors.light3 : ui.ds3.figure.nonessential
                font.pixelSize: 13
                width: parent.width - iconIncident.width - additionalInfo.width - 12
                wrapMode: Text.Wrap
                anchors {
                    left: iconIncident.right
                    leftMargin: 12
                }

                onLinkActivated: {
                    eventsStack.newEventClick(link, ui.ds3.special.white, event, "Text")
                }

                onLinkHovered: {
                    if (link) {
                        cursorShape.cursorShape = Qt.PointingHandCursor
                    } else {
                        cursorShape.cursorShape = Qt.ArrowCursor
                    }
                }

                Custom.HandMouseArea {
                    id: cursorShape
                    enabled: false
                    hoverEnabled: false
                    propagateComposedEvents: true
                    onPressed: mouse.accepted = false
                }

                Component.onCompleted: {
                    anchors.verticalCenter = parent.verticalCenter
                }
            }

            Item {
                id: additionalInfo
                clip: true
                width: visible ? 40 : 0
                height: parent.height
                anchors.right: parent.right
                visible: {
                    if (!eventDelegate.is_device_feature_enabled) return false
                    if (app_update) return true
                    if (facility_permission_request && appUser.role.includes("HEAD_OF_INSTALLERS")) return true
                    if (!event.hub_event) return false
                    if (event.hub_event.code == "M_ABS_12" && ["13", "18", "1A"].includes(event.hub_event.source_type)) return true // A911-2227
                    if (["M_1A_20", "M_1A_21", "M_1A_22", "M_1A_23", "M_1A_24", "M_1A_25", "M_44_26"].includes(event.hub_event.code)) return true
                    if (!event.hub_event.additional_data) return false
                    if (event.hub_event.additional_data.access_request) return false
                    if (event.hub_event.additional_data && event.hub_event.additional_data.device_malfunctions && event.hub_event.additional_data.device_malfunctions.items.length == 0) return false

                    // A911-1465
                    if (event.hub_event.code == "M_ABS_11") return false
                    if (event.hub_event.code == "M_2F_40") return false
                    if (event.hub_event.code == "M_2F_41") return false
                    if (event.hub_event.code == "M_2F_42") return false
                    if (event.hub_event.code == "M_2F_43") return false
                    if (["M_22_3E", "M_22_3C", "M_22_3D"].includes(event.hub_event.code)) return false
                    if (event.hub_event.code.startsWith("M_44")) return false

                    return true
                }

                property var additionalImageSource: {
                    if (!additionalInfo.visible) return ""
                    if (app_update) return "qrc:/resources/images/icons/info-red.svg"
                    if (facility_permission_request) return "qrc:/resources/images/icons/settings_green.svg"
                    if (!event.hub_event) return ""
                    if (event.hub_event.code == "M_ABS_12" && ["13", "18", "1A"].includes(event.hub_event.source_type)) return "qrc:/resources/images/icons/info-red.svg"   // A911-2227
                    if (["M_1A_20", "M_1A_21", "M_1A_22", "M_1A_23", "M_1A_24", "M_1A_25", "M_44_26"].includes(event.hub_event.code)) return "qrc:/resources/images/icons/info-red.svg"
                    if (event.hub_event.additional_data && event.hub_event.additional_data.device_malfunctions) return "qrc:/resources/images/icons/info-red.svg"
                    if (event.hub_event.additional_data && event.hub_event.additional_data.coordinates) return "qrc:/resources/images/icons/location.svg"
                    if (event.hub_event.additional_data && event.hub_event.additional_data.firmware_version) return "qrc:/resources/images/icons/info-red.svg"
                    if (event.hub_event.additional_data && event.hub_event.additional_data.malfunction_additional_data) return "qrc:/resources/images/icons/info-red.svg"
                    if (event.hub_event.additional_data && event.hub_event.additional_data.resource_description) {
                        if (ready_images.length > 0) return "qrc:/resources/images/desktop/icons/eye.svg"
                        if (count_images.is_all_photo_failed) return "qrc:/resources/images/desktop/icons/eye-grey-crossed.svg"
                        return "qrc:/resources/images/desktop/icons/eye-grey.svg"
                    }

                    return "qrc:/resources/images/events/logo.svg"
                }

                Image {
                    sourceSize.width: 32
                    sourceSize.height: 32
                    visible: !additionalPhotosInfo.visible
                    source: additionalInfo.additionalImageSource

                    anchors {
                        right: parent.right
                        verticalCenter: parent.verticalCenter
                    }

                }

                Column {
                    id: additionalPhotosInfo

                    width: 32
                    clip: true
                    visible: {
                        if (!eventDelegate.is_device_feature_enabled) return false
                        if (!event) return false
                        if (!event.hub_event) return false
                        if (!event.hub_event.additional_data) return false
                        if (!event.hub_event.additional_data.resource_description) return false

                        return !count_images.is_all_photo_failed
                    }

                    anchors {
                        right: parent.right
                        verticalCenter: parent.verticalCenter
                    }

                    Image {
                        sourceSize.width: 26
                        sourceSize.height: 26
                        source: additionalInfo.additionalImageSource

                        anchors {
                            horizontalCenter: parent.horizontalCenter
                        }
                    }

                    Custom.FontText {
                        text: count_images.ready_photos_amount + " / " + count_images.not_failed_photos_amount
                        color: ready_images.length > 0 ? ui.colors.white : "#8a8a8a"
                        width: parent.width
                        height: contentHeight
                        font.pixelSize: 12
                        wrapMode: Text.NoWrap
                        textFormat: Text.PlainText
                        maximumLineCount: 1
                        verticalAlignment: Text.AlignVCenter
                        horizontalAlignment: Text.AlignHCenter
                    }
                }

                Custom.HandMouseArea {
                    enabled: additionalInfo.visible
                    onClicked: {
                        if (app_update) {
                            app.get_app_change_log(app_update)
                            return
                        }

                        if (facility_permission_request) {
                            app.get_company_hub_permission_duration(
                                event.facility.id,
                                event.system_event.additional_data.facility_employee_acl_request_data
                            )
                            return
                        }

                        if (event.hub_event && event.hub_event.code == "M_ABS_12" && ["13", "18", "1A"].includes(event.hub_event.source_type)) {
                            Popups.antimasking_sensors_failed_popup()
                            return
                        }

                        if (event.hub_event && event.hub_event.code == "M_44_26") {
                            Popups.voltage_drop_popup()
                            return
                        }

                        if (event.hub_event && ["M_1A_20", "M_1A_21", "M_1A_22", "M_1A_23", "M_1A_24", "M_1A_25"].includes(event.hub_event.code)) {  //  A911-2425. Have to handle one of ["M_1A_20", "M_1A_21", "M_1A_22", "M_1A_23", "M_1A_24", "M_1A_25"]
                            Popups.dco_event_info_popup(event.hub_event.code)
                            return
                        }

                        if (event.hub_event.additional_data.device_malfunctions) {
                            PopupsDesk.malfunctions_popup(information, null)
                            return
                        }

                        if (event.hub_event.additional_data.malfunction_additional_data) {
                            PopupsDesk.malfunctions_popup(information, null)
                            return
                        }

                        if (event.hub_event.additional_data.coordinates) {
                            var info = {"mode": "temp", "info": {"lat": event.hub_event.additional_data.coordinates.latitude, "lon": event.hub_event.additional_data.coordinates.longitude}}
                            Popups.maps_popup(info)
                            return
                        }

                        if (event.hub_event.additional_data.resource_description && ready_images.length > 0) {
                            Popups.facility_motion_cam_popup(model)
                            return
                        }

                        if (event.hub_event.additional_data.firmware_version) {
                            app.get_hub_changelog(event.hub_event.additional_data.firmware_version.version, event.hub_event.hub_sub_type)
                        }
                    }
                }
            }
        }

        TableDivider { isHeader: false }

//        Item {
//            clip: true
//            Layout.fillHeight: true
//            Layout.minimumWidth: header.headerRow.children[9].width
//            Layout.maximumWidth: header.headerRow.children[9].width
//
//            Custom.FontText {
//                text: readable.source
//                color: ui.colors.middle1
//                font.pixelSize: 14
//                anchors {
//                    left: parent.left
//                    leftMargin: 12
//                    verticalCenter: parent.verticalCenter
//                }
//            }
//        }
//
//        TableDivider { isHeader: false }

        Item {
            clip: true
            Layout.fillHeight: true
            Layout.minimumWidth: header.headerRow.children[11].width
            Layout.maximumWidth: header.headerRow.children[11].width

            Item {
                id: itemLogsIncident
                width: 50
                height: parent.height
                anchors {
                    right: parent.right
//                    rightMargin: 30
                }
                property var incidentClosed: event.type === "SYSTEM_EVENT" && event.system_event.type === "INCIDENT_CLOSED" && !!event.incident_id
                visible: incidentClosed

                Image {
                    id: imageLogs
                    anchors.centerIn: parent
                    sourceSize.width: 24
                    sourceSize.height: 24
                    source: "qrc:/resources/images/icons/n-logtime-red.svg"
                }
                Custom.HandMouseArea {
                    anchors.fill: parent

                    onClicked: {
                        var iconY = mapToItem(home, imageLogs.x, imageLogs.y).y
                        function action(activities) {
                            Popups.incidents_logs(activities, parent, imageLogs.x + 24, imageLogs.y + 32, iconY)
                            eventsTable.action = null
                        }
                        eventsTable.action = action
                        app.incident_module.get_activities(event.incident_id)
                    }
                }
            }
            Custom.FontText {
                text: eventDelegate.is_device_feature_enabled ? readable.address : ""
                color: ui.colors.middle1
                font.pixelSize: 13
                width: itemLogsIncident.incidentClosed ? parent.width - 42 : parent.width - 12
                wrapMode: Text.WordWrap
                elide: Text.ElideRight
                textFormat: Text.PlainText
                maximumLineCount: 2
                rightPadding: 4
                anchors {
                    left: parent.left
                    leftMargin: 12
                    verticalCenter: parent.verticalCenter
                }
            }
        }
    }
}