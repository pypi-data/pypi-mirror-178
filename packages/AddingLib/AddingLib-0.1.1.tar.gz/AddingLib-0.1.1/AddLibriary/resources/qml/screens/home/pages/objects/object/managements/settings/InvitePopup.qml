
import QtQuick 2.12
import QtQuick.Controls 2.2

import "qrc:/resources/qml/components/desktop/"
import "qrc:/resources/qml/screens/home/pages/objects/object/popups/"
import "qrc:/resources/js/desktop/popups.js" as Popups
import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.Popup {
    id: popup

    width: 500
    height: 500

    modal: true
    focus: true

    property string title: ""
    property var sideMargin: 24

    Connections {
        target: app

        onActionSuccess: {
            popup.close()
        }

        onActionFailed: {
           popup.close()
        }
    }

    header: DS3.NavBarModal {
        id: installersSettingsBar

        anchors.top: undefined

        headerText: title
        isRound: false

        onClosed: () => {
            popup.close()
        }
    }

    DS3.Spacing {
        height: 24
    }

    DS3.Text {
        width: parent.width

        horizontalAlignment: Text.AlignHCenter
        text: util.insert(tr.you_can_add_up_to_N_users_to_this_hub, [hub.user_limit])
        color: ui.ds3.figure.secondary
        style: ui.ds3.text.body.LRegular
    }

    DS3.Spacing {
        height: 24
    }

    DS3.SettingsContainer {
        id: companyEmailItem

        width: parent.width

        anchors.horizontalCenter: parent.horizontalCenter

        DS3.InputMultiLine {
            id: companyEmail

            regex: ui.regexes.multi_emails

            atomInputMultiline {
                label: tr.email
                placeholderText: tr.email_tip
                required: false
            }
        }
    }

    footer: DS3.ButtonBar {
        id: nextButton

        buttonText: tr.next
        hasBackground: true
        enabled: companyEmail.atomInputMultiline.text.length

        button.onClicked: {
            if (!companyEmail.isValid) return

            if (!users.emails_count(companyEmail.atomInputMultiline.text.trim().toLowerCase(), false)) {
                var countVac = users.get_count_new_users_available()
                Popups.text_popup(tr.information, util.insert(tr.there_are_ld_free_slots_left_please_remove_some_emails_from_list_and_try_again, [countVac]))
                return
            }

            var data = users.check_invites(false, companyEmail.atomInputMultiline.text.trim().toLowerCase())
            if (data.accepted.length == 0) {
                Popups.text_popup(tr.information, tr.specified_email_are_already_registered_on_a_hub)
                return
            }
            if (data.denied.length == 0) {
                Popups.please_wait_popup()
                app.hub_management_module.invite_users(hub, companyEmail.atomInputMultiline.text.trim().toLowerCase(), false)
                return
            }

            application.openConfirmInvitesPopup(
                util.insert(tr.some_emails_was_ignored_because_they_already_registered_with_the_hub_invites_will_be_sent_to_following_emails, data.accepted),
                false,
                companyEmail.atomInputMultiline.text.trim().toLowerCase(),
                management
            )
        }
    }
}
