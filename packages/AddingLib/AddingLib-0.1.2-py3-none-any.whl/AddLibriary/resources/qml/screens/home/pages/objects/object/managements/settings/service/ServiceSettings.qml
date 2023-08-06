import QtQuick 2.7
import QtQuick.Controls 2.2

import "qrc:/resources/js/desktop/popups.js" as Popups
import "qrc:/resources/qml/components/911/DS3/" as DS3

Rectangle {
    id: serviceSettings

    property var sideMargin: 24
    // If setting wizard has started
    property var isWizard: false
    // Screens that aren't PD compliant
    property var notCompliantWizardScreens : []
    // Last screen where we were (to make component on complete just at first time)
    property int lastScreen: 0

    property var devEnable: true

    signal startWizard()
    signal closeWizard()

    onStartWizard: {
        serviceSettings.isWizard = true
        advancedSettingsLoader.setSource("qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/service/wizard/StartWizardScreen.qml")
    }

    onCloseWizard: {
        serviceSettings.isWizard = false
        serviceSettings.notCompliantWizardScreens = []
        lastScreen = 0
        advancedSettingsLoader.setSource("")
    }

    Connections {
        target: timezones

        onTimezonesLoaded: {
            if (hub.hub_timezone != "00") {
                timeZones.subtitle = timezones.find(hub.hub_timezone)
                changesChecker.changeInitialValues()
            }
        }
    }

    Connections {
        target: app

        onActionSuccess: {
            changesChecker.changeInitialValues()
        }
    }

    color: ui.ds3.bg.base

    Loader {
        id: timezoneLoader

        anchors.fill: parent

        z: serviceSettings.z * 2 + 1
    }

    Loader {
        id: advancedSettingsLoader

        anchors.fill: parent

        z: 3
    }

    DS3.ChangesChecker {
        id: changesChecker

        listeningValues: [
            timeZones.subtitle,
            ledBrightnessSlider.value,
            autoUpdateSwitch.checked,
            logsPicker.currentIndex,
        ]
    }

    DS3.NavBarModal {
        id: serviceSettingsBar

        headerText: tr.service
        showCloseIcon: false
        isRound: false
    }

    DS3.ScrollView {
        id: serviceSettingsScrollView

        anchors {
            fill: undefined
            top: serviceSettingsBar.bottom
            bottom: saveButton.top
            left: parent.left
            right: parent.right
        }

        padding: sideMargin

        DS3.SettingsContainer {
            width: parent.width

            anchors.horizontalCenter: parent.horizontalCenter

            DS3.SettingsNavigationTitlePrimary {
                id: timeZones

                property var selectedId: null

                title: tr.hub_time_zone
                subtitle: {
                    if (!hub.hub_timezone.length || hub.hub_timezone == "00"){
                        return ""
                    }
                    selectedId = hub.hub_timezone
                    if (timezones.find(hub.hub_timezone).length)
                        return timezones.find(hub.hub_timezone)
                    return hub.hub_timezone
                }
                visible: hub.firmware_version_dec >= 207181

                onEntered: {
                    timezoneLoader.setSource(
                        "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/service/Timezones.qml",
                        {timeZones: timeZones}
                    )
                }
            }
        }

        DS3.Spacing {
            height: 24
        }

        DS3.SettingsContainer {
            width: parent.width

            anchors.horizontalCenter: parent.horizontalCenter

            DS3.SettingsSliderIcon {
                id: ledBrightnessSlider

                enabled: devEnable
                value: hub.led_brightness
                title: tr.led_brightness
                from: 1
                to: 10
                stepSize: 1
                sideIcons: ["qrc:/resources/images/Athena/common_icons/BrightnessLow-M.svg", "qrc:/resources/images/Athena/common_icons/BrightnessHigh-M.svg"]
            }
        }

        DS3.Spacing {
            height: 4
        }

        DS3.Text {
            width: parent.width

            style: ui.ds3.text.body.MRegular
            text: tr.led_brightness_hint
            color: ui.ds3.figure.secondary
        }

        DS3.Spacing {
            height: 24
        }

        DS3.SettingsContainer {
            width: parent.width

            anchors.horizontalCenter: parent.horizontalCenter

            DS3.SettingsSwitch {
                id: autoUpdateSwitch

                enabled: devEnable
                visible: hub.firmware_version_dec >= 201000
                title: tr.firmware_auto_update
                checked: hub.hub_autoupdate
            }
        }

        DS3.Spacing {
            height: autoUpdateSwitch.visible ? 24 : 0
        }

        DS3.SettingsContainer {
            width: parent.width

            anchors.horizontalCenter: parent.horizontalCenter

            DS3.SettingsPickerTitleSecondary {
                id: logsPicker

                enabled: devEnable
                model: {
                    if (hub.hub_type == "HUB_PLUS" || hub.hub_type == "HUB_2_PLUS") {
                        return [tr.off, tr.log_types_1, "Wi-Fi"]
                    } else {
                        return [tr.off, tr.log_types_1]
                    }
                }
                currentIndex: hub.logs_state - 1
                atomTitle.title: tr.hub_logs
            }
        }

        DS3.Spacing {
            height: 4
        }

        DS3.Text {
            width: parent.width

            style: ui.ds3.text.body.MRegular
            text: tr.hub_logs_hint
            color: ui.ds3.figure.secondary
        }

        DS3.Spacing {
            height: 24
        }

        DS3.TitleSection {
            text: tr.advanced_settings
            isBgTransparent: true
            forceTextToLeft: true
            isCaps: true
        }

        ////////// advanced settings //////////
        Column {
            width: parent.width

            visible: !appCompany.company_id && hub.firmware_version_dec >= 209100

            DS3.SettingsContainer {
                width: parent.width

                DS3.SettingsNavigationTitlePrimary {
                    title: tr.PD_compliance_wizard
                    icon: "qrc:/resources/images/Athena/common_icons/PD6662Settings-L.svg"

                    onEntered: {
                        Popups.wizard_action_popup(
                            tr.we_already_set_up_all_required_settings_for_you,
                            tr.start_managing_security_of_your_home,
                            tr.start,
                            function() {
                                serviceSettings.startWizard()
                            }
                        );
                    }
                }
            }

            DS3.Comment {
                width: parent.width

                text: tr.PD_compliance_wizard_info
            }

            DS3.Spacing {
                height: 24
            }
        }

        DS3.SettingsContainer {
            width: parent.width

            anchors.horizontalCenter: parent.horizontalCenter

            DS3.SettingsNavigationTitlePrimary {
                id: serverConnection

                title: tr.server_connection

                onEntered: {
                    advancedSettingsLoader.setSource("qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/service/advanced_settings/ServerConnection.qml")
                }
            }

            DS3.SettingsNavigationTitlePrimary {
                id: postAlarmIndication

                title: tr.sirens

                onEntered: {
                    advancedSettingsLoader.setSource("qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/service/advanced_settings/PostAlarmIndication.qml")
                }
            }

            DS3.SettingsNavigationTitlePrimary {
                id: fireDetectors

                title: tr.fire_detectors
                visible: hub.hub_type != "YAVIR" && hub.firmware_version_dec >= 201000

                onEntered: {
                    advancedSettingsLoader.setSource("qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/service/advanced_settings/FireDetectors.qml")
                }
            }

            DS3.SettingsNavigationTitlePrimary {
                id: systemIntegrityCheck

                title: tr.prevention_of_arming
                visible: hub.firmware_version_dec >= 205000

                onEntered: {
                    advancedSettingsLoader.setSource("qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/service/advanced_settings/SystemIntegrityCheck.qml")
                }
            }

            DS3.SettingsNavigationTitlePrimary {
                id: alarmConfirmation

                title: tr.british_standard_setting
                visible:
                (
                    ((hub.hub_type == "YAVIR" || hub.hub_type == "YAVIR_PLUS") && hub.firmware_version_dec >= 209100)
                    || hub.firmware_version_dec >= 207186
                )

                onEntered: {
                    advancedSettingsLoader.setSource("qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/service/advanced_settings/AlarmConfirmation.qml")
                }
            }

            DS3.SettingsNavigationTitlePrimary {
                id: restoreAfterAlarm

                title: tr.reset_after_alarm
                visible: {
                    if (hub.hub_type == "YAVIR" || hub.hub_type == "YAVIR_PLUS" || hub.firmware_version_dec < 209100) {
                        return false
                    }
                    return true
                }

                onEntered: {
                    advancedSettingsLoader.setSource("qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/service/advanced_settings/RestoreAfterAlarm.qml")
                }
            }

            DS3.SettingsNavigationTitlePrimary {
                id: armingDisarmingFlow

                title: tr.arming_disarming
                visible: {
                    if (hub.hub_type == "YAVIR" || hub.hub_type == "YAVIR_PLUS" || hub.firmware_version_dec < 209100) {
                        return false
                    }
                    return true
                }

                onEntered: {
                    advancedSettingsLoader.setSource("qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/service/advanced_settings/ArmingDisarmingFlow.qml")
                }
            }

            DS3.SettingsNavigationTitlePrimary {
                id: devicesAutoBypass

                title: tr.auto_bypass
                visible: hub.firmware_version_dec >= 209100

                onEntered: {
                    advancedSettingsLoader.setSource("qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/service/advanced_settings/DevicesAutoBypass.qml")
                }
            }
        }

        Column {
            width: parent.width

            visible: !!appUser.company_id  // A911-7472 & A911-7738

            DS3.Spacing {
                height: 24
            }

            DS3.SettingsContainer {
                DS3.ButtonRow {
                    text: tr.clear_notifications
                    enabled: devEnable
                    isDanger: true

                    onClicked: {
                        Popups.confirm_clear_notofications(tr.confirm_notification_deletion, function() {
                            app.hub_management_module.clear_logs_for_hub(hub.id)
                        })
                    }
                }
            }
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
            var settings = {
                "debug_log_state": logsPicker.currentIndex + 1,
                "led_brightness_level": ledBrightnessSlider.value,
                "firmware": {
                    "auto_update_enabled": autoUpdateSwitch.checked,
                },
            }

            if (timeZones.selectedId) {
                settings["time_zone"] = timeZones.selectedId
            }

            Popups.please_wait_popup()
            app.hub_management_module.apply_update(management, hub, settings)
        }
    }
}
