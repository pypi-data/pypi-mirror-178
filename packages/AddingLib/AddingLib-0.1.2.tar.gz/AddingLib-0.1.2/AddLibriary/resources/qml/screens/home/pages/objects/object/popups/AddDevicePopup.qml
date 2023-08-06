import QtQuick 2.12
import QtQuick.Controls 2.2

import "qrc:/resources/qml/components/911/DS3/" as DS3
import "qrc:/resources/js/desktop/popups.js" as Popups

DS3.Popup {
    id: popup

    property string deviceType: ""
    property var device: null
    property var hub: null
    property int roomIndex: 0
    property var rooms: {
        if (appUser.company_id) return appCompany.current_facility.management.filtered_rooms
        return appCompany.pro_hubs_model.current_hub.management.filtered_rooms
    }

    property var groups: {
        if (appUser.company_id) return appCompany.current_facility.management.groups
        return appCompany.pro_hubs_model.current_hub.management.groups
    }

    function isFibraDevice() {
        return ["61", "62", "64", "68", "6a", "6d", "6e", "6f", "74", "75"].includes(deviceType)
    }

    function addDevice() {
        var deviceName = nameInput.atomInput.text.trim()
        var deviceQrCode = deviceQrCodeInput.atomInput.text.trim()

        progressCountdown.finish()

        if (!deviceName || !deviceQrCode) {
            if (!deviceName) {
                nameInput.atomInput.focus = false
            }
            if (!deviceQrCodeInput.atomInput.text) {
                deviceQrCodeInput.atomInput.focus = false
            }
            Popups.text_popup(tr.information, tr.please_fill_in_all_of_the_required_fields)
            return
        }
        if (!deviceQrCodeInput.atomInput.acceptableInput) {
            deviceQrCodeInput.atomInput.focus = false
            Popups.text_popup(tr.information, tr.bad_device_id)
            return
        }

        deviceType = deviceQrCodeInput.atomInput.text.length == 11 ? deviceQrCodeInput.atomInput.text.slice(8, 10).toLowerCase() : deviceQrCodeInput.atomInput.text.slice(6, 8).toLowerCase()

        if (hub.firmware_version_dec < 207000 && deviceType == "07") {
            Popups.text_popup(tr.information, tr.Dev_srch_failed_com_dev_unknown0)
            return
        }

        var room = rooms.get(roomsCombobox.currentIndex)
        var group = null

        if (isFibraDevice()) {
            textUnderComment.text = tr.add_wire_device_popup
        } else if (Object.keys(devicesTranslationsWOFibra).includes(deviceType)){
            textUnderComment.text = devicesTranslationsWOFibra[deviceType]
        } else {
            // Other devices
            textUnderComment.text = tr.system_can_only_see_enabled_devices_if_it_is_already_enabled_disable_it_first_wait_few_seconds_and_enable_device_again
        }
        deviceImage.visible = false

        if (hub.groups_enabled) {
            if (groupsCombobox.model.length) {
                var group = groups.get(groupsCombobox.currentIndex)
            } else {
                Popups.text_popup(tr.information, tr.please_add_at_least_one_group_first)
                return
            }
        }

        if (group) {
            app.hub_management_module.reg_device(hub, room.room_id, group.id, deviceQrCode, deviceName)
        } else {
            app.hub_management_module.reg_device(hub, room.room_id, '', deviceQrCode, deviceName)
        }

        timerColumnItem.visible = true
    }

    function addDeviceCancel() {
        timerColumnItem.visible = false
        if (isFibraDevice()) {
            textUnderComment.text = tr.add_wire_device_popup
        } else if (Object.keys(devicesTranslationsWOFibra).includes(deviceType)){
            textUnderComment.text = devicesTranslationsWOFibra[deviceType]
        } else {
            // Other devices
            textUnderComment.text = tr.system_can_only_see_enabled_devices_if_it_is_already_enabled_disable_it_first_wait_few_seconds_and_enable_device_again
        }
        deviceImage.visible = false
        app.hub_management_module.reg_device_cancel(hub.hub_id)
        progressCountdown.stop()
    }

    property var devicesTranslationsWOFibra: {
        "1e": tr.plug_the_socket_into_the_outlet_to_register_the_device, // Socket
        "4c": tr.plug_the_socket_into_the_outlet_to_register_the_device, // Socket base
        "0b": tr.push_system_arming_button_and_panic_button_simultaneously_to_add_key_fob, // SpaceControl
        "0c": tr.press_and_hold_to_add_device, // Button
        "1f": tr.wallswitch_registration, // WallSwitch
        "12": tr.relay_registration, // Relay
        "42": tr.press_and_hold_to_add_double_button, // Double Button
        "44": tr.connection_request_sent_lightswitch, // Light Switch
    }

    Connections {
        target: app

        onActionSuccess: {
            footerItem.button.enabled = false
            progressCountdown.finish()
            timerToClose.start()
        }

        onActionFailed: {
            progressCountdown.stop()
            timerColumnItem.visible = false
        }

        onOnlineChanged: {
            if (!app.online) {
                if (!appUser.company_id) {
                    application.errorPopup(tr.Com_no_connection0)
                }
                timerColumnItem.visible = false
            }
        }
    }

    Connections {
        target: app.hub_management_module

        onSearchTimeout: {
            Popups.popupByPath("qrc:/resources/qml/components/911/DS3/popups/Dialog.qml", {
                title: tr.Dev_srch_timeout0,
                text: tr.dev_not_found_descr,
                isVertical: true,
                closePolicy: Popup.NoAutoClose,
                firstButtonText: tr.retry,
                firstButtonCallback: addDevice,
                secondButtonText: tr.back,
                secondButtonCallback: () => {
                    timerColumnItem.visible = false
                }
            })
        }

        onRegStartTimer: {
            progressCountdown.start()
        }

        onSocketTypeGIsAlreadyAdded: {
            textUnderComment.text = tr.hold_button_complete_registration
            deviceImage.visible = true
            deviceImage.source = "qrc:/resources/images/Athena/add_device_to_other_hub/SocketTypeGAdding.svg"
        }

        onLightSwitchIsAlreadyAdded: {
            textUnderComment.text = tr.connection_press_button_lightswitch
            deviceImage.visible = true
            if (ls_subtype == "LIGHT_SWITCH_TWO_GANG") {
                deviceImage.source = "qrc:/resources/images/Athena/add_device_to_other_hub/LightSwitchTwoGangAdding.svg"
            } else {
                deviceImage.source = "qrc:/resources/images/Athena/add_device_to_other_hub/LightSwitchOneGangAdding.svg"
            }
        }
    }

    width: 500

    modal: true
    focus: true
    closePolicy: timerColumnItem.visible ? Popup.NoAutoClose : defaultPolicy

    header: DS3.NavBarModal {
        onClosed: () => {
            popup.close()
        }

        showCloseIcon: !timerColumnItem.visible
        headerText: timerColumnItem.visible ? tr.registering_device : tr.add_device

        /* -------------------------------------------- */
        /* desktop tests */
        accessibleIcoName: "add-device_device_close_button"
        accessibleTextName: "add-device_device_header_text"
        /* -------------------------------------------- */
    }
    footer: DS3.ButtonBar {
        buttonText: timerColumnItem.visible ? tr.cancel : tr.add_device
        button {
            isAttention: timerColumnItem.visible
            isOutline: timerColumnItem.visible
            onClicked: timerColumnItem.visible ? addDeviceCancel() : addDevice()

            /* -------------------------------------------- */
            /* desktop tests */
            accessibleAreaName: "add-device_device_footer_button"
            /* -------------------------------------------- */
        }
    }

    Column {
        id: addDeviceColumnItem

        width: parent.width

        topPadding: 24
        bottomPadding: 24
        spacing: 24
        visible: !timerColumnItem.visible

        Keys.onEnterPressed: {
            if (!timerColumnItem.visible) footerItem.button.clicked()
        }
        Keys.onReturnPressed: {
            if (!timerColumnItem.visible) footerItem.button.clicked()
        }
        Component.onCompleted: forceActiveFocus()

        Column {
            width: parent.width

            spacing: 4

            DS3.InputSingleLine {
                id: nameInput

                radius: 12
                atomInput {
                    label: tr.name
                    placeholderText: tr.enter_device_name
                    onTextChanged: {
                        atomInput.text = util.validator(atomInput.text, 24)
                        return
                    }

                    /* -------------------------------------------- */
                    /* desktop tests */
                    accessibleLabelName: "add-device_device_name_label"
                    accessibleFieldName: "add-device_device_name_field"
                    /* -------------------------------------------- */
                }
            }

            DS3.Comment {
                width: parent.width

                text: tr.assigning_meaningful_device_name_allows_you_to_identify_it_easily_if_alarm_is_triggered

                /* ------------------------------------------------ */
                /* desktop tests */
                Accessible.name: "add-device_device_name_comment"
                Accessible.description: text
                Accessible.role: Accessible.Paragraph
                /* ------------------------------------------------ */
            }
        }

        Column {
            width: parent.width

            spacing: 4

            DS3.InputSingleLine {
                id: deviceQrCodeInput

                radius: 12
                atomInput {
                    label: tr.device_id
                    placeholderText: tr.device_id_input
                    validator: RegExpValidator { regExp: ui.regexes.qr_code}
                    onTextChanged: {
                        deviceQrCodeInput.atomInput.text = util.validator(atomInput.text, 11)
                        return
                    }

                    /* -------------------------------------------- */
                    /* desktop tests */
                    accessibleLabelName: "add-device_device_qr_label"
                    accessibleFieldName: "add-device_device_qr_field"
                    /* -------------------------------------------- */
                }
            }

            DS3.Comment {
                width: parent.width

                text: tr.enter_device_id_desktop

                /* ------------------------------------------------ */
                /* desktop tests */
                Accessible.name: "add-device_device_qr_comment"
                Accessible.description: text
                Accessible.role: Accessible.Paragraph
                /* ------------------------------------------------ */
            }
        }

        DS3.SettingsContainer {
            width: parent.width

            DS3.SettingsPickerTitleSecondary {
                id: roomsCombobox

                atomTitle.title: tr.room
                model: rooms.room_names
                currentIndex: roomIndex

                /* ---------------------------------------------------- */
                /* desktop tests */
                accessibleTitleName: "add-device_device_room_title"
                accessibleItemNamePrefix: "add-device_device_room_room"

                Accessible.name: "add-device_device_room_dropdown"
                Accessible.description: currentText
                Accessible.role: Accessible.ComboBox
                Accessible.checkable: visible && enabled
                Accessible.onPressAction: {
                    if (!Accessible.checkable) return
                    if (!roomsCombobox.popup.visible) roomsCombobox.popup.open()
                    else roomsCombobox.popup.close()
                }
                /* ---------------------------------------------------- */
            }
        }

        DS3.SettingsContainer {
            width: parent.width

            visible: {
                if (hub.groups_enabled) {
                    return !["0a", "0b", "14", "15", "19", "1b", "43", "6a", "74", "75"].includes(
                        deviceQrCodeInput.atomInput.text.length == 11 ?
                        deviceQrCodeInput.atomInput.text.slice(8, 10).toLowerCase() :
                        deviceQrCodeInput.atomInput.text.slice(6, 8).toLowerCase())
                }
                return false
            }

            DS3.SettingsPickerTitleSecondary {
                id: groupsCombobox

                atomTitle.title: tr.group
                model: groups.group_names
                currentIndex: 0

                /* ---------------------------------------------------- */
                /* desktop tests */
                accessibleTitleName: "add-device_device_group_title"
                accessibleItemNamePrefix: "add-device_device_group_group"

                Accessible.name: "add-device_device_group_dropdown"
                Accessible.description: currentText
                Accessible.role: Accessible.ComboBox
                Accessible.checkable: visible && enabled
                Accessible.onPressAction: {
                    if (!Accessible.checkable) return
                    if (!groupsCombobox.popup.visible) groupsCombobox.popup.open()
                    else groupsCombobox.popup.close()
                }
                /* ---------------------------------------------------- */
            }
        }
    }

    Timer {
        id: timerToClose

        interval: 1000

        onTriggered: {
            popup.close()
        }
    }

    Column {
        id: timerColumnItem

        width: parent.width

        visible: false

        DS3.Spacing {
            height: 24
        }

        DS3.ProgressCountdownS {
            id: progressCountdown

            anchors.horizontalCenter: parent.horizontalCenter

            time: 30

            /* ------------------------------------------------ */
            /* desktop tests */
            accessibleTimeName: "add-device_device_timer_time"

            Accessible.name: "add-device_device_timer"
            Accessible.description: ""
            Accessible.role: Accessible.Graphic
            /* ------------------------------------------------ */
        }

        DS3.Spacing {
            height: 24
        }

        DS3.Text {
            id: textUnderComment

            width: parent.width

            text: {
                if (isFibraDevice()) {
                    return tr.add_wire_device_popup
                }
                if (Object.keys(popup.devicesTranslationsWOFibra).includes(deviceType)){
                    return popup.devicesTranslationsWOFibra[deviceType]
                }
                // Other devices
                return tr.system_can_only_see_enabled_devices_if_it_is_already_enabled_disable_it_first_wait_few_seconds_and_enable_device_again

            }
            style: ui.ds3.text.body.LRegular
            color: ui.ds3.figure.secondary
            horizontalAlignment: Text.AlignHCenter

            /* ------------------------------------------------ */
            /* desktop tests */
            Accessible.name: "add-device_device_timer_comment"
            Accessible.description: text
            Accessible.role: Accessible.Paragraph
            /* ------------------------------------------------ */
        }

        DS3.Spacing {
            height: deviceImage.visible ? 24 : 328
        }

        DS3.Image {
            id: deviceImage

            width: 320
            height: 320

            anchors.horizontalCenter: parent.horizontalCenter

            visible: false
        }
    }
}