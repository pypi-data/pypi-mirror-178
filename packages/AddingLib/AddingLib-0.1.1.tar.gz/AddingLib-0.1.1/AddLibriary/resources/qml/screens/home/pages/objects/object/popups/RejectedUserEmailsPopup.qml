import QtQuick 2.12
import QtQuick.Controls 2.2


import "qrc:/resources/js/popups.js" as Popups
import "qrc:/resources/qml/components/911/DS3/popups" as DS3Popups
import "qrc:/resources/qml/components/911/DS3/" as DS3


DS3Popups.Dialog {
    id: popup

    property var info_text

    title: tr.invite_not_sent_title
    text: info_text
    firstButtonText: tr.i_will_check
}