import QtQuick 2.12
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/911/DS3" as DS3

DS3.Popup {
    id: popup

    property var policy: policy
    property var agreement: agreement

    width: 423

    closePolicy: Popup.NoAutoClose

    hasCrossButton: false

    title: tr.terms_services_changes_title_desktop

    Column {
        width: parent.width

        DS3.Text {
            id: textLabel

            width: parent.width

            text: tr.terms_services_changes_descr_desktop
            style: ui.ds3.text.body.MRegular
            color: ui.ds3.figure.secondary
            horizontalAlignment: Text.AlignHCenter
        }

        DS3.Spacing { height: 16 }

        DS3.SettingsContainer {
            width: parent.width

            DS3.InfoTitleButtonIcon {
                id: endUserAgreement

                property var localizedLink: {
                    var locale = tr.get_locale()
                    if (locale == 'ru') {return "https://ajax.systems/ru/end-user-agreement/"}
                    if (locale == 'uk') {return "https://ajax.systems/ua/end-user-agreement/"}
                    return "https://ajax.systems/end-user-agreement/"
                }

                width: parent.width

                visible: agreement != 0
                atomTitle.title: tr.end_user_agreement
                buttonIconControl.source: "qrc:/resources/images/Athena/common_icons/ExternalLink-M.svg"

                onRightIconClicked: {
                    Qt.openUrlExternally(localizedLink)
                }
            }
        }

        DS3.Spacing { height: 24 }

        DS3.Text {
            id: textExplanation

            width: parent.width

            text: tr.agree_all_updates_desktop
            style: ui.ds3.text.body.MRegular
            color: ui.ds3.figure.secondary
            horizontalAlignment: Text.AlignHCenter
        }

        DS3.Spacing { height: 24 }
        DS3.Spacing { height: 8 }

        DS3.ButtonContained {
            id: firstButton

            anchors.horizontalCenter: parent.horizontalCenter

            width: parent.width

            text: tr.accept_and_proceed

            onClicked: {
                app.restore_pass_module.update_user_policies(agreement, policy)
                userPolicyAndAgreementChecker.running = true
                popup.close()
            }
        }

        DS3.Spacing { height: 8 }

        DS3.ButtonOutlined {
            id: secondButton

            anchors.horizontalCenter: parent.horizontalCenter

            width: parent.width

            color: ui.ds3.figure.interactive
            text: tr.reject

            onClicked: {
                popup.close()
                application.debug("user popup -> sign out")
                app.login_module.logout()
                screenLoader.source = "qrc:/resources/qml/screens/login/Login.qml"
            }
        }
    }
}