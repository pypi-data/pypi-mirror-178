import QtQuick 2.12
import QtQuick.Controls 2.13
import QtQuick.Window 2.13
import QtGraphicalEffects 1.13

import "qrc:/resources/js/popups.js" as Popups
import "qrc:/resources/js/desktop/popups.js" as DesktopPopups
import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/qml/components/desktop/"
import "qrc:/resources/qml/update"
import "qrc:/resources/js/desktop/popups.js" as PopupsDS3

ApplicationWindow {
    id: application

    property var last_window_state: null
    property var countries: null
    property var notifications: []
    property int notificationsMaxCount: 3
    property int notificationsShowingTime: 5 * 1000
    property var shortDateFormat: util.short_date_format(application.locale)
    property var shortTimeFormat: util.short_time_format(application.locale)
    property var shortDateTimeFormat: util.short_date_time_format(application.locale)
    property var policies_versions: {}
    property int initialLanguageIndex: -1
//  The maximum allowed height for popups
    property var maxPopupHeight: application.height - 64

    function debug(text, ga=true) {
        // disable log part : text.contains(smth) -> return
        console.log(":: QML :: " + text)

        if (ga) {
            __ga__.report("activity", text)
        }
    }

    signal notificationClicked()
    signal waitPopup()
    signal closeHubSettings()
    signal errorPopup(variant errorText)
    signal informationPopup(variant info)
    signal goToHubNotifications(variant hub_id)
    signal addDevicePopup(variant hub, variant roomIndex)
    signal addFibraDevicePopup(variant hub, variant roomIndex)

    // access card
    signal addAccessCardPopup(string mode)

    signal addCameraPopup(variant roomIndex, variant rooms)
    signal addCommonCameraPopup(variant roomIndex, variant rooms)
    signal addWireInputPopup(variant roomIndex, variant management)
    signal addWireSirenPopup(variant roomIndex, variant management)
    signal addYavirAccessControlPopup(variant roomIndex, variant management)
    signal addUserSettingsPopup()
    signal confirmEditedUserSettingsPopup(variant title, variant additionalTitle)
    signal notificationPopup(variant text)
    signal reportPopup(variant data)
    signal selectIncidentWithId(variant incident_id)
    signal confirmedToFaSuccess()
    signal goToChangePasswordSignal()
    signal goToSecurityTabAndOpenSessionsPopupSignal()
    signal toForgotPassword(variant user_email)
//    signal refreshPressed()

    signal openConfirmInvitesPopup(variant text, variant pro, variant emails, variant management)
    signal openTimezonesWarning(variant todo)

    onAddAccessCardPopup: {
        Popups.add_access_card_popup(mode)
    }

    onErrorPopup: {
        Popups.text_popup(tr.error, errorText)
    }

    onInformationPopup: {
        Popups.text_popup(tr.information, info)
    }

    onReportPopup: {
        Popups.report_popup(data)
    }

    onWaitPopup: {
        Popups.wait_popup()
    }

    onVisibilityChanged: {
        application.update()
        util.processEvents()
        if (visibility == Window.Windowed || visibility == Window.FullScreen || visibility == Window.Maximized) last_window_state = visibility
    }

    onConfirmedToFaSuccess: {
        Popups.two_fa_activated()
    }

    onOpenTimezonesWarning: {
        DesktopPopups.timezones_warning_popup(todo)
    }

    onOpenConfirmInvitesPopup: {
        DesktopPopups.confirm_invites_popup(text, pro, emails, management)
    }

    LayoutMirroring.enabled: true
    LayoutMirroring.childrenInherit: settings.language == "Farsi"

    Component.onCompleted: {
        screenLoader.source = __design_system__ ? "qrc:/resources/qml/screens/ds/Main.qml" : "qrc:/resources/qml/screens/login/Login.qml"

        /*
            Create new notification instances on application startup.
        */
        for (var i = 0; i < application.notificationsMaxCount; i++) {
            Popups.create_notification()
        }
    }

    Connections {
        target: app

        onNullScreen: {
            screenLoader.source = ""
        }

        onActionFailed: {
            DesktopPopups.error_popup(error_text)
        }

        onTestVolumePopupSucces: {
            Popups.text_popup(tr.information, text)
        }

        onNoGroupModeAccess: {
            Popups.text_popup(tr.error, error_text)
        }

        onRaiseWindow: {
            if (application.last_window_state == Window.FullScreen) {
                application.showFullScreen()
            } else if (application.last_window_state == Window.Maximized) {
                application.showMaximized()
            } else {
                application.show()
            }
            application.raise()
            application.requestActivate()
        }

        onLocalizedCountries: {
            application.countries = data
        }

        onTextPopup: {
            Popups.text_popup(info_label, info_text)
        }

        onPleaseWaitPopupOld: {
            DesktopPopups.please_wait_popup()
        }

        onUpdateEthernetSettings: {
            DesktopPopups.please_wait_popup(tr.updating_ethernet_settings, 180)
        }

        onNewEntering: {
            Popups.confirm_entering_popup(session)
        }

        onWhatsNew: {
            DesktopPopups.whats_new(news)
        }

        onNewNotification: {
            /*
                Ignore notification generation if the setting is disabled.
            */
            if (!settings.pushes_enabled) return

            /*
                Update each notification with
                information from the previous notification.
            */
            for (var i = application.notificationsMaxCount - 1; i > 0; i--) {
                application.notifications[i].updateNotification(
                    application.notifications[i - 1].notification,
                    application.notifications[i - 1].startTime
                )
            }

            /*
                Update the first notification with new data.
            */
            application.notifications[0].updateNotification(notification, new Date().getTime())
        }

        onCurrentUserReloaded: {
            if (userPolicyAndAgreementChecker.isTriggered) {
                app.get_policies_versions()
                userPolicyAndAgreementChecker.isTriggered = false
            }
        }

        onPoliciesVersionsReloaded: {
            if (result["agreement"] || result["policy"]) {
                if (userPolicyAndAgreementChecker.isFirstLoop) {
                    userPolicyAndAgreementChecker.isFirstLoop = false
                    app.restore_pass_module.update_user_policies(result["agreement"], result["policy"])
                } else if ((result["agreement"] != appUser.signed_end_user_agreement_version) || (result["policy"] != appUser.signed_privacy_policy_version)) {
                    PopupsDS3.popupByPath(
                        "qrc:/resources/qml/screens/home/pages/objects/object/popups/UpdateAgreement.qml",
                        {"agreement": result["agreement"], "policy": result["policy"]}
                    )
                    userPolicyAndAgreementChecker.running = false
                    return
                }
            }
        }
    }

    Connections {
        target: updater

        onInstallationStarted: {
            DesktopPopups.please_wait_download_popup()
        }
    }

    Connections {
        target: app.login_module

        onLoginSuccess: {
            screenLoader.source = "qrc:/resources/qml/screens/home/Home.qml"
            userPolicyAndAgreementChecker.running = true
        }

        onProLoginSuccess: {
            screenLoader.source = "qrc:/resources/qml/screens/pro/Home.qml"
            userPolicyAndAgreementChecker.running = true
        }

        onLoginIntoCompanySuccess: {
            screenLoader.source = "qrc:/resources/qml/screens/home/Home.qml"
            userPolicyAndAgreementChecker.running = true
        }

        onLoginIntoCompanyTabSuccess: {
            screenLoader.setSource("qrc:/resources/qml/screens/home/Home.qml", {"loginTab": tab})
            userPolicyAndAgreementChecker.running = true
        }

        onLoginIntoAccountSuccess: {
            screenLoader.source = "qrc:/resources/qml/screens/pro/Home.qml"
            userPolicyAndAgreementChecker.running = true
        }

        onEnterVerificationCode: {
            Popups.two_fa_confirm_login(loginData)
        }

        onLogoutSignal: {
            userPolicyAndAgreementChecker.isFirstLoop = true
            userPolicyAndAgreementChecker.running = false
        }
    }

    Connections {
        target: app.hub_management_module

        onKeyRegTimePopup: {
            DesktopPopups.key_reg_time_popup(hub_id, text, management)
        }
    }

    Connections {
        target: application

        onAddDevicePopup: {
            DesktopPopups.add_device_popup(hub, roomIndex)
        }
        onAddCameraPopup: {
            DesktopPopups.add_camera_popup(roomIndex, rooms)
        }
        onAddWireInputPopup: {
            DesktopPopups.add_wire_input_popup(roomIndex, management)
        }
        onAddWireSirenPopup: {
            DesktopPopups.add_wire_siren_popup(roomIndex, management)
        }
        onAddYavirAccessControlPopup: {
            DesktopPopups.add_yavir_access_control_popup(roomIndex, management)
        }
        onAddCommonCameraPopup: {
            DesktopPopups.add_common_camera_popup(roomIndex, rooms)
        }
        onAddUserSettingsPopup: {
            Popups.user_settings_popup()
        }
        onConfirmEditedUserSettingsPopup: {
            Popups.confirm_change_password(title, additionalTitle)
        }
        onNotificationPopup: {
            Popups.notification_popup(text)
        }
        onToForgotPassword: {
            Popups.password_change_popup(user_email)
        }
    }

    width: 1352
    height: {
        return Screen.desktopAvailableHeight > 768 ? 768 : 680
    }

    visible: true
    title: __application_name__ + "  —  " + __version__
    locale: Qt.locale(tr.locale)
    minimumWidth: 1352
    minimumHeight: 680

    onClosing: {
        function action() {
            close.accepted = true
            screenLoader.source = ""
            app.close()
            Qt.quit()
        }

        close.accepted = false
        Popups.exit_popup(action)
    }

    AppBackground {}

    ScreenLoader {
        id: screenLoader
    }

    AjaxImageFileDialog {
        id: imageFileDialog
    }

    Item {
        anchors.fill: parent

        focus: true

        Keys.onPressed: {
            if (event.key == Qt.Key_F1) {
                tr.next_translation()
                event.accepted = true;
                return
            }
            if (event.key == Qt.Key_F2) {
                tr.prev_translation()
                event.accepted = true;
                return
            }

            /*
            if (event.key == Qt.Key_F5 || (event.key == Qt.Key_R && (event.modifiers & Qt.ControlModifier))) {
                refreshPressed()
                event.accepted = true;
                return
            }
            */
        }
    }

    UpdateBar {}

    Shortcut {
        property var last_language_index:  __farsi_language_features__ == true ? 30 : 29

        sequence: "Ctrl+f6"
        context: Qt.ApplicationShortcut

        onActivated: {
            if (__build__ == "qa") {
                if (initialLanguageIndex == -1) {
                    initialLanguageIndex = tr.get_available_tr().languages.indexOf(settings.language)
                }
                if (initialLanguageIndex == last_language_index) {
                    initialLanguageIndex = 3 // set English if loads with Localize as default
                }
                if(tr.get_available_tr().languages.indexOf(settings.language) == last_language_index) {
                    tr.select_lang(initialLanguageIndex)
                } else {
                    tr.select_lang(last_language_index)
                }
            }
        }
    }


    Timer {
        id: ramUsageLogTimer
        repeat: true
        running: true
        interval: app.log_period_ram_usage

        onTriggered: {
            app.write_ram_usage_to_log()
        }
    }

    Timer {
        id: userPolicyAndAgreementChecker

        property var isFirstLoop: true
        property var isTriggered: false

        repeat: true
        running: false
        interval: { if (isFirstLoop)  return 1000 * 5
            return 1000 * 60 * 60 * 24 } // 24 hours

        onTriggered: {
            userPolicyAndAgreementChecker.isTriggered = true
            if(typeof appUser !== "undefined") {
                app.get_current_user()
            }
        }
    }

    Timer {
        interval: 1000 * 60 * 10
        repeat: true

        triggeredOnStart: false
        running: true

        onTriggered: {
            __ga__.report("activity", "ping")
        }
    }

    /* ------------------------------------------------ */
    /* desktop tests */
    Accessible.name: "application"
    Accessible.description: "application instance"
    Accessible.role: Accessible.Application
    /* ------------------------------------------------ */
}
