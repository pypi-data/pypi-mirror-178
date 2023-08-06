import QtQuick 2.12
import QtQuick.Controls 2.2

import "qrc:/resources/qml/components/911/DS3/popups" as DS3Popups

DS3Popups.Dialog {
    id: popup

    property var callback: () => {}

    title: tr.dont_delete_title
    text: tr.dont_delete_descr

    firstButtonCallback: callback
    firstButtonText: tr.interrupt_button_account
    isFirstButtonRed: true
    isVertical: true

    secondButtonText: tr.delete_button_account
}