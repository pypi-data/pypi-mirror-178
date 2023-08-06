import QtQuick 2.12
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.13

import "qrc:/resources/js/popups.js" as Popups
import "qrc:/resources/js/desktop/popups.js" as PopupsDesk
import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/qml/screens/home/pages/events/parts" as Parts
import "qrc:/resources/qml/components/911/DS3" as DS3
import "qrc:/resources/js/utils.js" as Utils


Rectangle {
    id: eventDelegate

    width: header.width
    color: event.hub_event ? ui.colors.dark2 : ui.colors.dark3
    height: 41

    property var header: eventsTable.headerItem
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
        height: 40

        Item {
            Layout.fillHeight: true
            Layout.minimumWidth: header.headerRow.children[0].width
            Layout.maximumWidth: header.headerRow.children[0].width

            Rectangle {
                width: 4
                height: parent.height
                anchors.left: parent.left
                color: {
                    if (event["hub_event"]) {
                        if (!eventDelegate.is_device_feature_enabled) return ui.ds3.figure.disabled
                        return event_color
                    }
                    return event.hub_event ? ui.colors.dark2 : ui.colors.dark3
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

        Parts.TableDivider { isHeader: false }

        Item {
            clip: true
            Layout.fillHeight: true
            Layout.minimumWidth: header.headerRow.children[3].width
            Layout.maximumWidth: header.headerRow.children[3].width

            DS3.Icon {
                id: iconLog

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
            }

            Custom.FontText {
//            see A911-673
                id: stubText
                text: eventDelegate.is_device_feature_enabled ? util.clear_html(notif_text) : tr.event_not_supported
                wrapMode: Text.WordWrap
                width: parent.width - iconLog.width - additionalInfo.width - 4
                font.pixelSize: 13
                textFormat: Text.PlainText
                visible: false
            }

            Custom.FontText {
                text: eventDelegate.is_device_feature_enabled ? notif_text : tr.event_not_supported
                textFormat: Text.PlainText
                color: eventDelegate.is_device_feature_enabled ? ui.colors.light2 : ui.ds3.figure.nonessential
                font.pixelSize: 13
                width: parent.width - iconLog.width - additionalInfo.width - 4
                wrapMode: Text.WordWrap
                anchors {
                    left: iconLog.right
                    leftMargin: 12
                }
                Component.onCompleted: {
                    if (stubText.lineCount <= 3) {
                        anchors.verticalCenter = parent.verticalCenter
                    } else {
                        anchors.verticalCenter = undefined
                    }
                }
            }

            Item {
                id: additionalInfo
                clip: true
                width: visible ? 40 : 0
                height: parent.height
                anchors.right: parent.right
                visible: {
                    if (app_update) return true
                    if (!eventDelegate.is_device_feature_enabled) return false
                    if (facility_permission_request && appUser.role.includes("HEAD_OF_INSTALLERS")) return true
                    if (!event.hub_event) return false
                    if (event.hub_event.code == "M_22_34") return true
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
                    if (event.hub_event.code == "M_22_34") return "qrc:/resources/images/notifications/n-restore-after-alarm-red.svg"
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

                        if (hub && hub.alarm_happened && event.hub_event && event.hub_event.code == "M_44_26") {
                            Popups.voltage_drop_popup()
                            return
                        }

                        if (event.hub_event && event.hub_event.code == "M_22_34") {
                            PopupsDesk.reset_alarm_popup(hub, management)
                            return
                        }

                        if (event.hub_event && event.hub_event.code == "M_ABS_12" && ["13", "18", "1A"].includes(event.hub_event.source_type)) {
                            Popups.antimasking_sensors_failed_popup()
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

        Parts.TableDivider { isHeader: false }

        Item {
            clip: true
            Layout.fillHeight: true
            Layout.minimumWidth: header.headerRow.children[5].width
            Layout.maximumWidth: header.headerRow.children[5].width

            Custom.FontText {
                text: {
                    if (!eventDelegate.is_device_feature_enabled) return ""
                    return event.hub_event ? event.hub_event.source_name : event.system_event.employee_first_name + " " + event.system_event.employee_last_name
                }
                color: ui.colors.middle1
                font.pixelSize: 14
                anchors {
                    left: parent.left
                    leftMargin: 12
                    verticalCenter: parent.verticalCenter
                }
            }
        }
    }
}