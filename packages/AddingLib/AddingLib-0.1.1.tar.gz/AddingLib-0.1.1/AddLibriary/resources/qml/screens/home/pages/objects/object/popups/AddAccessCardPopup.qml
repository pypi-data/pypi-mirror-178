import QtQuick 2.12
import QtQuick.Controls 2.2

import "qrc:/resources/js/popups.js" as Popups
import "qrc:/resources/js/desktop/popups.js" as DesktopPopups
import "qrc:/resources/qml/components/911/DS3/popups" as DS3Popups
import "qrc:/resources/qml/components/911/DS3" as DS3


DS3Popups.PopupMultistep {
    id: popup

    property var management: {
        if (appCompany.current_facility) return appCompany.current_facility.management
        return appCompany.pro_hubs_model.current_hub.management
    }

    property var users: {
        if (!appUser.company_id) return appCompany.pro_hubs_model.current_hub.management.users
        return appCompany.current_facility.management.users
    }

    property var currentUser

    width: 500

    maxStepHeight: maxPopupHeight - headerItem.height - footerItem.height
    height: maxPopupHeight
    closePolicy: Popup.NoAutoClose

    firstStepComponent: DS3Popups.PopupStep {
        id: firstStep

        Connections {
            target: app

            onActionSuccess: {
                popup.close()
            }

            onActionFailed: {
                goBack(popup.currentStepIndex)
                app.hub_management_module.exit_card_mode()
            }
        }

        Connections {
            target: app.hub_management_module

            onPressKeypadButton: {
                setChild(
                    "qrc:/resources/qml/screens/home/pages/objects/object/popups/AccessCardActivateKeypadPopup.qml",
                    {
                        "type": type,
                        "color": color,
                        "user_id": user_id
                    }
                )
            }

            onCardNotAdded: {
                if (error == "USER_TIMEOUT") {
                    Popups.text_popup(tr.error, tr.acc_card_user_action_timeout0)
                }
                if (error == "TIMEOUT") {
                    Popups.text_popup(tr.error, tr.acc_card_user_action_timeout0)
                }
                if (error == "NO_ANSWER") {
                    Popups.text_popup(tr.error, tr.acc_card_reader_timeout0)
                }
                if (error == "ALREADY_ADDED") {
                    Popups.text_popup(tr.information, tr.acc_card_exist0)
                }
                if (error == "INVALID_CARD") {
                    Popups.text_popup(tr.information, tr.acc_card_incompatible0)
                }
            }

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
        }

        height: maxStepHeight

        sidePadding: 24

        header: DS3.NavBarModal {
            headerText: tr.adding_card_flow

            onClosed: () => {
                popup.close()
            }
        }

        DS3.Spacing {
            height: 24
        }

        DS3.CarrouselContainerStack {
            id: photoCarousel

            selectedType: "CARD"
            devicesModel: ["CARD", "TAG"]
            colorPeaker.colorModel: [
                {
                    text: tr.black,
                    circleColor: ui.ds3.special.black,
                    serverColor: "BLACK",
                },
                {
                    text: tr.white,
                    circleColor: ui.ds3.special.white,
                    serverColor: "WHITE",
                }
            ]
        }

        DS3.Spacing {
            height: 24
        }

        DS3.SettingsContainer {
            width: parent.width

            DS3.InputSingleLine {
                id: deviceNameField

                atomInput {
                    label: tr.name
                    placeholderText: tr.enter_pass_tag_name_input

                    onTextChanged: {
                        atomInput.text = util.validator(atomInput.text, 24)
                    }
                }

                Keys.onEnterPressed: {
                    footerItem.button.clicked(true)
                }

                Keys.onReturnPressed: {
                    footerItem.button.clicked(true)
                }
            }
        }

        DS3.Comment {
            width: parent.width

            text: tr.enter_pass_tag_name_descr
        }

        DS3.Spacing {
            height: 24
        }

        DS3.SettingsContainer {
            DS3.SettingsTitleSecondaryNavigation {
                title: tr.userAssociated
                subtitle: popup.currentUser && popup.currentUser.name ? popup.currentUser.name : tr.guest_user

                onEntered: {
                    setChild(
                        "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/tests/GetAccessCardUserPopupStep.qml",
                        {"user": popup.currentUser, "addCardFlowFlag": true, "device": null}
                    )
                }
            }
        }

        DS3.Spacing {
            height: 24
        }

        footer: DS3.ButtonBar {
            hasBackground: true
            button.text: tr.next

            button.onClicked: {
                var deviceName = deviceNameField.atomInput.text.trim()
                if (!deviceName) {
                    Popups.text_popup(tr.information, tr.please_fill_in_all_of_the_required_fields)
                    return
                }
                var color = photoCarousel.colorPeaker.currentColor

                var type = photoCarousel.selectedType

                var user_id = !!popup.currentUser ? popup.currentUser.id : "00000000"
                DesktopPopups.please_wait_popup()
                app.hub_management_module.add_access_card(deviceName, color, type, user_id, popup.mode)
            }
        }
    }
}
