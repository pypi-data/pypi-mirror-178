import QtQuick 2.12
import QtQuick.Controls 2.2

import "qrc:/resources/qml/components/911/DS3/" as DS3
import "qrc:/resources/js/desktop/popups.js" as Popups

DS3.Popup {
    id: popup

    property string deviceName: ""
    property string fibraQrcode: ""
    property string deviceType: ""
    property string deviceColor: ""
    property var fibraDevicesImages: {
        "61" : {
            "1": "qrc:/resources/images/Athena/fibra/blinked_devices/DoorProtectFibraBlink-White.png",
            "2": "qrc:/resources/images/Athena/fibra/blinked_devices/DoorProtectFibraBlink-Black.png",
        },
        "62" : {
            "1": "qrc:/resources/images/Athena/fibra/blinked_devices/MotionProtectFibraBlink-White.png",
            "2": "qrc:/resources/images/Athena/fibra/blinked_devices/MotionProtectFibraBlink-Black.png",
        },
        "64" : {
            "1": "qrc:/resources/images/Athena/fibra/blinked_devices/GlassProtectFibraBlink-White.png",
            "2": "qrc:/resources/images/Athena/fibra/blinked_devices/GlassProtectFibraBlink-Black.png",
        },
        "68" : {
            "1": "qrc:/resources/images/Athena/fibra/blinked_devices/CombiProtectFibraBlink-White.png",
            "2": "qrc:/resources/images/Athena/fibra/blinked_devices/CombiProtectFibraBlink-Black.png",
        },
        "6a" : {
            "1": "qrc:/resources/images/Athena/fibra/blinked_devices/KeyPadFibraBlink-White.png",
            "2": "qrc:/resources/images/Athena/fibra/blinked_devices/KeyPadFibraBlink-Black.png",
        },
        "6d" : {
            "1": "qrc:/resources/images/Athena/fibra/blinked_devices/MotionCamFibraBlink-White.png",
            "2": "qrc:/resources/images/Athena/fibra/blinked_devices/MotionCamFibraBlink-Black.png",
        },
        "6e" : {
            "1": "qrc:/resources/images/Athena/fibra/blinked_devices/MotionProtectFibraBlink-White.png",
            "2": "qrc:/resources/images/Athena/fibra/blinked_devices/MotionProtectFibraBlink-Black.png",
        },
        "6f" : {
            "1": "qrc:/resources/images/Athena/fibra/blinked_devices/DoorProtectFibraBlink-White.png",
            "2": "qrc:/resources/images/Athena/fibra/blinked_devices/DoorProtectFibraBlink-Black.png",
        },
        "74" : {
            "1": "qrc:/resources/images/Athena/fibra/blinked_devices/StreetSirenFibraBlink-White.png",
            "2": "qrc:/resources/images/Athena/fibra/blinked_devices/StreetSirenFibraBlink-Black.png",
        },
        "75" : {
            "1": "qrc:/resources/images/Athena/fibra/blinked_devices/HomeSirenFibraBlink-White.png",
            "2": "qrc:/resources/images/Athena/fibra/blinked_devices/HomeSirenFibraBlink-Black.png",
        },
        "7c" : {
            "1": "qrc:/resources/images/Athena/fibra/blinked_devices/MultiTransmitterFibraBlink-White.png",
            "2": "qrc:/resources/images/Athena/fibra/blinked_devices/MultiTransmitterFibraBlink-Black.png",
        }
    }
    property var device: null
    property var hub: null
    property var rooms: {
        if (appUser.company_id) return appCompany.current_facility.management.filtered_rooms
        return appCompany.pro_hubs_model.current_hub.management.filtered_rooms
    }

    property var groups: {
        if (appUser.company_id) return appCompany.current_facility.management.groups
        return appCompany.pro_hubs_model.current_hub.management.groups
    }

    function addDevice() {
        var deviceName = nameInput.atomInput.text.trim()
        var deviceQrCode = deviceQrCodeInput.atomInput.text.trim()

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
        if (hub.firmware_version_dec < 207000 &&
            ([10, 11].includes(ddeviceQrCodeInput.atomInput.text.length) ? deviceQrCodeInput.atomInput.text.slice(8, 10) == "07" : deviceQrCodeInput.atomInput.text.slice(6, 8) == "07")) {
            Popups.text_popup(tr.information, tr.Dev_srch_failed_com_dev_unknown0)
            return
        }

        var room = rooms.get(roomsCombobox.currentIndex)
        var group = null

        if (hub.groups_enabled) {
            if (groupsCombobox.model.length) {
                var group = groups.get(groupsCombobox.currentIndex)
            } else {
                Popups.text_popup(tr.information, tr.please_add_at_least_one_group_first)
                return
            }
        }

        app.hub_management_module.reg_device(
            hub,
            room.room_id,
            group ? group.id : "",
            deviceQrCode,
            deviceName
        )
    }

    Component.onCompleted: {
        deviceType = deviceQrCodeInput.atomInput.text.length == 11 ?
            deviceQrCodeInput.atomInput.text.substring(8, 10).toLowerCase() :
            deviceQrCodeInput.atomInput.text.substring(6, 8).toLowerCase()
        deviceColor = deviceQrCodeInput.atomInput.text.length == 11 ?
            deviceQrCodeInput.atomInput.text.substring(10, 11).toLowerCase() :
            deviceQrCodeInput.atomInput.text.substring(8, 9).toLowerCase()

        app.hub_management_module.device_command_for_fibra_indication(deviceQrCodeInput.atomInput.text, 29)
    }

    Component.onDestruction: {
        app.hub_management_module.device_command_for_fibra_indication(deviceQrCodeInput.atomInput.text, 28)
    }

    Connections {
        target: app

        onActionSuccess: {
            popup.close()
        }

        onActionFailed: {
            popup.close()
        }

        onOnlineChanged: {
            if (!app.online && !appUser.company_id) {
                application.errorPopup(tr.Com_no_connection0)
            }
        }
    }

    Connections {
        target: app.hub_management_module

        onSearchTimeout: {
            Popups.popupByPath("qrc:/resources/qml/components/911/DS3/popups/Dialog.qml", {
                title: tr.dev_not_found,
                text: tr.dev_not_found_fibra_descr,
                isVertical: true,
                firstButtonCallback: addDevice,
                firstButtonText: tr.retry,
                secondButtonText: tr.back,
            })
        }
    }

    width: 500

    modal: true

    closePolicy: Popup.CloseOnEscape | Popup.NoAutoClose
    header: DS3.NavBarModal {
        onClosed: () => {
            popup.close()
        }

        headerText: tr.bus_devices_adding_title
    }
    footer: DS3.ButtonBar {
        buttonText: tr.save
        button.onClicked: addDevice()
    }

    Column {
        width: parent.width

        topPadding: 24
        bottomPadding: 24
        spacing: 24

        Keys.onEnterPressed: footerItem.button.clicked()
        Keys.onReturnPressed: footerItem.button.clicked()

        Component.onCompleted: forceActiveFocus()

        DS3.InfoContainer {
            width: parent.width

            imageType: DS3.InfoContainer.ImageType.BigImage
            imageSource: fibraDevicesImages[deviceType][deviceColor]
            descComponent.text: tr.bus_devices_adding_descr
        }

        Column {
            width: parent.width

            spacing: 4

            DS3.InputSingleLine {
                id: nameInput

                radius: 12
                atomInput {
                    text: deviceName
                    label: tr.name
                    placeholderText: tr.enter_device_name
                    onTextChanged: {
                        atomInput.text = util.validator(atomInput.text, 24)
                        return
                    }
                }
            }

            DS3.Comment {
                width: parent.width

                text: tr.assigning_meaningful_device_name_allows_you_to_identify_it_easily_if_alarm_is_triggered
            }
        }

        DS3.InputSingleLine {
            id: deviceQrCodeInput

            radius: 12
            atomInput {
                text: fibraQrcode
                label: tr.device_id
                readOnly: true
                opacity: 0.3
                labelItem.opacity: 0.3
                required: false
            }
        }

        DS3.SettingsContainer {
            id: roomsCombobox

            width: parent.width

            DS3.SettingsPickerTitleSecondary {
                atomTitle.title: tr.room
                model: rooms.room_names
                currentIndex: 0
            }
        }

        DS3.SettingsContainer {
            width: parent.width

            visible: hub.groups_enabled && !["6a", "74", "75"].includes(deviceType)

            DS3.SettingsPickerTitleSecondary {
                id: groupsCombobox

                atomTitle.title: tr.group
                model: groups.group_names
                currentIndex: 0
            }
        }
    }
}