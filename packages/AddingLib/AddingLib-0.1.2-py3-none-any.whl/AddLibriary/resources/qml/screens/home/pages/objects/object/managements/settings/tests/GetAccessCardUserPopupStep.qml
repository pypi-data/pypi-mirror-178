import QtQuick 2.7
import QtQuick.Controls 2.2
import QtGraphicalEffects 1.12

import "qrc:/resources/qml/components/desktop"
import "qrc:/resources/qml/components/911/DS3/" as DS3
import "qrc:/resources/qml/components/911/DS3/popups" as DS3Popups
import 'qrc:/resources/js/desktop/popups.js' as Popups
import "qrc:/resources/js/images.js" as Images


DS3Popups.PopupStep {
    id: getUserPopup

    property var user: null

    property var selected_user_id: !addCardFlowFlag && device && device.associated_user_id ? device.associated_user_id : (!!user ? user.id : null)
//  If adding pass/tag flow (not settings)
    property bool addCardFlowFlag: false

    Connections {
        target: app

        onActionSuccess: {
            goBack()
        }

        onAltActionSuccess: {
            goBack()
        }
    }

    sidePadding: 24
    title: tr.user

    DS3.ChangesChecker {
        id: changesChecker

        listeningValues: [
            guestUser.selected,
            selected_user_id
        ]
    }

    DS3.Spacing {
        height: 24
    }

    DS3.SettingsContainer {
        width: parent.width

        DS3.UserSelectionSingle {
            id: guestUser

            selected: selected_user_id == "00000000" || !selected_user_id
            imageSource: Images.get_image("22", "Small")
            atomTitle.title: tr.guest_user

            onSelectedCallback: () => {
                selected_user_id = "00000000"
            }
        }
    }

    DS3.Spacing {
        height: 24
    }

    DS3.SettingsContainer {
        width: parent.width

        ListView {
            id: usersView

            width: parent.width
            height: contentHeight

            spacing: 1
            interactive: false
            model: users.normalized_users.names.map( (name, index) => {
                return {
                    "name": name,
                    "id": users.normalized_users.user_ids[index],
                    "image": users.normalized_users.user_pictures[index],
                    "role": users.normalized_users.roles[index],
                }
            } )

            delegate: DS3.UserSelectionSingle {
                property var user_id: modelData.id

                objectName: "delegate"
                imageSource: !!modelData.image && modelData.image != "WRONG" ? modelData.image : ""
                atomTitle.title: modelData.name ? modelData.name : tr.user_was_deleted
                role: {
                    if (!modelData || !modelData.role) return ""
                    if (modelData.role == "USER") return tr.user
                    if (modelData.role == "MASTER") return tr.admin
                    if (modelData.role == "PRO") return tr.pro
                    return ""
                }
                selected: modelData.id == selected_user_id

                onSelectedCallback: () => {
                    selected_user_id = modelData.id
                }
            }
        }
    }

    DS3.Spacing {
        height: 24
    }

    footer: DS3.ButtonBar {
        id: saveButton

        width: parent.width

        button.text: tr.save
        hasBackground: true
        enabled: changesChecker.hasChanges

        button.onClicked: {
            if (addCardFlowFlag) {
                popup.currentUser = management.users.get_user(selected_user_id)
                goBack()
                return
            }

            var settings = {
                "associated_user_id": selected_user_id,
                "_params": {
                    "alt_action_success": true,
                },
            }

            Popups.please_wait_popup()
            app.hub_management_module.apply_update(management, device, settings)
        }
    }
}
