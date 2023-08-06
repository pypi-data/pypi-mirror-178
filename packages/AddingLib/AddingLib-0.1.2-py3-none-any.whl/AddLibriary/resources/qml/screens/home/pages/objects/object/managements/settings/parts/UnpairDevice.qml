import QtQuick 2.7
import QtQuick.Controls 2.2

import "qrc:/resources/qml/components/911/DS3" as DS3
import "qrc:/resources/js/desktop/popups.js" as Popups


DS3.SettingsContainer {
    width: parent.width

    DS3.ButtonRow {
        id: unpairDevice

        text: tr.unpair_device
        isDanger: true

        onClicked: {
            if (device.obj_type == "2e") {
                if (!management.devices.fake_cards_block().is_kpp_kpc_here) {
                    Popups.popupByPath("qrc:/resources/qml/components/911/DS3/popups/Dialog.qml", {
                        title: tr.warning,
                        text: tr.remove_card_warning_alert,
                        closePolicy: Popup.NoAutoClose,
                        firstButtonText: tr.delete,
                        firstButtonCallback: () => {
                            app.hub_management_module.delete_access_card(device.id, "WITHOUT_CARD")
                        },
                        secondButtonText: tr.cancel,
                        secondButtonIsOutline: true,
                        secondButtonCallback: () => {
                            app.hub_management_module.exit_card_mode()
                        },
                    })
                } else {
                    Popups.please_wait_popup()
                    app.hub_management_module.delete_access_card(device.id, "WITH_CARD")
                }
            } else {
                Popups.delete_device_popup(hub.hub_id, device, management)
            }
        }

        /* ---------------------------------------------------- */
        /* desktop tests */
        Accessible.name: "delete_device_" + device.id + "_button"
        Accessible.description: "<button enabled=" + Accessible.checkable + ">" + text + "</button>"
        Accessible.role: Accessible.Button
        Accessible.checkable: visible && enabled
        Accessible.onPressAction: {
            if (!Accessible.checkable) return
            unpairDevice.clicked(true)
        }
        /* ---------------------------------------------------- */
    }
}