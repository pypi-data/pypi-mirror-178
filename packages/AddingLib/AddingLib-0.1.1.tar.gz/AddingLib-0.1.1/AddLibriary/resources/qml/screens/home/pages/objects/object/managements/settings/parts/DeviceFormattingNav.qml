import QtQuick 2.7
import QtQuick.Controls 2.2

import "qrc:/resources/js/desktop/popups.js" as DesktopPopups
import "qrc:/resources/js/popups.js" as Popups
import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.SettingsNavigationTitlePrimary {
    Connections {
        target: app.hub_management_module

        onCardNotFormatted: {
            if (["TIMEOUT", "USER_TIMEOUT"].includes(error)) {
                goBack()
                Popups.text_popup(tr.error, tr.acc_card_user_action_timeout0)
            }

            if (error == "NO_ANSWER") {
                goBack()
                Popups.text_popup(tr.error, tr.acc_card_reader_timeout0)
            }
        }

        onFormatAccessCardStarted: {
            setChild(
                "qrc:/resources/qml/screens/home/pages/objects/object/popups/AccessCardActivateKeypadPopup.qml",
                {
                    "isResetFlow": true,
                }
            )
        }
    }

    title: tr.formatting_access_device
    icon: "qrc:/resources/images/Athena/settings_icons/PassTagResetSettings-L.svg"
    visible: device.test_signal_lost_available

    onEntered: {
        DesktopPopups.popupByPath(
            "qrc:/resources/qml/components/911/DS3/popups/Dialog.qml", {
                title: tr.warning,
                text: tr.alert_formatting,
                firstButtonText: tr.continue_,
                firstButtonCallback: () => {
                    DesktopPopups.please_wait_popup()
                    app.hub_management_module.erase_access_card("press_keypad")
                },
                secondButtonText: tr.cancel,
            }
        )
    }
}
