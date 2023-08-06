import QtQuick 2.12
import QtQuick.Controls 2.2

import "qrc:/resources/js/images.js" as Images
import "qrc:/resources/qml/components/911/DS3/popups" as DS3Popups
import "qrc:/resources/qml/components/911/DS3" as DS3

DS3Popups.PopupStep {
    id: accessCardTimerPopup

    property var keypad_type

    width: 500

    title: isResetFlow ? tr.formatting_access_device : tr.adding_card_flow

    header: DS3.NavBarModal {
        headerText: accessCardTimerPopup.title

        onClosed: () => {
            app.hub_management_module.exit_card_mode()
            close()
        }
    }

    DS3.Spacing {
        height: 24
    }

    DS3.InfoContainer {
        imageType: DS3.InfoContainer.ImageType.DeviceImage
        imageSource: !!type ? Images.get_image(type, "Large", color) : ""
        titleComponent.text: isResetFlow ? tr.successfully_formatted : (type == "TAG" ? tr.tag_added : tr.access_device_added)
        descComponent.text: isResetFlow ? tr.successfully_formatted_info : (user_id == "00000000" ? tr.access_device_added_guest_tip : tr.access_device_added_tip)
    }

    footer: DS3.ButtonBar {
        buttonText: tr.done
        hasBackground: true
        button.onClicked: {
            app.hub_management_module.exit_card_mode()
            if (isResetFlow) {
                isResetFlow = false
                goBack(currentStepIndex)
            } else {
                close()
            }
        }

        buttons: [
            DS3.ButtonOutlined {
                text: isResetFlow ? tr.format_another_access_device : tr.add_another_access_device

                onClicked: {
                    if (isResetFlow) {
                        app.hub_management_module.erase_access_card("timer")
                        goBack(currentStepIndex - 2)
                        countdown.stop()
                        countdown.start()
                    } else {
                        app.hub_management_module.exit_card_mode()
                        deviceNameField.atomInput.text = ""
                        goBack(currentStepIndex)
                    }
                }
            }
        ]
    }
}
