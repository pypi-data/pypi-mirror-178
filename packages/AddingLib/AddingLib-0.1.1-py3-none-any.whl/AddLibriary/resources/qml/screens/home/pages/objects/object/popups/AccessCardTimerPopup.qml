import QtQuick 2.12
import QtQuick.Controls 2.2

import "qrc:/resources/js/images.js" as Images
import "qrc:/resources/qml/components/911/DS3/popups" as DS3Popups
import "qrc:/resources/qml/components/911/DS3" as DS3
import "qrc:/resources/js/desktop/popups.js" as Popups


DS3Popups.PopupStep {
    id: accessCardTimerPopup

    property var keypad_type
    property var keypad_color
    readonly property var itemsImages: [
        "qrc:/resources/images/cards/KPCWhiteTagBlack.png",
        "qrc:/resources/images/cards/KPCWhiteTagWhite.png",
        "qrc:/resources/images/cards/KPCWhitePassBlack.png",
        "qrc:/resources/images/cards/KPCWhitePassWhite.png",
        "qrc:/resources/images/cards/KPCBlackTagBlack.png",
        "qrc:/resources/images/cards/KPCBlackTagWhite.png",
        "qrc:/resources/images/cards/KPCBlackPassBlack.png",
        "qrc:/resources/images/cards/KPCBlackPassWhite.png",
        "qrc:/resources/images/cards/KPPWhiteTagBlack.png",
        "qrc:/resources/images/cards/KPPWhiteTagWhite.png",
        "qrc:/resources/images/cards/KPPWhitePassBlack.png",
        "qrc:/resources/images/cards/KPPWhitePassWhite.png",
        "qrc:/resources/images/cards/KPPBlackTagBlack.png",
        "qrc:/resources/images/cards/KPPBlackTagWhite.png",
        "qrc:/resources/images/cards/KPPBlackPassBlack.png",
        "qrc:/resources/images/cards/KPPBlackPassWhite.png",
    ]

    Connections {
        target: app.hub_management_module

        onCardNotFormatted: {
            goBack(currentStepIndex)
            app.hub_management_module.exit_card_mode()
        }

        onCardAdded: {
            setChild(
                "qrc:/resources/qml/screens/home/pages/objects/object/popups/AccessCardResultPopup.qml",
                {"keypad_type": keypad_type}
            )
        }

        onCardFormatted: {
            setChild(
                "qrc:/resources/qml/screens/home/pages/objects/object/popups/AccessCardResultPopup.qml",
                {"keypad_type": keypad_type}
            )
        }
    }

    width: 500

    title: isResetFlow ? tr.formatting_access_device : (isDeleteFlow ? tr.remove_access_device : tr.adding_card_flow)
    mainView.contentSpacing: 24

    header: DS3.NavBarModal {
        headerText: accessCardTimerPopup.title
        showCloseIcon: false
    }

    DS3.Spacing {
        height: 24
    }

    DS3.InfoContainer {
        imageType: DS3.InfoContainer.ImageType.DeviceLargeImage
        imageSource: {
            let imgIdx = 0
            if (keypad_type == "19") imgIdx += 8
            if (keypad_color == "BLACK") imgIdx += 4
            if (type == "CARD") imgIdx += 2
            if (color == "WHITE") imgIdx += 1
            return itemsImages[imgIdx]
        }
        titleComponent.text: {
            if (keypad_type == "19") {
                if (type == "TAG") return tr.bring_tag_keypad_plus
                return tr.bring_access_key_keypad_plus
            }
            if (keypad_type == "43") {
                if (type == "TAG") return tr.bring_tag_keypad_combi
                return tr.bring_access_key_keypad_combi
            }
            return tr.bring_access_key_keypad_plus
        }
        descComponent {
            text: isResetFlow ? tr.alert_formatting : ""
            color: ui.ds3.figure.attention
        }
    }

    DS3.ProgressCountdownS {
        id: countdown

        Component.onCompleted: {
            countdown.start()
        }

        anchors.horizontalCenter: parent.horizontalCenter

        time: 59

        onTimerFinished: {
            app.hub_management_module.exit_card_mode()
            goBack(currentStepIndex)
        }
    }

    footer: DS3.ButtonBar {
        id: cancelButton

        width: parent.width

        hasBackground: true
        button.text: isDeleteFlow ? (type == "TAG" ? tr.i_dont_have_tag : tr.i_dont_have_an_access_device) : tr.cancel
        isOutline: !isDeleteFlow
        isAttention: !isDeleteFlow

        button.onClicked: {
            if (isDeleteFlow) {
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
            } else {
                app.hub_management_module.exit_card_mode()
                goBack(currentStepIndex)
            }
        }

        buttons: [
            DS3.ButtonOutlined {
                text: tr.cancel
                visible: isDeleteFlow

                onClicked: {
                    app.hub_management_module.exit_card_mode()
                    goBack(currentStepIndex)
                }
            }
        ]
    }
}
