import QtQuick 2.7
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/911/DS3/popups" as DS3Popups
import "qrc:/resources/js/desktop/popups.js" as DesktopPopups

DS3Popups.Dialog {
    id: popup

    width: 320
    // height: 292

    autoClose: false

    title: tr.delete_account_title_copy
    text: tr.delete_account_descr
    
    isVertical: true
    isFirstButtonRed: true
    firstButtonText: tr.delete_button
    secondButtonText: tr.cancel

    Connections {
        target: appUser

    onIsUserHasHubsRequestResponse: { popup.close() }
    }
    firstButtonCallback: () => {
        appUser.does_user_have_personal_hubs()
        DesktopPopups.please_wait_popup(tr.checking_progress, 30, [appUser.isUserHasHubsRequestFailed, appUser.isUserHasHubsRequestResponse])
    }
    secondButtonCallback: popup.close
}