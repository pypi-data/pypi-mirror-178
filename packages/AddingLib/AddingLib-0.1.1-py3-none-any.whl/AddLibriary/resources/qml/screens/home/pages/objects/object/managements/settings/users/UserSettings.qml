import QtQuick 2.7
import QtQuick.Controls 2.2

import "qrc:/resources/js/desktop/popups.js" as Popups
import "qrc:/resources/qml/components/911/DS3/" as DS3

Rectangle {
    property var user: null
    property var sideMargin: 24
    property var devEnable: true

    property var userHubRole: user.hub_role

    Connections {
        target: management

        onUsersChanged: changesChecker.changeInitialValues()
    }

    anchors.fill: parent

    color: ui.ds3.bg.base

    DS3.ChangesChecker {
        id: changesChecker

        listeningValues: [
            notificationsSettings.checked,
            systemSettingsAccess.checked,
            systemSettings.checked,
            nightmodeActivation.checked,
            panic.checked,
            viewCameras.checked,
            switchControls.checked,
            structureSettings.checked,
            eventsSettings.checked,
            chimeActivation.checked
        ]
    }

    DS3.NavBarModal {
        id: usersSettingsBar

        headerText: tr.user_settings
        showCloseIcon: false
        showBackArrow: true
        isRound: false

        onBackAreaClicked: {
            userHubRole == "PRO" ?
            loader.setSource("qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/installers/InstallersSettings.qml", {"user": user}) :
            loader.setSource("qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/users/UsersSettings.qml", {"user": user})
        }
    }

    DS3.ScrollView {
        id: userSettings

        anchors {
            fill: undefined
            top: usersSettingsBar.bottom
            bottom: saveButton.top
            left: parent.left
            right: parent.right
        }

        padding: sideMargin

        DS3.SettingsContainer {
            width: parent.width

            DS3.SettingsSwitch {
                id: userRoleToggle

                visible: hub.hub_type != "YAVIR" && hub.hub_type != "YAVIR_PLUS" && userHubRole != "PRO"
                checked: userHubRole == "MASTER"
                cancelBinding: false

                onSwitched: () => {
                    Popups.please_wait_popup(tr.request_send, 30, [management.usersChanged])
                    let role = checked ? "USER" : "MASTER"
                    let command = {
                        "hub_id": hub.hub_id,
                        "user_id": user.user_id,
                        "user_role": role,
                    }
                    app.hub_management_module.change_user_role(command)
                }
                title: tr.admin
            }

            //--------------------- notifications --------------------------------------
            DS3.SettingsNavigationTitlePrimary {
                visible: hub.hub_type != "YAVIR" && hub.hub_type != "YAVIR_PLUS"
                title: tr.manage_notifications

                onEntered: {
                    loader.setSource("qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/users/Notifications.qml", {"user": user})
                }
            }
            //--------------------- privacy_management --------------------------------------


            DS3.SettingsSwitch {
                id: notificationsSettings

                title: tr.privacy_management_title
                enabled: userHubRole == "USER"
                visible: hub.is_photo_on_demand_compliant && (hub.access_to_slow_pod_allowed || hub.access_to_camera_privacy_settings_allowed || hub.access_to_fast_pod_allowed) && userHubRole != "PRO"
                checked: user.privacy_access_settings
            }
        }

        DS3.Text {
            width: parent.width

            text: tr.privacy_management_desc
            color: ui.ds3.figure.nonessential
            style: ui.ds3.text.body.SRegular
            visible: notificationsSettings.visible
        }

        DS3.Spacing {
            height: sideMargin

            visible: hub.hub_type != "YAVIR" && hub.hub_type != "YAVIR_PLUS"
        }
        //--------------------- permissions --------------------------------------
        DS3.Text {
            text: tr.permissions
            style: ui.ds3.text.special.SectionCaps
            color: ui.ds3.figure.secondary
        }

        DS3.SettingsContainer {
            id: permissionsContainer

            width: parent.width

            DS3.SettingsSwitch {
                id: systemSettingsAccess

                visible: hub.hub_type != "YAVIR" && userHubRole == "MASTER"
                title: tr.system_settings
                checked: user.system_settings_access
            }

            DS3.SettingsSwitch {
                id: systemSettings

                visible:
                    hub.firmware_version_dec < 206000 ?
                    true :
                    !hub.groups_enabled
                title: tr.arm_disarm
                checked: user.arm_disarm_settings_access
            }

            DS3.SettingsSwitch {
                id: nightmodeActivation

                visible: hub.firmware_version_dec >= 206000 && hub.groups_enabled
                enabled: userHubRole == "USER" && devEnable
                title: tr.perimetral_arm_disarm
                checked: user.night_mode_settings_access
            }

            DS3.SettingsSwitch {
                id: panic

                title: tr.panic
                checked: user.panic_settings_access
            }

            DS3.SettingsSwitch {
                id: viewCameras

                visible: !hub.access_to_camera_privacy_settings_allowed && hub.firmware_version_dec < 212001
                title: tr.view_cameras
                checked: user.camera_settings_access
            }

            DS3.SettingsSwitch {
                id: switchControls

                visible: hub.hub_type != "YAVIR" && hub.hub_type != "YAVIR_PLUS"
                title: tr.switch_controls
                checked: user.relay_settings_access
            }

            DS3.SettingsSwitch {
                id: structureSettings

                visible: hub.hub_type != "YAVIR" && hub.hub_type != "YAVIR_PLUS" && userHubRole == "USER"
                title: tr.view_devices_rooms
                checked: user.structure_settings_access
            }

            DS3.SettingsSwitch {
                id: eventsSettings

                visible: hub.hub_type != "YAVIR" && hub.hub_type != "YAVIR_PLUS" && userHubRole == "USER"
                title: tr.view_notifications
                checked: user.events_settings_access
            }

            DS3.SettingsSwitch {
                id: chimeActivation

                visible: hub.chimes_available
                enabled: devEnable
                title: tr.chime_activation
                checked: user.chimes_activation_access
            }
            //--------------------- reset_after_alarm --------------------------------------
            DS3.SettingsNavigationTitlePrimary {
                visible: hub.hub_type != "YAVIR" && hub.hub_type != "YAVIR_PLUS" && hub.firmware_version_dec >= 209100
                title: tr.reset_after_alarm

                onEntered: {
                    loader.setSource("qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/users/RestorationAfterAlarm.qml", {"user": user})
                }
            }
            //--------------------- groups --------------------------------------
            DS3.SettingsNavigationTitlePrimary {
                visible:
                    hub.firmware_version_dec < 206000 ?
                    false :
                    hub.groups_enabled
                title: tr.groups_hub_settings

                onEntered: {
                    loader.setSource("qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/users/Groups.qml", {"user": user})
                }
            }
        }
            //--------------------- user_password_settings --------------------------------------
        DS3.Spacing {
            height: 24

            visible: userPasswordText.visible
        }

        DS3.TitleSection {
            id: userPasswordText

            text: tr.user_passcode_new
            isCaps: true
            isBgTransparent: true
            forceTextToLeft: true
            visible: {
                if (appUser.company_id) return false
                if (["YAVIR", "YAVIR_PLUS"].includes(hub.hub_type)) {
                    if (hub.current_user.hub_role == "PRO" || hub.current_user.user_id == user.user_id) {
                        return hub.has_keypad
                    }
                    return false
                }
                if (hub.firmware_version_dec < 206000) { return false }
                if (hub.current_user.user_id == user.user_id) { return hub.has_keypad }
                return false
            }
        }

        DS3.SettingsContainer {
            DS3.SettingsNavigationTitlePrimary {
                visible: userPasswordText.visible
                title: tr.user_password_settings

                onEntered: {
                    keypadSettingsLoader.setSource("qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/installers/UserKeyPadSettings.qml", {"user": user})
                }
            }
        }

            // --------------------------cancel access------------------------------
        DS3.Spacing {
            height: sideMargin
        }

        DS3.SettingsContainer {
            DS3.ButtonRow {
                id: cancelAccessBtn

                isDanger: true
                text: tr.cancel_access
                enabled: devEnable
                visible: userHubRole == "PRO"

                onClicked: {
                    Popups.please_wait_popup(tr.request_send, 30, [management.usersChanged])
                    if (!app.hub_management_module.user_has_default_permissions(user)) {
                        app.hub_management_module.change_user_access_mask(user, hub.hub_id, "cancel_access", false)
                    } else {
                        management.usersChanged()
                    }
                }
            }

            DS3.ButtonRow {
                id: deleteUserButton

                isDanger: true
                text: tr.delete_user

                onClicked: {
                    Popups.popupByPath("qrc:/resources/qml/components/911/DS3/popups/Dialog.qml", {
                        title: tr.warning,
                        text: tr.you_are_about_to_revoke_hub_access_for_user_are_you_sure,

                        firstButtonCallback: () => {
                            Popups.please_wait_popup()
                            if (userHubRole == "PRO") {
                                loader.setSource("qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/installers/InstallersSettings.qml", {"user": user})
                            } else {
                                loader.setSource("qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/users/UsersSettings.qml", {"user": user})
                            }
                            app.hub_management_module.delete_user(user, hub.hub_id)
                        },
                        firstButtonText: tr.revoke,
                        isFirstButtonRed: true,
                        secondButtonText: tr.cancel,
                        isVertical: true,
                    })
                }
            }
        }

        DS3.InfoFooter {
           id: usrId

           subtitleUpper.text: util.insert(tr.user_id, [user.index])
           footerType: DS3.InfoFooter.FooterType.User
        }
    }

    DS3.ButtonBar {
        id: saveButton

        anchors {
            bottom: parent.bottom
            horizontalCenter: parent.horizontalCenter
        }

        buttonText: tr.save
        hasBackground: true
        enabled: changesChecker.hasChanges

        button.onClicked: {
            Popups.please_wait_popup(tr.request_send, 30, [management.usersChanged])
            let settings = {
                "privacy_access_settings": notificationsSettings.checked,
                "system_settings": systemSettingsAccess.checked,
                "panic_settings": panic.checked,
                "camera_settings": viewCameras.checked,
                "relay_settings": switchControls.checked,
                "structure_settings": structureSettings.checked,
                "events_settings": eventsSettings.checked,
                "chimes_settings": chimeActivation.checked
            }

            if (systemSettings.visible) settings["arm_disarm_settings"] = systemSettings.checked
            if (nightmodeActivation.visible) settings["night_mode_settings"] = nightmodeActivation.checked
            if (user.hub_binding_role == "MASTER") settings["user_permissions_update"] = true

            app.hub_management_module.change_user_access_mask(user, hub.hub_id, settings)
        }
    }

    Loader {
        id: groupsLoader

        anchors.fill: parent
    }

    Loader {
        id: keypadSettingsLoader

        anchors.fill: parent
    }

// добавление ключа к очень старым Яворам.
// НЕ работает (и в этом приложе никогда не работало). Возможно, будет тикет на это.

//            Item {
//                height: 48
//                width: parent.width
//
//                visible: true
//                visible: {
//                    if (hub.hub_type == "YAVIR" || hub.hub_type == "YAVIR_PLUS") {
//                        if (hub.firmware_version_dec < 207002) {
//                            return true
//                        }
//                        return false
//                    }
//                    return false
//                }
//
//                Item {
//                    height: parent.height
//                    width: parent.width - 70
//
//                    anchors.horizontalCenter: parent.horizontalCenter
//
//                    Text {
//                        anchors.centerIn: parent
//                        font.family: roboto.name
//                        font.pixelSize: 14
//                        color: ui.colors.green1
//                        text: {
//                            if (user.access_key_id == "0000000000000000") return tr.add_key
//                            return tr.delete_key
//                        }
//
//                        MouseArea {
//                            anchors.fill: parent
//                            enabled: devEnable
//                            hoverEnabled: true
//                            onEntered: {
//                                parent.color = "#fdfdfd"
//                            }
//                            onExited: {
//                                parent.color = "#60e3ab"
//                            }
//                            onClicked: {
//                                if (user.access_key_id == "0000000000000000") {
//                                    client.user_reg_key(user.user_id)
//                                } else {
//                                    client.user_del_key(user)
//                                }
//                            }
//                        }
//                    }
//                }
//            }


//    Component.onCompleted: {
//        if (user.user_id == hub.current_user.user_id && !hub.current_user.common_params_access) {
//            keypadSettingsLoader.setSource("qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/installers/UserKeyPadSettings.qml", {"user": user})
//        }
//    }
}