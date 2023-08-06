import QtQuick 2.12
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.13

import "qrc:/resources/js/desktop/popups.js" as Popups
import "qrc:/resources/qml/components/911/DS3" as DS3

Item {
    signal openSecondStepTwoFaPopupSignal()

    Connections {
        target: app.login_module

        onLogoutSignal: {
            popup.close()
        }
    }

    DS3.NavBarModal {
        id: navBarModal

        headerText: tr.app_settings
        showCloseIcon: false
        isRound: false
    }

    DS3.ScrollView {
        anchors {
            topMargin: navBarModal.height
        }

        contentSpacing: 24
//--------------------- Notifications --------------------------------------

        Column {
            width: parent.width

            spacing: 1

            DS3.SettingsContainer {
                width: parent.width

                DS3.SettingsSwitch {
                    checked: settings.pushes_enabled
                    title: tr.notifications
                    cancelBinding: false

                    onSwitched: () => {
                        settings.pushes_enabled = !settings.pushes_enabled
                    }
                }
            }
            DS3.Comment {
                width: parent.width

                text: appUser.company_id ? tr.notifications_desc_company : tr.notifications_desc
            }
        }

//------------------------- Language ---------------------------------------

        DS3.SettingsContainer {
            width: parent.width

            DS3.SettingsPickerTitleSecondary {
                id: languageCombobox

                atomTitle.title: tr.a911_language
                model: util.native_language_from_list(tr.get_available_tr().languages)
                currentIndex: tr.get_available_tr().languages.indexOf(tr.get_selected())

                onActivated: {
                    application.debug("user popup -> select lang -> " + tr.get_available_tr().languages[languageCombobox.currentIndex], false)
                    __ga__.report("activity", "user popup -> select lang")
                    tr.select_lang(currentIndex)
                }
            }
        }

//------------------------- Units of measure -------------------------------

        Column {
            width: parent.width

            spacing: 1

            DS3.SettingsContainer {
                width: parent.width

                DS3.SettingsPickerTitleSecondary {
                    id: unitsOfMeasureCombobox

                    atomTitle.title: tr.units_of_measure
                    model: [tr.automatic, tr.metric_system, tr.imperial_system]
                    currentIndex: ['auto', 'metric', 'imperial'].indexOf(settings.measure_system_raw)

                    onActivated: {
                        if (unitsOfMeasureCombobox.currentIndex == 0) {settings.measure_system = 'auto'}
                        if (unitsOfMeasureCombobox.currentIndex == 1) {settings.measure_system = 'metric'}
                        if (unitsOfMeasureCombobox.currentIndex == 2) {settings.measure_system = 'imperial'}
                    }
                }
            }

            DS3.Comment {
                width: parent.width

                text: tr.metric_imperial_desktop_desc
            }
        }


//------------------------- Scale -------------------------------


        Column {
            width: parent.width

            spacing: 1
            visible: __scaling_features__

            DS3.SettingsContainer {
                width: parent.width

                DS3.SettingsPickerTitleSecondary {
                    id: scaleCombobox

                    suffix: "%"
                    atomTitle.title: tr.screen_scale_desktop
                    model: ["100", "125", "150", "175", "200"]
                    currentIndex: ["1", "1.25", "1.5", "1.75", "2"].indexOf(settings.scale)

                    onActivated: {
                        let currentScale = model[currentIndex] / 100
                        if (currentScale == settings.scale) return
                        settings.scale = currentScale
                        Popups.app_restart_required_popup()
                    }
                }
            }

            DS3.Comment {
                width: parent.width

                text: tr.screen_scale_descr_desktop
            }
        }
    }
}