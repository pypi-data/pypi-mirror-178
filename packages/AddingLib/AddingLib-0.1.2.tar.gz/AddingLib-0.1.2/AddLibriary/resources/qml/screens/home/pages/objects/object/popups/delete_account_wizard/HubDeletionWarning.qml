import QtQuick 2.7
import QtQuick.Controls 2.2

import "qrc:/resources/qml/components/911/DS3" as DS3
import "qrc:/resources/qml/" as Root
import "qrc:/resources/js/desktop/popups.js" as DesktopPopups

DS3.Popup {
    id: hubDeletionWarningPopup

    width: 500
    height: maxPopupHeight

    modal: true
    focus: true

    header: DS3.NavBarModal {
        onClosed: () => hubDeletionWarningPopup.close()
    }

    DS3.Spacing {
        height: 24
    }

    DS3.InfoContainer {
        id: infoContainer

        titleComponent.text: tr.delete_data_from_hub_title
        descComponent.text: tr.delete_data_from_hub_descr
    }

    DS3.Spacing {
        height: 24
    }

    Root.ContextLoader {
        id: accountDelerionContextLoader

        height: item.height

        contextTarget: app.accountDeletion
    }

    DS3.Spacing {
        height: 24
    }
    Connections {
        target: appUser

        // onDeleteUserAccountRequestFailed: hubDeletionWarningPopup.close()
        onUserHasCompaniesEmployeeResponse: hubDeletionWarningPopup.close()
        onUserHasCompaniesOwnerResponse: hubDeletionWarningPopup.close()
        onDeleteUserAccountRequestResponse: hubDeletionWarningPopup.close()
    }
    footer: DS3.ButtonBar {
        id: nextButton

        buttonText: tr.next
        hasBackground: true

        button.onClicked: {
            appUser.delete_user_account_request()
            DesktopPopups.please_wait_popup(tr.checking_progress, 30, [appUser.deleteUserAccountRequestFailed, appUser.userHasCompaniesEmployeeResponse, appUser.userHasCompaniesOwnerResponse, appUser.deleteUserAccountRequestResponse,])
        }
    }
}