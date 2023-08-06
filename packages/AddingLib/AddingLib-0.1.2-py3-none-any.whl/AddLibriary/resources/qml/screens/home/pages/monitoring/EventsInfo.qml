import QtQuick 2.12
import QtQuick.Controls 2.13
import QtGraphicalEffects 1.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/js/popups.js" as Popups
import "qrc:/resources/js/desktop/popups.js" as PopupsDesk
import "qrc:/resources/qml/components/911/DS3" as DS3
import "qrc:/resources/js/utils.js" as Utils


Rectangle {
    visible: !tabBarIsOpened
    color: ui.colors.black
    Layout.minimumWidth: incidentPage.width
    Layout.maximumWidth: incidentPage.width
    Layout.minimumHeight: 203
    Layout.preferredHeight: Layout.maximumHeight
    Layout.fillHeight: true

    Rectangle {
        anchors.fill: parent
        color: ui.colors.dark4
        visible: eventsView.model.length == 0
    }

    ScrollView {
        anchors.fill: parent
        clip: true

        ListView {
            id: eventsView
            width: parent.width
            spacing: 1
            boundsBehavior: Flickable.StopAtBounds

            model: {
                if (incident == null) return []
                return incident.filtered_events
            }

            Connections {
                target: tr

                onTranslation_changed: {
                    if (eventsView.model.length == 0) return

                    incident.events.new_tr()
                }
            }

            Custom.EmptySpaceLogo {
                size: incident.is_system_incident ? parent.width / 3 : parent.width / 4
                visible: eventsView.model.length == 0
            }

            section.property: "date"
            section.criteria: ViewSection.FullString
            section.labelPositioning: ViewSection.CurrentLabelAtStart | ViewSection.InlineLabels
            section.delegate: Item {
                width: eventsView.width
                height: 32

                Rectangle {
                    width: eventsView.width
                    height: 32
                    color: ui.colors.dark4
                }

                Custom.FontText {
                    anchors.centerIn: parent
                    color: ui.colors.white
                    font.capitalization: Font.Capitalize
                    font.letterSpacing: 1
                    text: {
                        var today = Date.fromLocaleString(application.locale, section, "yyyy-MM-dd")
                        return today.toLocaleDateString(application.locale, application.locale.dateFormat(Locale.LongFormat))
                    }
                }
            }

            delegate: Rectangle {
                id: eventDelegate

                property bool is_device_feature_enabled: !event.hub_event || Utils.check_feature_enabled(
                    event["hub_event"]["source_type"],
                    event["hub_event"]["code"]
                )

                width: eventsView.width
                height: 56
                color: event.hub_event ? ui.colors.dark1 : ui.colors.dark2
                opacity: {
                    if (event.incident_id == incident.id) {
                        return 1
                    }
                    return 0.6
                }

                Rectangle {
                    width: 4
                    height: 56
                    anchors.left: parent.left
                    color: {
                        if (event["hub_event"]) {
                            if (!eventDelegate.is_device_feature_enabled) return ui.ds3.figure.disabled
                            return event_color
                        }

                        return event.hub_event ? ui.colors.dark1 : ui.colors.dark2
                    }
                }

                RowLayout {
                    anchors {
                        fill: parent
                        leftMargin: 4
                    }
                    spacing: 0

                    Item {
                        Layout.minimumWidth: 8
                        Layout.maximumWidth: 8
                        Layout.fillHeight: true
                    }

                    Custom.FontText {
                        function timeConveter(time) {
                            if (settings.is_ampm_time_format) {
                                var timeSplitted = time.split(":")
                                timeSplitted[0] = timeSplitted[0] % 12
                                time = timeSplitted[0] + ":" + timeSplitted[1] + ":" + timeSplitted[2]
                            }
                            return time
                        }

                        Layout.fillHeight: true
                        color: eventDelegate.is_device_feature_enabled ? ui.colors.white : ui.ds3.figure.nonessential
                        font.pixelSize: 14
                        text: timeConveter(time)
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }

                    Item {
                        Layout.minimumWidth: 44
                        Layout.maximumWidth: 44
                        Layout.fillHeight: true

                        DS3.Icon {
                            id: iconIncident

                            property var image_with_color: {
                                if (event.system_event) return app.get_system_icon(event.system_event.type)
                                return eventDelegate.is_device_feature_enabled ?
                                    app.get_notification_icon(event.hub_event.code) :
                                    app.get_notification_icon("not_supported")
                            }

                            anchors.centerIn: parent

                            source: image_with_color.source
                            color: image_with_color.color
                        }
                    }

                    Item {
                        Layout.fillHeight: true
                        Layout.fillWidth: true
                        Layout.alignment: Qt.AlignVCenter

                        Custom.FontText {
                            width: parent.width - additionalInfo.width - 12
                            color: eventDelegate.is_device_feature_enabled ? ui.colors.light3 : ui.ds3.figure.nonessential
                            text: eventDelegate.is_device_feature_enabled ? normal_text : tr.event_not_supported
                            height: parent.height
                            font.pixelSize: 14
                            wrapMode: Text.WordWrap
                            textFormat: Text.PlainText
                            verticalAlignment: Text.AlignVCenter
                        }

                        Item {
                            id: additionalInfo
                            clip: true
                            width: visible ? 56 : 0
                            height: parent.height
                            anchors.right: parent.right
                            visible: {
                                if (app_update) return true
                                if (!eventDelegate.is_device_feature_enabled) return false
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

                                return true
                            }

                            property var additionalImageSource: {
                                if (!additionalInfo.visible) return ""
                                if (app_update) return "qrc:/resources/images/icons/info-red.svg"
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
                                enabled: additionalInfo.visible && event.incident_id == incident.id
                                onClicked: {
                                    if (app_update) {
                                        app.get_app_change_log(app_update)
                                        return
                                    }

                                    if (event.hub_event && event.hub_event.code == "M_44_26") {
                                        Popups.voltage_drop_popup()
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
                                        var newIndex = incident.filtered_events.map_from_source(index)
                                        newIndex = incident.motion_cam_events.map_from_source(newIndex)
                                        tabBarInfo.currentTab = 3
                                        tabBarInfo.photosGrid.itemAtIndex(newIndex).photoArea.clicked(true)
                                    }

                                    if (event.hub_event.additional_data.firmware_version) {
                                        app.get_hub_changelog(event.hub_event.additional_data.firmware_version.version, event.hub_event.hub_sub_type)
                                    }
                                }
                            }
                        }
                    }

                    Item {
                        Layout.minimumWidth: 16
                        Layout.maximumWidth: 16
                        Layout.fillHeight: true
                    }
                }
            }
        }
    }
}
