import QtQuick 2.12
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.13
import QtGraphicalEffects 1.14

import "qrc:/resources/js/popups.js" as Popups
import "qrc:/resources/js/images.js" as Images
import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/js/desktop/popups.js" as PopupsDesk
import "qrc:/resources/qml/components/911/DS3" as DS3
import "qrc:/resources/js/utils.js" as Utils


Rectangle {
    id: eventsBody
    color: ui.colors.dark3

    property var proNotifications: appCompany.pro_hubs_model.current_hub.notifications

    property var prevLength: 0

    Custom.EmptySpaceLogo {
        visible: proNotifications.length == 0
    }

    DS3.ListView {
        id: listView

        width: parent.width

        anchors {
            top: parent.top
            bottom: parent.bottom
        }

        list {
            /*
            A911-2659: add cacheBuffer to avoid erroneous filtering
            A911-5053: remove cacheBuffer to avoid scroll freezing

            cacheBuffer: 50000
            */
            section.property: "date"
            section.criteria: ViewSection.FullString
            section.labelPositioning: ViewSection.CurrentLabelAtStart | ViewSection.InlineLabels
            section.delegate: Rectangle {
                width: eventsBody.width
                height: 32
                color: ui.colors.dark3

                Custom.FontText {
                    anchors.centerIn: parent
                    color: ui.colors.white
                    font.capitalization: Font.Capitalize
                    font.letterSpacing: 1
                    text: {
                        var today = Date.fromLocaleString(application.locale, section, "yyyy-MM-dd")
                        return today.toLocaleDateString(application.locale, application.locale.dateFormat(Locale.LongFormat))
                    }

                    /* ---------------------------------------------------- */
                    /* desktop tests */
                    Accessible.name: "notifications_header_" + section + "_date"
                    Accessible.description: text
                    Accessible.role: Accessible.Paragraph
                    /* ---------------------------------------------------- */
                }
            }

            model: eventsBody.proNotifications

            delegate: Item {
                width: parent.width
                height: 64

                Rectangle {
                    id: deleg

                    property bool is_device_feature_enabled: !event.hub_event || Utils.check_feature_enabled(
                        event["hub_event"]["source_type"],
                        event["hub_event"]["code"]
                    )

                    /* -------------------------------------------- */
                    /* desktop tests */
                    property var accessibleBasis: __accessible_unique_ids__ ? "notifications_event_" + event.hub_event.event_id : "event"

                    Accessible.name: "notifications_event_" + event.hub_event.event_id + "_instance"
                    Accessible.description: "instance of notification (group)"
                    Accessible.role: Accessible.Grouping
                    /* -------------------------------------------- */

                    width: parent.width
                    height: 56

                    radius: 8
                    clip: true
                    color: ui.colors.dark1
                    anchors {
                        top: parent.top
                        horizontalCenter: parent.horizontalCenter
                    }

                    property var spacing: 16

                    Rectangle {
                        id: markerItem

                        width: parent.radius * 2
                        height: parent.height
                        radius: parent.radius
                        color: {
                            if (event["hub_event"]) {
                                if (!deleg.is_device_feature_enabled) return ui.ds3.figure.disabled
                                return event_color
                            }
                            return "transparent"
                        }

                        Rectangle {
                            width: parent.width / 2
                            height: parent.height
                            color: ui.colors.dark1
                            anchors {
                                left: parent.left
                                leftMargin: parent.radius
                            }
                        }

                        /* ------------------------------------------------ */
                        /* desktop tests */
                        Accessible.name: deleg.accessibleBasis + "_color"
                        Accessible.description: markerItem.color
                        Accessible.role: Accessible.Graphic
                        /* ------------------------------------------------ */
                    }

                    Item {
                        id: iconItem

                        width: 24
                        height: 24

                        anchors {
                            left: markerItem.right
                            leftMargin: deleg.spacing - parent.radius
                            verticalCenter: parent.verticalCenter
                        }

                        DS3.Icon {
                            property var image_with_color: {
                                if (event.system_event) return app.get_system_icon(event.system_event.type)
                                return deleg.is_device_feature_enabled ?
                                    app.get_notification_icon(event.hub_event.code) :
                                    app.get_notification_icon("not_supported")
                            }

                            anchors.centerIn: parent

                            source: image_with_color.source
                            color: image_with_color.color

                            /* -------------------------------------------- */
                            /* desktop tests */
                            Accessible.name: deleg.accessibleBasis + "_icon"
                            Accessible.description: source + "_" + color
                            Accessible.role: Accessible.Graphic
                            /* -------------------------------------------- */
                        }
                    }

                    Item {
                        id: imageItem
                        width: 40
                        height: 40
                        anchors {
                            left: iconItem.right
                            leftMargin: deleg.spacing
                            verticalCenter: parent.verticalCenter
                        }

                        property var useMask: {
                            var temp = event.hub_event.source_type.toLowerCase()
                            if (temp == "22" || temp == "23" || temp == "24" || temp == "2a" || temp == "2b" || temp == "2c" || temp == "2d" || temp == "50" || temp == "51") return true
                            return false
                        }

                        property var devicesWithoutColor: ["22", "23", "24", "25", "2a", "2b", "2c", "2d", "50", "51"]

                    Image {
                        id: objectImage
                        anchors.fill: parent
                        visible: !imageItem.useMask
                        fillMode: Image.PreserveAspectFit
                        onStatusChanged: {
                            if (objectImage.status == Image.Error)
                                objectImage.source = "qrc:/resources/images/desktop/delegates/UserPicture/UserPictureSmall.png"
                        }
                        source: {
                            var color = "WHITE"
                            var st = event.hub_event.source_type.toLowerCase()

                                if (!deleg.is_device_feature_enabled) return "qrc:/resources/images/Athena/notifications/WiredBlack-M.png"

                                if (object_image != "") return object_image

                                if (st == "21") {
                                    var hub = management.devices.hub

                                return Images.get_image(hub.image_type_name, "Small", hub.color)
                            }

                                if (!imageItem.devicesWithoutColor.includes(st)) {
                                    var device = management.devices.get_by_id(event.hub_event.source_id)
                                    if (device && device.color) {
                                        color = device.color
                                    }

                            }
                            var card = management.devices.get_by_id(event.hub_event.source_id)
                            if (card && card.obj_type == "2e") {
                                st = card.card_type
                                color = card.color
                                return Images.get_image(st, "Small", color)
                            }

                            if (st == "26") {
                                var wi = management.devices.get_by_id(event.hub_event.source_id)
                                if (wi) {
                                    return Images.get_image(wi.input_is_tamper == 1 ? "26-wired-tamper" : "26-wired-intrusion", "Small")
                                }
                            }

                            if (st == "1d") {
                                var wimt = management.devices.get_by_id(event.hub_event.source_id)
                                if (wimt) {
                                    return Images.get_image(wimt.obj_type, "Small", wimt.input_type, wimt.assigned_mtr_object.mtr2_available ? wimt.custom_alarm_S2 : wimt.custom_alarm)
                                }
                            }

                            if (event.hub_event.source_type == "2A") {
                                return "qrc:/resources/images/Athena/settings_icons/Scenarios-M.svg"
                            }

                            if (st == "28") {
                                return Images.get_image(device.device_type != 2 ? "28-keypad-yavir" : "28-reader-yavir", "Small")
                            }

                            if (st == "29") {
                                return Images.get_image(st, "Small")
                            }

                            if (st == "4c") {
                                return Images.get_image(st, "Small", color, null, "TYPE_G")
                            }

                            if (st == "44") {
                                return Images.get_image(st, "Small", color, null, "LIGHT_SWITCH_ONE_GANG")
                            }

                            if (st == "4d") {
                                return Images.get_image(st, "Small", color, null, "FIRE_PROTECT2")
                            }
                            var temp = Images.get_image(st, "Small", color)
                            return temp
                        }
                    }

                        OpacityMask {
                            visible: imageItem.useMask
                            anchors.fill: objectImage
                            source: objectImage

                            maskSource: Rectangle {
                                width: imageItem.width
                                height: imageItem.height
                                radius: height / 2
                                visible: false
                            }
                        }

                        /* ------------------------------------------------ */
                        /* desktop tests */
                        Accessible.name: deleg.accessibleBasis + "_image"
                        Accessible.description: objectImage.source
                        Accessible.role: Accessible.Graphic
                        /* ------------------------------------------------ */
                    }

                    Custom.FontText {
                        id: textItem
                        color: deleg.is_device_feature_enabled ? ui.colors.light3 : ui.ds3.figure.nonessential
                        font.pixelSize: 14
                        width: parent.width - 256
                        wrapMode: Text.WordWrap
                        textFormat: Text.PlainText
                        verticalAlignment: Text.AlignVCenter
                        text: {
                            if (!deleg.is_device_feature_enabled) return tr.event_not_supported
                            var temp = notif_text
                            return temp.charAt(0).toUpperCase() + temp.slice(1)
                        }
                        anchors {
                            left: imageItem.right
                            leftMargin: deleg.spacing
                            verticalCenter: parent.verticalCenter
                        }

                        /* ------------------------------------------------ */
                        /* desktop tests */
                        Accessible.name: deleg.accessibleBasis + "_text"
                        Accessible.description: text
                        Accessible.role: Accessible.Paragraph
                        /* ------------------------------------------------ */
                    }

                    Item {
                        id: additionalInfo
                        clip: true
                        width: visible ? 56 : 0
                        height: parent.height
                        anchors {
                            right: timeItem.left
                            rightMargin: deleg.spacing
                        }

                        visible: {
                            if (app_update) return true
                            if (!deleg.is_device_feature_enabled) return false
                            if (!event.hub_event) return false
                            if (event.hub_event && event.hub_event.code == "M_ABS_12" && ["13", "18", "1A"].includes(event.hub_event.source_type)) return true // A911-2227
                            if (["M_1A_20", "M_1A_21", "M_1A_22", "M_1A_23", "M_1A_24", "M_1A_25", "M_44_26"].includes(event.hub_event.code)) return true
                            if (hub && hub.alarm_happened && event.hub_event.code == "M_22_34") return true
                            if (!event.hub_event.additional_data) return false
                            if (event.hub_event.additional_data.access_request) return false
                            if (event.hub_event.additional_data && event.hub_event.additional_data.device_malfunctions && event.hub_event.additional_data.device_malfunctions.items.length == 0) return false
                            // Events with additional info we don't need to show
                            if (
                                [
                                    "M_ABS_11", "M_22_3C", "M_22_3E", "M_22_3D", "M_2F_40", "M_2F_41", "M_2F_42",
                                    "M_2F_43"
                                ].includes(event.hub_event.code)
                            ) return false
                            if (event.hub_event.code.startsWith("M_44")) return false

                            return true
                        }

                        property var additionalImageSource: {
                            if (!additionalInfo.visible) return ""
                            if (app_update) return "qrc:/resources/images/icons/info-red.svg"
                            if (event.hub_event && event.hub_event.code == "M_ABS_12" && ["13", "18", "1A"].includes(event.hub_event.source_type)) return "qrc:/resources/images/icons/info-red.svg"   // A911-2227
                            if (["M_1A_20", "M_1A_21", "M_1A_22", "M_1A_23", "M_1A_24", "M_1A_25", "M_44_26"].includes(event.hub_event.code)) return "qrc:/resources/images/icons/info-red.svg"
                            if (hub && hub.alarm_happened && event.hub_event.code == "M_22_34") return "qrc:/resources/images/notifications/n-restore-after-alarm-red.svg"
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

                                if (hub && hub.alarm_happened && event.hub_event && event.hub_event.code == "M_44_26") {
                                    Popups.voltage_drop_popup()
                                    return
                                }

                                if (hub && hub.alarm_happened && event.hub_event && event.hub_event.code == "M_22_34") {
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
    //                                if (!hub.current_user.common_params_access) {
    //                                    Popups.text_popup(tr.error, tr.no_pro_permissions)
    //                                    return
    //                                }
                                    Popups.facility_motion_cam_popup(model)
                                    return
                                }

                                if (event.hub_event.additional_data.firmware_version) {
                                    app.get_hub_changelog(event.hub_event.additional_data.firmware_version.version, event.hub_event.hub_sub_type)
                                }
                            }
                        }
                    }

                    Item {
                        id: timeItem
                        width: 80
                        height: parent.height
                        anchors.right: parent.right

                        Custom.FontText {
                            color: ui.colors.light3
                            font.pixelSize: 14
                            width: parent.width - 16
                            wrapMode: Text.WordWrap
                            verticalAlignment: Text.AlignVCenter
                            text: deleg.is_device_feature_enabled ? time : ""
                            anchors {
                                right: parent.right
                                rightMargin: 16
                                verticalCenter: parent.verticalCenter
                            }

                            /* -------------------------------------------- */
                            /* desktop tests */
                            Accessible.name: deleg.accessibleBasis + "_time"
                            Accessible.description: text
                            Accessible.role: Accessible.Paragraph
                            /* -------------------------------------------- */
                        }
                    }
                }
            }
        }

        onBottomReached: app.hub_management_module.get_hub_events(hub.hub_id, proNotifications.length)

        Connections {
            target: tr

            onTranslation_changed: {
                appCompany.pro_hubs_model.current_hub.events.new_tr()
            }
        }
    }

    Connections {
        target: management

        onLogsDropped: {
            appCompany.pro_hubs_model.current_hub.events.clear_all()
        }
    }
}
