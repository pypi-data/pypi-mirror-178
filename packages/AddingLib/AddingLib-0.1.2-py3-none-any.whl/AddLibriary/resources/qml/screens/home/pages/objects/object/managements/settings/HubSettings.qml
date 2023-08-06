import QtQuick 2.7
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.3
import QtGraphicalEffects 1.12

import "qrc:/resources/qml/components/desktop/"
import "qrc:/resources/qml/screens/home/pages/objects/object/managements/views"
import "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/parts/"
import "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/users/"

import "qrc:/resources/js/desktop/popups.js" as Popups
import "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/settings/" as Settings
import "qrc:/resources/qml/components/911/DS3" as DS3

DS3.Popup {
    id: popup

    width: 875
    height: maxPopupHeight

    property var device: null

    property var currentIndex: -1

    property var devEnable: not_armed && hub.online && !hub.config_migration.inited

    property var not_armed: {
        if (!hub) return false

        if (hub.groups_enabled && ["NO_STATE_WITH_GROUPS_INFO", "DISARMED", "DISARMED_NIGHT_MODE_OFF"].includes(hub.state_with_groups)) return true
        if (!hub.groups_enabled && ["NO_STATE_INFO", "DISARMED"].includes(hub.state)) return true

        return false
    }

    property var selectedTab: null

    // migration
    property var filteredAvailableHubsWithoutCurrent: {
        return app.filtered_available_hubs_without_current
    }

    property var filteredNotAvailableHubsWithoutCurrent: {
        return app.filtered_not_available_hubs_without_current
    }

    property var donorManagement: {
        return app.donor_management
    }

    property var donorHubDevices: {
        return donorManagement.devices
    }

    property var donorHubRooms: {
        return donorManagement.rooms
    }

    property var donorHubGroups: {
        return donorManagement.groups
    }

    property var donorHubUsers: {
        return donorManagement.users
    }

    property var donorHubScenarios: {
        return donorManagement.scenarios
    }

    property var donorHub: {
        return donorManagement.devices.hub
    }

    property var filteredWithoutButtonsDevices: {
        return management.filteredWithoutButtonsDevices
    }

    property var filteredButtonsDevices: {
        return management.filteredButtonsDevices
    }

    property var filteredWithoutButtonsDevicesInProgress: {
        return management.filteredWithoutButtonsDevicesInProgress
    }

    property var filteredButtonsDevicesInProgress: {
        return management.filteredButtonsDevicesInProgress
    }

    property var openCompanies: false

    property var devices: {
        return management.devices
    }
    // migration end

    property var sideMargin: 24

    property bool isDiscardChanges: false

    Connections {
        target: hub

        onDataChanged: {
            nameField.atomInput.text = device.name
        }
    }

    property var hubSettingsContext: hubPageLoader.contextTarget.hubSettings

    Component.onCompleted: {
        let hubTabs = hubTabsRepeater.model
        let findTab = false

        hubTabs.every((tab, index) => {
            if (tab.isEnabled && !tab.link) {
                currentIndex = index
                loader.setSource(tab.source)
                loader.item.enabled = tab.contentEnabled == undefined ? true : tab.contentEnabled
                findTab = true
                return false
            }
            return true
        })
        if (findTab) return
        if (hubMigrationTab.enabled) {
            filteredAvailableHubsWithoutCurrent.set_search_filter("")
            filteredNotAvailableHubsWithoutCurrent.set_search_filter("")
            app.get_hub_migration_donors(hub.hub_id, management)
            filteredAvailableHubsWithoutCurrent.set_filter(hub.hub_id)
            filteredNotAvailableHubsWithoutCurrent.set_filter(hub.hub_id)
            currentIndex = -1
            hubMigrationTab.active = true
            loader.setSource("qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/migration/MigrationSettings.qml")
            findTab = true
        } else if (!hub.online) {
            loader.setSource("qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/HubOfflineScreen.qml")
        } else {
            loader.setSource("qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/NoHubPermissionsScreen.qml")
        }
    }

    Behavior on width {
        NumberAnimation { duration: 200 }
    }

    closePolicy: isDiscardChanges ? Popup.NoAutoClose : Popup.CloseOnEscape | Popup.NoAutoClose
    hasCrossButton: false
    backgroundColor: ui.ds3.bg.low
    sideMargins: 0

    header: DS3.NavBarModal {
        headerText: tr.hub_settings

        onClosed: () => {
            if (isDiscardChanges) {
                var discard_changes_popup = Popups.popupByPath("qrc:/resources/qml/components/911/DS3/popups/Dialog.qml", {
                    title: tr.dont_save_title,
                    text: tr.dont_save_descr,
                    firstButtonText: tr.discard_changes_button,
                    isFirstButtonRed: true,
                    firstButtonCallback: () => {
                        popup.close()
                    },
                    secondButtonCallback: () => {
                        discard_changes_popup.close()
                    },
                    secondButtonText: tr.back_editing_button,
                    secondButtonIsOutline: true,
                    isVertical: true,
                })
            } else popup.close()
        }
    }

    footer: Item { height: 0 }

    Item {
        width: parent.width
        height: popup.height - headerItem.height

        Rectangle {
            id: rightSide

            width: 500
            height: leftSide.height - anchors.topMargin

            anchors {
                top: parent.top
                right: parent.right
                topMargin: 1
            }
            color: ui.ds3.bg.base

            Loader {
                id: loader

                width: 500
                height: parent.height

                anchors.right: parent.right
            }
        }

        Rectangle {
            id: leftSide

            width: 375
            height: parent.height

            anchors {
                top: parent.top
                left: parent.left
            }

            color: ui.ds3.bg.low

            DS3.ScrollView {
                width: 375
                height: parent.height

                anchors {
                    fill: undefined
                    left: parent.left
                    top: popup.header.bottom
                    bottom: popup.bottom
                    horizontalCenter: parent.horizontalCenter
                }
                padding: 0

                DS3.Spacing {
                    height: 24
                }

                HubImage {
                    width: 120
                    height: 120

                    opacity: enabled ? 1 : 0.3

                    anchors.horizontalCenter: parent.horizontalCenter
                }

                DS3.Spacing {
                    height: 24
                }

                DS3.SettingsContainer {
                    width: parent.width - sideMargin * 2

                    anchors.horizontalCenter: parent.horizontalCenter

                    DS3.InputSingleLine {
                        id: nameField

                        enabled: devEnable && hub.current_user.advanced_params_access
                        atomInput {
                            label: tr.name
                            placeholderText: tr.hub_name
                            text: device.name

                            onTextChanged: {
                                nameField.atomInput.text = Qt.binding(() => device.name)
                            }
                        }

                        DS3.MouseArea {
                            hoverEnabled: true
                            cursorShape: Qt.PointingHandCursor
                            onClicked: {
                                if (!hub.current_user.common_params_access) return
                                if (!devEnable) return
                                Popups.change_hub_name_popup()
                            }
                        }
                    }
                }

                DS3.Spacing {
                    height: 24
                }

                DS3.SettingsContainer {

                    width: parent.width - sideMargin * 2

                    anchors.horizontalCenter: parent.horizontalCenter

                    Repeater {
                        id: hubTabsRepeater

                        property var userGuideLink: app.hub_management_module.get_manual_link(device)

                        width: parent.width

                        model: [
                            {
                                title: tr.users,
                                icon: "qrc:/resources/images/Athena/settings_icons/UserSettings-L.svg",
                                source: "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/users/UsersSettings.qml",
                                isEnabled: devEnable && hub.current_user.common_params_access
                            },
                            {
                                title: tr.log_types_1,
                                icon: "qrc:/resources/images/Athena/settings_icons/Ethernet-L.svg",
                                source: "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/ethernet/HubEthernetSettings.qml",
                                isEnabled: devEnable && hub.current_user.advanced_params_access
                            },
                            {
                                title: "Wi-Fi",
                                icon: "qrc:/resources/images/Athena/settings_icons/WiFi-L.svg",
                                visible: hub.hub_type == "HUB_PLUS" || hub.hub_type == "HUB_2_PLUS",
                                source: "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/wifi/WifiSettings.qml",
                                isEnabled: devEnable && hub.current_user.advanced_params_access
                            },
                            {
                                title: tr.gsm,
                                icon: "qrc:/resources/images/Athena/settings_icons/GSM-L.svg",
                                source: "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/gsm/GSMSettings.qml",
                                isEnabled: devEnable && hub.current_user.advanced_params_access
                            },
                            {
                                title: tr.geofence,
                                visible: __geofence_features__,
                                icon: "qrc:/resources/images/Athena/settings_icons/Geofence-L.svg",
                                source: "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/geofence/GeofenceSettings.qml",
                                isEnabled: devEnable
                            },
                            {
                                title: tr.keypad_access_codes_menu,
                                visible: hub.firmware_version_dec >= 213001 && !["HUB", "YAVIR"].includes(hub.hub_type),
                                icon: "qrc:/resources/images/Athena/settings_icons/TwoFactorAuthenticationSettings-L.svg",
                                source: "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/access_codes/AccessCodesSettings.qml",
                                isEnabled: devEnable && hub.current_user.advanced_params_access
                            },
                            {
                                title: tr.groups_hub_settings,
                                icon: "qrc:/resources/images/Athena/settings_icons/Groups-L.svg",
                                source: "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/groups/GroupsSettings.qml",
                                isEnabled: devEnable && hub.current_user.group_edit_access
                            },
                            {
                                title: tr.scenario_arm_disarm_schedule,
                                icon: "qrc:/resources/images/Athena/settings_icons/Scenarios-L.svg",
                                source: "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/hub_scenarios/ArmDisarmScenariosScreen.qml",
                                isEnabled: devEnable && hub.current_user.scenario_edit_access
                            },
                            {
                                title: tr.detection_zone_test,
                                icon: "qrc:/resources/images/Athena/settings_icons/DetectionZoneSettings-L.svg",
                                visible: hub.hub_type != "YAVIR",
                                source: "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/zonetest/ZoneTestSettings.qml",
                                isEnabled: devEnable && hub.current_user.advanced_params_access
                            },
                            {
                                title: hub.hub_type == "HUB_FIBRA" ? "Jeweller / Fibra" : "Jeweller",
                                icon: "qrc:/resources/images/Athena/settings_icons/Jeweller-L.svg",
                                visible: hub.hub_type == "YAVIR" ? false : true,
                                source: "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/jeweller/JewellerSettings.qml",
                                isEnabled: devEnable && hub.current_user.advanced_params_access
                            },
                            {
                                title: tr.wires_settings,
                                icon: "qrc:/resources/images/Athena/settings_icons/Wires-L.svg",
                                visible: hub.hub_type == "HUB_FIBRA",
                                source: "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/wires/WiresSettings.qml",
                                isEnabled: devEnable && hub.current_user.advanced_params_access
                            },
                            {
                                title: tr.service,
                                icon: "qrc:/resources/images/Athena/settings_icons/ServiceSettings-L.svg",
                                source: "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/service/ServiceSettings.qml",
                                isEnabled: devEnable && hub.current_user.advanced_params_access
                            },
                            {
                                title: tr.security_companies,
                                icon: "qrc:/resources/images/Athena/settings_icons/SecurityCompanies-L.svg",
                                source: "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/companies/CompaniesSettings.qml",
                                isEnabled: devEnable && hub.current_user.advanced_params_access
                            },
                            {
                                title: tr.monitoring_station,
                                icon: "qrc:/resources/images/Athena/settings_icons/Monitoring-L.svg",
                                source: "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/monitoring/MonitoringSettings.qml",
                                isEnabled: devEnable && hub.current_user.advanced_params_access
                            },
                            {
                                title: tr.installers_companies_menu_title,
                                icon: "qrc:/resources/images/Athena/settings_icons/Installer-L.svg",
                                source: "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/installers/InstallersSettings.qml",
                                isEnabled: devEnable && (hub.current_user.common_params_access || (!appUser.company_id && hub.has_keypad)),
                            },
                            {
                                title: tr.address,
                                icon: "qrc:/resources/images/Athena/settings_icons/Address-L.svg",
                                visible: !appUser.company_id && hub.hub_type != "YAVIR",
                                source: "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/address/AddressSettings.qml",
                                isEnabled: devEnable&& hub.current_user.common_params_access
                            },
                            {
                                title: tr.user_guide,
                                icon: "qrc:/resources/images/Athena/settings_icons/UserGuide-L.svg",
                                link: userGuideLink,
                                isEnabled: true,
                                visible: !hub.hub_type.includes("YAVIR")
                            },
                            {
                                title: "Certification",
                                icon: "qrc:/resources/images/Athena/settings_icons/Geofence-L.svg",
                                source: "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/certification/CertificationSettings.qml",
                                isEnabled: !certificationTabEasterEgg.hidden
                            }
                        ]

                        delegate: DS3.SettingsNavigationTitlePrimary {
                            title: modelData.title
                            icon: modelData.icon
                            visible: modelData.visible != false && (
                                modelData.title != "Certification" || !certificationTabEasterEgg.hidden
                            )
                            enabled: modelData.isEnabled
                            color: index == currentIndex ? ui.ds3.special.selection : ui.ds3.bg.highest

                            onEntered: {
                                // When we have unsaved changes at access codes page
                                if (isDiscardChanges) {
                                    var discardChangesPopup = Popups.popupByPath("qrc:/resources/qml/components/911/DS3/popups/Dialog.qml", {
                                        title: tr.dont_save_title,
                                        text: tr.dont_save_descr,
                                        firstButtonText: tr.discard_changes_button,
                                        isFirstButtonRed: true,
                                        firstButtonCallback: () => {
                                            if (modelData.source) {
                                                if (currentIndex == index) return
                                                hubMigrationTab.active = false
                                                currentIndex = index
                                                loader.setSource(modelData.source)
                                                loader.item.enabled = modelData.contentEnabled == undefined ? true : modelData.contentEnabled
                                            }
                                            if (modelData.link) Qt.openUrlExternally(modelData.link)
                                            isDiscardChanges = false
                                        },
                                        secondButtonCallback: () => {
                                            discardChangesPopup.close()
                                        },
                                        secondButtonText: tr.back_editing_button,
                                        secondButtonIsOutline: true,
                                        isVertical: true,
                                    })
                                    return
                                }

                                if (modelData.source) {
                                    if (currentIndex == index) return
                                    hubMigrationTab.active = false
                                    currentIndex = index
                                    loader.setSource(modelData.source)
                                    loader.item.enabled = modelData.contentEnabled == undefined ? true : modelData.contentEnabled
                                }
                                if (modelData.link) Qt.openUrlExternally(modelData.link)
                            }
                        }
                    }
                }

                DS3.Spacing {
                    width: parent.width
                    height: 24

                    DS3.MouseArea {
                        id: certificationTabEasterEgg

                        // Whether certification tab is hidden
                        property bool hidden: true

                        enabled: __hub_certification_features__
                        cursorShape: Qt.ArrowCursor
                        pressAndHoldInterval: 3000
                        onPressAndHold: hidden = false
                    }
                }

                Column {
                    width: parent.width

                    visible: hub.migration_available

                    DS3.SettingsContainer {
                        width: parent.width - sideMargin * 2

                        anchors.horizontalCenter: parent.horizontalCenter

                        DS3.SettingsNavigationTitlePrimary {
                            id: hubMigrationTab

                            property bool active: false

                            title: tr.hub_migration
                            icon: "qrc:/resources/images/Athena/settings_icons/DataImport-L.svg"
                            enabled: hub.online && not_armed && hub.current_user.advanced_params_access
                            color: active ? ui.ds3.special.selection : ui.ds3.bg.highest

                            onEntered: {
                                if (hubMigrationTab.active == true) return
                                filteredAvailableHubsWithoutCurrent.set_search_filter("")
                                filteredNotAvailableHubsWithoutCurrent.set_search_filter("")
                                app.get_hub_migration_donors(hub.hub_id, management)
                                filteredAvailableHubsWithoutCurrent.set_filter(hub.hub_id)
                                filteredNotAvailableHubsWithoutCurrent.set_filter(hub.hub_id)
                                currentIndex = -1
                                hubMigrationTab.active = true
                                loader.setSource("qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/migration/MigrationSettings.qml")
                            }
                        }
                    }

                    DS3.Spacing {
                        height: 4
                    }

                    DS3.Text {
                        width: parent.width - sideMargin * 2

                        anchors.horizontalCenter: parent.horizontalCenter

                        text: tr.hub_migration_info
                        style: ui.ds3.text.body.MRegular
                        color: ui.ds3.figure.secondary
                    }

                    DS3.Spacing {
                        height: 24
                    }
                }

                DS3.SettingsContainer {
                    width: parent.width - sideMargin * 2

                    anchors.horizontalCenter: parent.horizontalCenter

                    DS3.ButtonRow {
                        id: unpairButton

                        enabled: {
                            if (appUser.company_id) return false
                            return !hub.config_migration.inited
                        }
                        text: tr.unpair
                        isDanger: true

                        onClicked: {
                            Popups.hub_delete_popup()
                        }

                        /* ------------------------------------------------ */
                        /* desktop tests */
                        Accessible.name: "delete_hub_" + hub.hub_id + "_button"
                        Accessible.description: "<button enabled=" + Accessible.checkable + ">" + text + "</button>"
                        Accessible.role: Accessible.Button
                        Accessible.checkable: visible && enabled
                        Accessible.onPressAction: {
                            if (!Accessible.checkable) return
                            unpairButton.clicked(true)
                        }
                        /* ------------------------------------------------ */
                    }
                }

                DS3.Spacing {
                    height: 24
                }
            }
        }
    }
}