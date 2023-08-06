import QtQuick 2.7
import QtQuick.Controls 2.2


Connections {
    target: app.hub_management_module

    onRejectedEmails: (info_text) => Popups.text_popup(tr.information, info_text)

    onRejectedUserEmails: Popups.popupByPath(
        "qrc:/resources/qml/screens/home/pages/objects/object/popups/RejectedUserEmailsPopup.qml",
        {
            "info_text": info_text
        }
    )
}
