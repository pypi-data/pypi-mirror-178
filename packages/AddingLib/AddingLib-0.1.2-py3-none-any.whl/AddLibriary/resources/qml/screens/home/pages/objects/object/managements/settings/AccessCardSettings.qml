import QtQuick 2.7
import QtQuick.Controls 2.2

import "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/settings/" as Settings
import "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/parts/" as Parts
import "qrc:/resources/qml/components/911/DS3" as DS3
import "qrc:/resources/js/desktop/popups.js" as Popups
import "qrc:/resources/qml/components/911/DS3/popups" as DS3Popups

// Because we need to change header in child components
DS3Popups.PopupMultistep {
    id: popup

//  QObject of device
    property var device: null
//  Whether device is enabled
    property var devEnable: hub.online && device.online

    width: 500

    maxStepHeight: maxPopupHeight - headerItem.height - footerItem.height
    height: maxPopupHeight
    closePolicy: currentStepIndex == 0 ? Popup.CloseOnEscape : Popup.NoAutoClose

    firstStepComponent: Parts.CommonSettings {
        id: accessCardSettings

        property var all_selected:  util.all_selected_access_card_groups(groups, selected)
        property var groups: management.filtered_groups.get_all_groups()
        property var selected: device.get_selected_groups()
        property var currentUser: management.users.get_user(device.associated_user_id)

        Connections {
            target: app.hub_management_module

            onCardNotAdded: {
                if (["USER_TIMEOUT", "TIMEOUT"].includes(error)) {
                    Popups.text_popup(tr.error, tr.acc_card_user_action_timeout0)
                }
                if (error == "NO_ANSWER") {
                    Popups.text_popup(tr.error, tr.acc_card_reader_timeout0)
                }
            }

            onDeleteWithCardStarted: {
                setChild(
                    "qrc:/resources/qml/screens/home/pages/objects/object/popups/AccessCardActivateKeypadPopup.qml",
                    {
                        "type": deviceImageItem.selectedType,
                        "color": deviceImageItem.colorPeaker.currentColor,
                        "user_id": device.associated_user_id,
                        "isDeleteFlow": true,
                    }
                )
            }

            onCardDeleted: {
                popup.close()
            }
        }

        Connections {
            target: app

            onAltActionSuccess: {
                popup.close()
            }
        }

        settingsForChangesChecker: [
            deviceImageItem.selectedType,
            deviceImageItem.colorPeaker.currentColor
        ]

        generateSettings: () => {
            var settings = {
                "name": {"name": deviceName.atomInput.text.trim()},
                "attribute": {
                    "type": deviceImageItem.selectedType,
                    "color": deviceImageItem.colorPeaker.currentColor,
                },
                "_params": {
                    "alt_action_success": true,
                },
            }

            // Temporary solution for backward compatibility
            settings["_refactored"] = true

            return settings
        }

        header: DS3.NavBarModal {
            headerText: accessCardSettings.title
        }

        deviceImageComponent: DS3.CarrouselContainerStack {
            id: photoCarousel

            selectedType: device.card_type
            colorPeaker.currentColor: device.color
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

        roomsCombobox.visible: false

        DS3.SettingsContainer {
            width: parent.width

            DS3.SettingsTitleSecondaryNavigation {
                id: userAssociated

                title: tr.userAssociated
                subtitle: {
                    if (device.associated_user_id == "00000000") return tr.guest_user
                    return accessCardSettings.currentUser && accessCardSettings.currentUser.name ?
                        accessCardSettings.currentUser.name :
                        tr.user_was_deleted
                }

                onEntered: {
                    setChild(
                        "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/tests/GetAccessCardUserPopupStep.qml",
                        {"user": accessCardSettings.currentUser}
                    )
                }
            }

            DS3.SettingsTitleSecondaryNavigation {
                id: armingDisarming

                title: tr.arm_permission_with_group
                subtitle: {
                    var existing_selected = util.all_selected_existing_access_card_groups(groups, accessCardSettings.selected)
                    if (accessCardSettings.all_selected && device.perimeter_arm) {
                        return tr.full_hub_access
                    }
                    if (existing_selected.length && device.perimeter_arm) {
                        return tr.partial_access
                    }
                    if (existing_selected.length) {
                        return util.insert(tr.scenario_arm_disarm_groups_selected, [existing_selected.length])
                    }
                    if (device.perimeter_arm) {
                        return tr.perimeter
                    }
                    if (!existing_selected.length && !device.perimeter_arm) {
                        return tr.no_hub_access
                    }
                }
                visible: device.associated_user_id == "00000000" && hub.groups_enabled

                onEntered: {
                    setChild(
                        "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/tests/GroupsArmDisarmPermissionsPopupStep.qml",
                    )
                }
            }

            DS3.SettingsSwitch {
                id: deactivation

                title: tr.card_is_active
                checked: device.card_enabled
                cancelBinding: false

                onSwitched: () => {
                    Popups.waitPopup(app.hub_management_module.cardActiveStateUpdated)
                    app.hub_management_module.update_card_state(device.id, !checked)
                }
            }
        }

        DS3.Spacing {
            height: 24
        }

        DS3.SettingsContainer {
            width: parent.width

            Parts.ManualNav {}
        }
    }
}