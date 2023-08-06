import QtQuick 2.12
import QtQuick.Controls 2.2

import "qrc:/resources/js/desktop/popups.js" as Popups
import "qrc:/resources/js/images.js" as Images
import "qrc:/resources/qml/components/911/DS3/popups" as DS3Popups
import "qrc:/resources/qml/components/911/DS3" as DS3

DS3Popups.PopupStep {
    id: accessCardActivateKeypadPopup
//  Devices in management
    property var devices: management.devices
//  If reset(erase, format) flow (Not adding)
    property bool isResetFlow
//  If delete flow
    property bool isDeleteFlow
//  Type of KeyPad where user touched button
    property var keypad_type: null
//  Color of KeyPad where user touched button
    property var keypad_color: null
//  Type of card (pass or tag)
    property var type: null
//  Color of pass/tag (black or white)
    property var color: null
//  Associated user id
    property var user_id: null

    Connections {
        target: app.hub_management_module

        onPressDoneKeypadButton: {
            setChild(
                "qrc:/resources/qml/screens/home/pages/objects/object/popups/AccessCardTimerPopup.qml",
                {"keypad_type": keypad_type, "keypad_color": keypad_color}
            )
        }

        onFormatAccessCardStarted: {
            if (isResetFlow) {
                goBack(currentStepIndex - 2)
                return
            }
            isResetFlow = true
            goBack(currentStepIndex - 1)
        }

        onCardNotAdded: {
            if (error == "CARD_FULL") {
                if (isDeleteFlow) {
                    close()
                    app.hub_management_module.exit_card_mode()
                    return
                }
                Popups.popupByPath("qrc:/resources/qml/components/911/DS3/popups/Dialog.qml", {
                    title: tr.error,
                    text: tr.acc_card_full0,
                    closePolicy: Popup.NoAutoClose,
                    firstButtonText: tr.format,
                    firstButtonCallback: () => {
                        Popups.please_wait_popup()
                        app.hub_management_module.erase_access_card("press_keypad")
                    },
                    secondButtonText: tr.cancel,
                    secondButtonIsOutline: true,
                    secondButtonCallback: () => {
                        goBack(currentStepIndex)
                        app.hub_management_module.exit_card_mode()
                    },
                })
            } else if (["TIMEOUT", "NO_ANSWER", "USER_TIMEOUT", "ALREADY_ADDED", "INVALID_CARD"].includes(error)) {
                goBack(currentStepIndex)
                app.hub_management_module.exit_card_mode()
            }
        }

        onCardDeleted: {
            close()
        }
    }

    width: 500

    title: isResetFlow ? tr.formatting_access_device : (isDeleteFlow ? tr.remove_access_device : tr.adding_card_flow)
    mainView.contentSpacing: 24

    header: DS3.NavBarModal {
        headerText: accessCardActivateKeypadPopup.title
        showBackArrow: popup.child.hasChild

        onBackAreaClicked: {
            goBack()
            app.hub_management_module.exit_card_mode()
         }
        onClosed: () => {
            app.hub_management_module.exit_card_mode()
            popup.close()
        }
    }

    DS3.Spacing {
        height: 24
    }

    DS3.InfoContainer {
        imageType: DS3.InfoContainer.ImageType.PlugImage
        imageSource: "qrc:/resources/images/Athena/common_icons/ActiveAnyButton.svg"
        descComponent.text: {
            if (devices.fake_cards_block().is_kpp_here() && devices.fake_cards_block().is_kpc_here()) {
                return tr.click_disarm_button_keypad_plus_combi
            } else if (devices.fake_cards_block().is_kpp_here()) {
                return tr.click_disarm_button_keypad_plus
            } else {
                return tr.click_disarm_button_keypad_combi
            }
        }
    }

    Rectangle {
        width: 32
        height: 32

        anchors.horizontalCenter: parent.horizontalCenter

        radius: width / 2
        color: ui.ds3.bg.highest

        DS3.Icon {
            anchors.centerIn: parent

            source: "qrc:/resources/images/Athena/notifications/Disarmed-M.svg"
            color: ui.ds3.figure.base
        }
    }

    DS3.Image {
        width: 136
        height: 136

        anchors.horizontalCenter: parent.horizontalCenter

        source: {
            if (!devices.fake_cards_block().is_kpp_here() && !devices.fake_cards_block().is_kpc_here()) return ""
            if (devices.fake_cards_block().is_kpp_here() && devices.fake_cards_block().is_kpc_here()) {
                return "qrc:/resources/images/desktop/delegates/KeyPadPlusCombi/KeyPadPlusCombiLarge.png"
            } else if (devices.fake_cards_block().is_kpp_here()) {
                keypad_color = devices.fake_cards_block().keypad_color("19")
                return Images.get_image("19", "Large", keypad_color)
            } else {
                keypad_color = devices.fake_cards_block().keypad_color("43")
                return Images.get_image("43", "Large", keypad_color)
            }
        }
    }

    footer: Item {
        width: parent.width
        height: isDeleteFlow ? buttonBar.height : 0

        DS3.ButtonBar {
            id: buttonBar

            visible: isDeleteFlow
            buttonText: type == "TAG" ? tr.i_dont_have_tag : tr.i_dont_have_an_access_device
            hasBackground: true
            button.onClicked: {
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
                })
            }

            buttons: [
                DS3.ButtonOutlined {
                    text: tr.cancel

                    onClicked: {
                        goBack(popup.currentStepIndex)
                        app.hub_management_module.exit_card_mode()
                    }
                }
            ]
        }
    }
}
