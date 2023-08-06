import QtQuick 2.12

import "qrc:/resources/js/popups.js" as Popups
import "qrc:/resources/js/desktop/popups.js" as DesktopPopups
import "qrc:/resources/qml/components/911/DS3" as DS3


Item {
    id: security

    property var sessions: app.security_module.sessions
    property var filteredSessions: app.security_module.filtered_sessions
    property alias enableTwoFa: enableTwoFa

    signal openSecondStepTwoFaPopupSignal()

    onOpenSecondStepTwoFaPopupSignal: {
        app.security_module.get_secret()
        Popups.second_step_2fa_popup()
    }

    Connections {
        target: app.security_module

        onTwoFaStateSignal: {
            enableTwoFa.checked = state == "ENABLED"
        }
    }

    Connections {
        target: app.login_module

        onLogoutSignal: {
            popup.close()
        }
    }

    DS3.NavBarModal {
        id: navBarModal

        headerText: sessionsPage.visible ? tr.sessions : tr.account_security
        showCloseIcon: false
        isRound: false
        showBackArrow: sessionsPage.visible

        onBackAreaClicked: mainContent.visible = true

        DS3.ButtonIcon {
            id: manualIcon

            anchors {
                verticalCenter: parent.verticalCenter
                left: undefined
                right: parent.right
                leftMargin: 16
                rightMargin: 16
            }

            source: "qrc:/resources/images/Athena/common_icons/Update-M.svg"
            opacity: enabled ? 1 : 0.3
            visible: !mainContent.visible

            onClicked: {
                app.security_module.get_sessions()
                DesktopPopups.waitPopup(app.security_module.sessionsReceived)
            }
        }
    }

    DS3.ScrollView {
        id: mainContent

        width: parent.width

        anchors.topMargin: navBarModal.height

        contentSpacing: 24

        Column {
            width: parent.width

            spacing: 1

            DS3.SettingsContainer {
                DS3.SettingsSwitch {
                    id: enableTwoFa

                    title: tr.t_factor_authentication

                    onSwitched: () => {
                        if (checked) {
                            let settings = {
                                confirmText: tr.disable,
                                saveColor: ui.colors.red1,
                            };

                            Popups.confirm_action_popup(tr.disable_2_factor_authentication, function() {
                                app.security_module.disable_two_fa()
                            }, settings)
                        } else {
                            if (sessions.length) {
                                var popup_created = Popups.terminate_session_warning_popup(tr.log_out_pay_attention_devices, function() {
                                   popup_created.close()
                                }, true)
                            }
                            else {
                                openSecondStepTwoFaPopupSignal()
                            }
                        }
                    }
                }
            }

            DS3.Comment {
                text: tr.t_factor_authentication_info_new
            }
        }

        Column {
            width: parent.width

            spacing: 1

            DS3.SettingsContainer {
                DS3.SettingsNavigationTitlePrimary {
                    title: tr.sessions

                    onEntered: {
                        app.security_module.get_sessions()
                        mainContent.visible = false
                    }
                }
            }

            DS3.Comment {
                text: tr.learn_more
                itemsColor: ui.ds3.figure.interactive

                DS3.MouseArea {
                    onClicked: Qt.openUrlExternally("http://instructionservice.ops.ajax.systems/2fa?lang=" + tr.get_locale())
                }
            }
        }
    }

    DS3.ScrollView {
        id: sessionsPage

        anchors.topMargin: navBarModal.height

        visible: !mainContent.visible
        contentSpacing: 24

        Column {
            width: parent.width

            DS3.TitleSection {
                text: tr.current_session
                isCaps: true
                isBgTransparent: true
                forceTextToLeft: true
            }

            DS3.SettingsContainer {
                DS3.InfoSession {
                    sessionVersion: {
                        var label = ""
                        if (sessions.this_session.application_label) {
                            label = util.label_correct(sessions.this_session.application_label)
                        }
                        if (sessions.this_session.client_version_major) {
                            label += " "
                            label += sessions.this_session.client_version_major
                        }
                        return label
                    }
                    sessionDevice: sessions.this_session.client_device_model + ", " + sessions.this_session.client_os
                    sessionIp: sessions.this_session.last_connection_ip != "n/a" ?
                        (!!sessions.this_session.last_connection_ip && sessions.this_session.last_connection_ip)
                        : tr.na
                    isCurrentSession: true
                }
            }
        }

        DS3.SettingsContainer {
            visible: sessions.legacy_session_exists

            DS3.CommentImportant {
                status: DS3.CommentImportant.Status.Attention
                imageItem.source: "qrc:/resources/images/Athena/views_icons/Alarm-M.svg"
                atomTitle {
                    title: tr.scenario_important_note
                    subtitle: tr.sessions_were_detected
                }
            }

            DS3.CommentImportant {
                imageItem.source: "qrc:/resources/images/Athena/notifications/Update-M.svg"
                atomTitle.subtitle: tr.update_app_for_sessions
            }

            DS3.CommentImportant {
                imageItem.source: "qrc:/resources/images/Athena/notifications/TwoFactorAuthentication-M.svg"
                atomTitle {
                    subtitle: util.insert(
                        tr.kill_session_manually,
                        ["<a href='#changePassword'><font color='#5AE4AA'>", "</font></a>", "<a href='#twoFa'><font color='#5AE4AA'>", "</font></a>"]
                    )
                    subtitleItem {
                        textFormat: Text.RichText

                        onLinkActivated: {
                            mainContent.visible = true
                            if (link == "#changePassword") stackLayout.currentIndex = 0
                        }
                    }
                }
            }
        }

        Column {
            width: parent.width

            visible: !!sessionsRepeater.count

            spacing: 1

            DS3.TitleSection {
                text: tr.active_sessions
                isCaps: true
                isBgTransparent: true
                forceTextToLeft: true
            }

            DS3.SettingsContainerItem {
                width: parent.width
                height: childrenRect.height

                isFirst: true

                DS3.ButtonRow {
                    color: ui.ds3.figure.transparent
                    text: tr.terminate_other_sessions
                    isDanger: true
                    rowLeftAlign: true

                    onClicked: {
                        Popups.terminate_session_warning_popup(
                            sessions.length == 1 ? tr.log_out_pay_attention : tr.log_out_pay_attention_devices,
                            function() { app.security_module.kill_sessions(sessions.sessions(), true) },
                            false
                        )
                    }
                }
            }

            Repeater {
                id: sessionsRepeater

                width: parent.width

                model: filteredSessions

                DS3.SettingsContainerItem {
                    width: parent.width
                    height: childrenRect.height

                    isLast: index == sessionsRepeater.count - 1

                    DS3.InfoSession {
                        color: ui.ds3.figure.transparent
                        sessionVersion: {
                            var label = ""
                            if (session.application_label) {
                                label = util.label_correct(session.application_label)
                            }
                            if (session.client_version_major) {
                                label += " "
                                label += session.client_version_major
                            }
                            return label
                        }
                        sessionDevice: session.client_device_model + ", " + session.client_os
                        sessionIp: session.last_connection_ip != "n/a" ? session.last_connection_ip : ""
                        sessionDate: time_str
                        sessionTime: date_str
                        onClicked: Popups.terminate_session_warning_popup(
                            tr.log_out_pay_attention,
                            function() {app.security_module.kill_sessions([session.session_id], true)},
                            false
                        )
                    }
                }
            }
        }
    }
}
